"""
Data models for Firecrawl Lead Enricher.
Compatible with standard dataclasses and Pydantic.
"""

from typing import List, Optional

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False


if HAS_PYDANTIC:
    class ContactInfo(BaseModel):
        emails: List[str] = Field(default_factory=list)
        phones: List[str] = Field(default_factory=list)
        address: Optional[str] = Field(default=None)
        social_links: List[str] = Field(default_factory=list)

    class ProductService(BaseModel):
        name: str
        description: Optional[str] = Field(default=None)

    class CompanyProfile(BaseModel):
        url: str
        company_name: str
        tagline: Optional[str] = Field(default=None)
        industry: Optional[str] = Field(default=None)
        description: Optional[str] = Field(default=None)
        vat_or_tax_id: Optional[str] = Field(default=None)
        contact: ContactInfo = Field(default_factory=ContactInfo)
        products_and_services: List[ProductService] = Field(default_factory=list)
        tech_stack_detected: List[str] = Field(default_factory=list)
        crawled_pages_count: int = Field(default=1)

else:
    from dataclasses import dataclass, field, asdict

    @dataclass
    class ContactInfo:
        emails: List[str] = field(default_factory=list)
        phones: List[str] = field(default_factory=list)
        address: Optional[str] = None
        social_links: List[str] = field(default_factory=list)

    @dataclass
    class ProductService:
        name: str
        description: Optional[str] = None

    @dataclass
    class CompanyProfile:
        url: str
        company_name: str
        tagline: Optional[str] = None
        industry: Optional[str] = None
        description: Optional[str] = None
        vat_or_tax_id: Optional[str] = None
        contact: ContactInfo = field(default_factory=ContactInfo)
        products_and_services: List[ProductService] = field(default_factory=list)
        tech_stack_detected: List[str] = field(default_factory=list)
        crawled_pages_count: int = 1

        def model_dump(self):
            return asdict(self)
