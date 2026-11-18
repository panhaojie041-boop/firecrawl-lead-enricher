"""
Exporters for Firecrawl Lead Enricher.
Outputs profiles to JSON, CSV, and Markdown summaries.
"""

import csv
import json
from typing import List
from .models import CompanyProfile


class DataExporter:

    @staticmethod
    def to_json(profile: CompanyProfile, filepath: str, indent: int = 2):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile.model_dump(), f, ensure_ascii=False, indent=indent)

    @staticmethod
    def to_csv(profiles: List[CompanyProfile], filepath: str):
        if not profiles:
            return

        headers = [
            "Company Name", "URL", "Industry", "Tagline", "Emails", "Phones",
            "Address", "VAT/Tax ID", "Social Links", "Tech Stack", "Pages Crawled"
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for p in profiles:
                writer.writerow([
                    p.company_name,
                    p.url,
                    p.industry or "",
                    p.tagline or "",
                    "; ".join(p.contact.emails),
                    "; ".join(p.contact.phones),
                    p.contact.address or "",
                    p.vat_or_tax_id or "",
                    "; ".join(p.contact.social_links),
                    ", ".join(p.tech_stack_detected),
                    p.crawled_pages_count
                ])

    @staticmethod
    def to_markdown_report(profile: CompanyProfile) -> str:
        md = [
            f"# Company Intelligence Report: {profile.company_name}",
            f"**Website:** {profile.url} | **Industry:** {profile.industry or 'N/A'}",
            "",
            f"> {profile.tagline or 'No tagline detected.'}",
            "",
            "## Overview",
            profile.description or "No description provided.",
            "",
            "## Contact Information",
            f"- **Emails:** {', '.join(profile.contact.emails) if profile.contact.emails else 'None found'}",
            f"- **Phones:** {', '.join(profile.contact.phones) if profile.contact.phones else 'None found'}",
            f"- **Address:** {profile.contact.address or 'N/A'}",
            f"- **VAT / Tax ID:** {profile.vat_or_tax_id or 'N/A'}",
            f"- **Social Profiles:** {', '.join(profile.contact.social_links) if profile.contact.social_links else 'None'}",
            "",
            "## Products & Services",
        ]
        if profile.products_and_services:
            for s in profile.products_and_services:
                md.append(f"- **{s.name}**" + (f": {s.description}" if s.description else ""))
        else:
            md.append("- No specific services itemized in headers.")

        md.extend([
            "",
            "## Detected Tech Stack",
            ", ".join(profile.tech_stack_detected) if profile.tech_stack_detected else "None detected",
            "",
            f"*(Enriched via Firecrawl Python SDK • Pages analyzed: {profile.crawled_pages_count})*"
        ])

        return "\n".join(md)
