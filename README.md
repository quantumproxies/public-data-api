# arXiv preprints API — examples

Preprint search on arXiv — abstracts, authors, categories and PDF links.

**Live page, full schema & pricing → [quanticdata.io/collectors/arxiv-api/](https://quanticdata.io/collectors/arxiv-api/)**

Searches arXiv's export API (keyless). One row per paper: arXiv id, title, abstract, authors, submitted and updated dates, subject categories, DOI when present and the direct PDF link. A plain query searches every field; arXiv prefixes (ti:, au:, abs:, cat:) pass through, and category narrows to one subject class (cs.AI, stat.ML…). Sort by relevance, submission or update date.

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/arxiv_papers/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mixture of experts", "sort": "latest", "max_results": 10}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `query` (string, required) — Free text, or arXiv fielded syntax (ti:, au:, abs:).
- `category` (string) — Subject class (cs.AI, cs.CL, stat.ML…).
- `sort` (string) — Result order.
- `max_results` (integer) — How many papers to deliver at most (1–100). You pay only for delivered papers.

## Output — one row per paper

| field | type | description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `arxiv_id` | string | arXiv identifier (with version). |
| `title` | string | Title. |
| `abstract` | string | Abstract. |
| `authors` | string[] | Authors (up to 20). |
| `published` | string | First submission date. |
| `updated` | string | Last version date. |
| `categories` | string[] | Subject categories. |
| `doi` | string | DOI when assigned. |
| `pdf_url` | string | Direct PDF. |
| `url` | string | Abstract page. |

## Pricing

**$0.0004 per delivered paper** ($0.4 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 5,000 papers — no card required.

## Links

- This collector: https://quanticdata.io/collectors/arxiv-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
