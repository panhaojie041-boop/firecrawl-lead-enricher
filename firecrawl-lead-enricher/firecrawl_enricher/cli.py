"""
Command-Line Interface for Firecrawl Lead Enricher.
"""

import argparse
import sys
from .core import FirecrawlLeadEnricher
from .exporter import DataExporter

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
except ImportError:
    console = None


def main():
    parser = argparse.ArgumentParser(
        description="Firecrawl Lead Enricher - Extract structured B2B intelligence from websites using Firecrawl SDK."
    )
    parser.add_argument("url", help="Target website URL (e.g., https://example.com)")
    parser.add_argument("--crawl", action="store_true", help="Crawl multiple pages instead of single scrape")
    parser.add_argument("--pages", type=int, default=3, help="Max pages to crawl when --crawl is enabled (default: 3)")
    parser.add_argument("--out-json", help="Path to save JSON output")
    parser.add_argument("--out-csv", help="Path to save CSV output")
    parser.add_argument("--out-md", help="Path to save Markdown audit report")

    args = parser.parse_args()

    if console:
        console.print(f"[bold cyan]Firecrawl Lead Enricher[/bold cyan] analyzing [bold yellow]{args.url}[/bold yellow]...")
    else:
        print(f"Analyzing {args.url}...")

    enricher = FirecrawlLeadEnricher()
    profile = enricher.enrich(args.url, crawl=args.crawl, max_pages=args.pages)

    if console:
        table = Table(title=f"Company Profile: {profile.company_name}")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row("Website", profile.url)
        table.add_row("Industry", profile.industry or "N/A")
        table.add_row("Tagline", profile.tagline or "N/A")
        table.add_row("Emails", ", ".join(profile.contact.emails) or "None")
        table.add_row("Phones", ", ".join(profile.contact.phones) or "None")
        table.add_row("VAT / Tax ID", profile.vat_or_tax_id or "N/A")
        table.add_row("Address", profile.contact.address or "N/A")
        table.add_row("Socials", ", ".join(profile.contact.social_links) or "None")
        table.add_row("Tech Stack", ", ".join(profile.tech_stack_detected) or "None")

        console.print(table)
    else:
        print(f"Company: {profile.company_name}")
        print(f"Industry: {profile.industry}")
        print(f"Emails: {', '.join(profile.contact.emails)}")
        print(f"Phones: {', '.join(profile.contact.phones)}")

    if args.out_json:
        DataExporter.to_json(profile, args.out_json)
        msg = f"[OK] Saved JSON to {args.out_json}"
        if console:
            console.print(f"[green]{msg}[/green]")
        else:
            print(msg)

    if args.out_csv:
        DataExporter.to_csv([profile], args.out_csv)
        msg = f"[OK] Saved CSV to {args.out_csv}"
        if console:
            console.print(f"[green]{msg}[/green]")
        else:
            print(msg)

    if args.out_md:
        report = DataExporter.to_markdown_report(profile)
        with open(args.out_md, "w", encoding="utf-8") as f:
            f.write(report)
        msg = f"[OK] Saved Markdown Report to {args.out_md}"
        if console:
            console.print(f"[green]{msg}[/green]")
        else:
            print(msg)


if __name__ == "__main__":
    main()
