"""
Simple example demonstrating how to enrich a single company website using Firecrawl Lead Enricher.
"""

from firecrawl_enricher import FirecrawlLeadEnricher
from firecrawl_enricher.exporter import DataExporter


def main():
    # Initialize enricher (reads FIRECRAWL_API_KEY from environment or .env)
    enricher = FirecrawlLeadEnricher()

    target_url = "https://acme-industrial.com"
    print(f"Scraping and analyzing {target_url} with Firecrawl...")

    # Enrich profile
    profile = enricher.enrich(target_url, crawl=False)

    print("\n--- Extracted Company Profile ---")
    print(f"Company: {profile.company_name}")
    print(f"Industry: {profile.industry}")
    print(f"Emails: {profile.contact.emails}")
    print(f"Phones: {profile.contact.phones}")
    print(f"Address: {profile.contact.address}")
    print(f"VAT / Tax ID: {profile.vat_or_tax_id}")
    print(f"Tech Stack: {profile.tech_stack_detected}")

    # Generate Markdown Report
    report = DataExporter.to_markdown_report(profile)
    print("\n--- Generated Markdown Audit Report Preview ---")
    print(report[:300] + "...\n")


if __name__ == "__main__":
    main()
