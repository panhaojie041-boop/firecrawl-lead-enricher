"""
Firecrawl Lead Enricher
AI-Powered Company Intelligence & Lead Enrichment Tool
Built with Firecrawl Python SDK (https://docs.firecrawl.dev/sdks/python)
"""

__version__ = "1.0.0"
__author__ = "OpenMausBot Team"

from .core import FirecrawlLeadEnricher
from .models import CompanyProfile, ContactInfo, ProductService

__all__ = ["FirecrawlLeadEnricher", "CompanyProfile", "ContactInfo", "ProductService"]
