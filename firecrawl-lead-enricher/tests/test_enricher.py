"""
Unit tests for Firecrawl Lead Enricher.
"""

from firecrawl_enricher.core import FirecrawlLeadEnricher
from firecrawl_enricher.models import CompanyProfile


SAMPLE_PAGE_TEXT = """# Nexus Robotics
Autonomous Warehouse Automation and Robotics

Nexus Robotics builds next-generation automated guided vehicles (AGVs) and AI vision sorting for industrial fulfillment centers.

## Solutions
- Autonomous Guided Vehicles
- High-Speed Vision Sorting
- Warehouse Orchestration Engine

## Contact Information
Headquarters: Via Torino 15, 10100 Torino, Italy
Sales: contact@nexus-robotics.com, info@nexus-robotics.com
Direct Line: +39 011 55443322
Partita IVA: IT98765432101
LinkedIn: https://linkedin.com/company/nexus-robotics

Built with Python, FastAPI, Docker, and React.
"""


def test_parsing_profile():
    enricher = FirecrawlLeadEnricher()
    profile = enricher.parse_content("https://nexus-robotics.com", SAMPLE_PAGE_TEXT)

    assert profile.company_name == "Nexus-robotics"
    assert profile.industry == "Manufacturing & Industrial" or profile.industry == "Technology & Software"
    assert "contact@nexus-robotics.com" in profile.contact.emails
    assert "+39 011 55443322" in profile.contact.phones
    assert profile.vat_or_tax_id == "IT98765432101"
    assert "Python" in profile.tech_stack_detected
    assert "FastAPI" in profile.tech_stack_detected
    assert len(profile.products_and_services) >= 2


def test_url_normalization():
    enricher = FirecrawlLeadEnricher()
    assert enricher._normalize_url("example.com") == "https://example.com"
    assert enricher._normalize_url("http://example.com") == "http://example.com"
    assert enricher._normalize_url("https://example.com") == "https://example.com"
