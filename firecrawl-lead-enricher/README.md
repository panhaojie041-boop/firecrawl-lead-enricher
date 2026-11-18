# 🔍 Firecrawl Lead Enricher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Built with Firecrawl](https://img.shields.io/badge/Built%20with-Firecrawl%20SDK-orange.svg)](https://docs.firecrawl.dev/sdks/python)

An AI-powered B2B intelligence and lead enrichment tool built using the **[Firecrawl Python SDK](https://docs.firecrawl.dev/sdks/python)**. 

Extract clean, structured business data (company overview, contact information, VAT/tax IDs, products/services, tech stack, and social profiles) from any target website or domain with a single command.

---

## 🚀 Features

- **Built on Firecrawl SDK:** Leverages Firecrawl's advanced web scraping and deep crawling engine to convert complex web pages into LLM-ready markdown.
- **Automated Entity Extraction:**
  - 🏢 **Company Details:** Official name, industry categorization, tagline, and comprehensive overview.
  - 📞 **Contact Intelligence:** Direct verified emails, phone numbers, physical addresses, and social media handles.
  - 📑 **Corporate Identifiers:** Automatic detection of European VAT IDs (Partita IVA, CIF, etc.) and tax identifiers.
  - 📦 **Products & Services:** Extraction of core solutions and offerings.
  - 💻 **Tech Stack Detection:** Identifies frameworks, cloud providers, and libraries referenced on the site.
- **Multi-Format Export:** Generates clean **JSON**, consolidated **CSV** (for CRM import), and formatted **Markdown Intelligence Reports**.
- **Interactive CLI:** Rich terminal visualization with structured tables and status indicators.

---

## 📐 Architecture

```
┌───────────────────────┐
│ Target Domain / URL   │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────────────────────┐
│ Firecrawl Python SDK (firecrawl-py)   │
│ • Scrapes or deep-crawls pages        │
│ • Converts HTML to clean Markdown     │
└──────────┬────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────┐
│ FirecrawlLeadEnricher Parser          │
│ • Contact & VAT extraction            │
│ • Industry inference & services       │
│ • Tech stack pattern recognition      │
└──────────┬────────────────────────────┘
           │
           ▼
┌───────────────────────────────────────┐
│ Multi-Format Data Exporter            │
│ ├── JSON Output (API / DB ready)      │
│ ├── CSV Export (HubSpot / CRM import) │
│ └── Markdown Executive Report         │
└───────────────────────────────────────┘
```

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/firecrawl-lead-enricher.git
   cd firecrawl-lead-enricher
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Firecrawl API Key:**
   Get your API key at [firecrawl.dev](https://firecrawl.dev).
   ```bash
   cp .env.example .env
   # Edit .env and set your FIRECRAWL_API_KEY
   ```

---

## 💻 Usage

### 1. Interactive CLI

Enrich a single domain and display a rich summary table in the terminal:
```bash
python -m firecrawl_enricher.cli https://acme-industrial.com
```

Deep crawl up to 5 pages and export results to JSON, CSV, and Markdown report:
```bash
python -m firecrawl_enricher.cli https://acme-industrial.com \
  --crawl \
  --pages 5 \
  --out-json company.json \
  --out-csv leads.csv \
  --out-md report.md
```

### 2. Python SDK Integration

```python
from firecrawl_enricher import FirecrawlLeadEnricher
from firecrawl_enricher.exporter import DataExporter

# Initialize enricher
enricher = FirecrawlLeadEnricher()

# Scrape and extract structured intelligence
profile = enricher.enrich("https://example-enterprise.com", crawl=False)

print(f"Company: {profile.company_name}")
print(f"Industry: {profile.industry}")
print(f"Emails: {profile.contact.emails}")
print(f"VAT / Tax ID: {profile.vat_or_tax_id}")

# Export to Markdown executive report
report = DataExporter.to_markdown_report(profile)
print(report)
```

### 3. Batch Processing

Run the batch processing example to enrich a list of domains and output a consolidated CSV:
```bash
python examples/batch_enrich_leads.py
```

---

## 🧪 Testing

Run unit tests with `pytest`:
```bash
pytest tests/
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
