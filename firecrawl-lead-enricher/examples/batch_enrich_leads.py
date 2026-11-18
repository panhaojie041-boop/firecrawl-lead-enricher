"""
Batch enrichment script for processing multiple domains and exporting to CSV.
"""

from firecrawl_enricher import FirecrawlLeadEnricher
from firecrawl_enricher.exporter import DataExporter


def main():
    enricher = FirecrawlLeadEnricher()

    sample_domains = [
        "https://acme-industrial.com",
        "https://techcorp-logistics.io",
        "https://buildmaster-systems.org"
    ]

    profiles = []
    print(f"Starting batch enrichment of {len(sample_domains)} companies...")

    for url in sample_domains:
        print(f"-> Processing {url}...")
        p = enricher.enrich(url, crawl=False)
        profiles.append(p)

    output_csv = "enriched_leads.csv"
    DataExporter.to_csv(profiles, output_csv)
    print(f"\n[OK] Successfully enriched {len(profiles)} companies! Saved to {output_csv}")


if __name__ == "__main__":
    main()
