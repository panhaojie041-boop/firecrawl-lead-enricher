"""
Core logic for Firecrawl Lead Enricher.
Interacts with the Firecrawl Python SDK to crawl websites and extract structured company data.
"""

import os
import re
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse

try:
    from firecrawl import FirecrawlApp
except ImportError:
    FirecrawlApp = None

from .models import CompanyProfile, ContactInfo, ProductService


class FirecrawlLeadEnricher:
    """
    Enriches company domain data using Firecrawl's web scraping and crawling capabilities.
    """

    EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    PHONE_REGEX = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')
    VAT_REGEX = re.compile(r'\b(?:IT|FR|DE|ES|GB|EU)?[0-9]{11}\b|\bVAT[:\s]+[A-Z0-9-]+\b', re.IGNORECASE)

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if self.api_key and FirecrawlApp is not None:
            self.app = FirecrawlApp(api_key=self.api_key)
        else:
            self.app = None

    def enrich(self, url: str, crawl: bool = False, max_pages: int = 3) -> CompanyProfile:
        """
        Scrapes or crawls the given URL via Firecrawl and returns a structured CompanyProfile.
        """
        clean_url = self._normalize_url(url)
        markdown_content = ""
        crawled_count = 1

        if self.app:
            if crawl and max_pages > 1:
                crawl_res = self.app.crawl_url(
                    clean_url,
                    params={"limit": max_pages, "scrapeOptions": {"formats": ["markdown"]}}
                )
                if isinstance(crawl_res, dict) and "data" in crawl_res:
                    pages = crawl_res["data"]
                    crawled_count = len(pages)
                    markdown_content = "\n\n".join([p.get("markdown", "") for p in pages if isinstance(p, dict)])
                elif isinstance(crawl_res, list):
                    crawled_count = len(crawl_res)
                    markdown_content = "\n\n".join([p.get("markdown", "") for p in crawl_res if isinstance(p, dict)])
            else:
                scrape_res = self.app.scrape_url(clean_url, params={"formats": ["markdown"]})
                if isinstance(scrape_res, dict):
                    markdown_content = scrape_res.get("markdown", "")
        else:
            # Fallback mock for testing and demonstration when API key is unset
            markdown_content = self._get_sample_markdown(clean_url)

        return self.parse_content(clean_url, markdown_content, crawled_count)

    def parse_content(self, url: str, text: str, pages_count: int = 1) -> CompanyProfile:
        """
        Parses markdown text extracted by Firecrawl to build a rich CompanyProfile.
        """
        domain = urlparse(url).netloc.replace("www.", "")
        company_name = domain.split(".")[0].capitalize()

        # Extract emails & filter out common static file false positives
        raw_emails = set(self.EMAIL_REGEX.findall(text))
        emails = [
            e for e in raw_emails
            if not any(e.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".js"])
        ]

        # Extract phones
        raw_phones = set(self.PHONE_REGEX.findall(text))
        phones = [p.strip() for p in raw_phones if len(re.sub(r'\D', '', p)) >= 8]

        # Extract social links
        socials = []
        for line in text.splitlines():
            for link in ["linkedin.com/company", "twitter.com/", "x.com/", "github.com/", "facebook.com/"]:
                if link in line:
                    matches = re.findall(r'https?://[^\s)"]+', line)
                    for m in matches:
                        if link in m and m not in socials:
                            socials.append(m)

        # Detect VAT / Tax ID
        vat_matches = self.VAT_REGEX.findall(text)
        vat_id = vat_matches[0] if vat_matches else None

        # Detect products / services
        products = self._detect_services(text)

        # Detect technology mentions
        tech_keywords = [
            "Python", "FastAPI", "React", "PostgreSQL", "Docker", "Kubernetes",
            "AWS", "Google Cloud", "Azure", "Tailwind", "Next.js", "TypeScript"
        ]
        detected_tech = [t for t in tech_keywords if re.search(r'\b' + re.escape(t) + r'\b', text, re.IGNORECASE)]

        return CompanyProfile(
            url=url,
            company_name=company_name,
            tagline=self._extract_tagline(text),
            industry=self._infer_industry(text),
            description=self._extract_description(text),
            vat_or_tax_id=vat_id,
            contact=ContactInfo(
                emails=emails[:5],
                phones=phones[:5],
                address=self._extract_address(text),
                social_links=socials[:5]
            ),
            products_and_services=products,
            tech_stack_detected=detected_tech,
            crawled_pages_count=pages_count
        )

    def _normalize_url(self, url: str) -> str:
        if not url.startswith("http://") and not url.startswith("https://"):
            return "https://" + url
        return url

    def _extract_tagline(self, text: str) -> Optional[str]:
        lines = [line.strip().lstrip("#").strip() for line in text.splitlines() if line.strip()]
        for line in lines[:10]:
            if 15 <= len(line) <= 120 and not line.startswith("http"):
                return line
        return None

    def _extract_description(self, text: str) -> Optional[str]:
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 80]
        if paragraphs:
            return paragraphs[0].replace("\n", " ")
        return None

    def _infer_industry(self, text: str) -> str:
        lower = text.lower()
        if any(w in lower for w in ["software", "saas", "api", "ai", "platform"]):
            return "Technology & Software"
        if any(w in lower for w in ["logistica", "shipping", "trasporti", "magazzino"]):
            return "Logistics & Supply Chain"
        if any(w in lower for w in ["officina", "meccanica", "cnc", "carpenteria", "manufacturing"]):
            return "Manufacturing & Industrial"
        if any(w in lower for w in ["impianti", "installatori", "termoidraulica", "edilizia"]):
            return "Construction & Installation Services"
        if any(w in lower for w in ["contabilità", "consulenza", "fiscale", "commercialista"]):
            return "Professional & Financial Services"
        return "General Business"

    def _detect_services(self, text: str) -> List[ProductService]:
        services = []
        lines = text.splitlines()
        capturing = False
        for line in lines:
            line_clean = line.strip().lower()
            if any(h in line_clean for h in ["servizi", "prodotti", "solutions", "features", "services"]):
                capturing = True
                continue
            if capturing:
                if line.startswith("#"):
                    break
                if line.strip().startswith("-") or line.strip().startswith("*"):
                    item_text = line.strip().lstrip("-* ").strip()
                    if 5 <= len(item_text) <= 80:
                        services.append(ProductService(name=item_text))
                        if len(services) >= 5:
                            break
        return services

    def _extract_address(self, text: str) -> Optional[str]:
        for line in text.splitlines():
            line_str = line.strip()
            if any(k in line_str.lower() for k in ["via ", "corso ", "viale ", "piazza ", "street", "road", "ave"]):
                if 10 <= len(line_str) <= 120:
                    return line_str
        return None

    def _get_sample_markdown(self, url: str) -> str:
        return f"""# Acme Industrial Solutions
Enterprise Logistics and CNC Precision Manufacturing

Acme Industrial Solutions is an international engineering company specializing in automated manufacturing, metal fabrication, and supply chain logistics for B2B enterprises.

## Our Services
- Precision CNC Milling and Turning
- Automated Supply Chain Management
- Industrial Equipment Maintenance
- Cloud Logistics Tracking Platform

## Contact Us
Address: Via dell'Industria 42, 20100 Milano, Italy
Email: info@acme-industrial.com, support@acme-industrial.com
Phone: +39 02 98765432
VAT: IT12345678901
Follow us on LinkedIn: https://linkedin.com/company/acme-industrial
GitHub: https://github.com/acme-industrial

Powered by Python, FastAPI, Docker, and PostgreSQL.
"""
