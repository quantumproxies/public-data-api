# Public Data API

[![ci](https://github.com/quantumproxies/public-data-api/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/public-data-api/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Public data from Python or the command line: arXiv preprints, scholarly works from OpenAlex, ClinicalTrials.gov studies, FDA adverse-event reports, World Bank indicators, daily weather, Wikipedia summaries, Wikidata entities, Open Library books and NVD vulnerabilities, as JSON or CSV. The code is free and open source (MIT). Each of these sources publishes its own public API; this package puts all ten behind one client and one QuanticData sign-in, returns the same flat rows and CSV export for every source, retries on rate limits and dropped connections, and runs long jobs in the background.

```bash
pip install git+https://github.com/quantumproxies/public-data-api
public-data login
public-data arxiv "retrieval augmented generation" --max-results 25 -o papers.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=public-data-api).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `public-data arxiv` | query, or ti:/au:/abs: syntax | Title, abstract, authors, categories, dates, PDF link, 16 fields per row ([fields and price](https://quanticdata.io/collectors/arxiv-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 100 |
| `public-data papers` | search terms | Title, authors, year, citations, DOI, venue, open-access link, 32 fields per row ([fields and price](https://quanticdata.io/collectors/academic-paper-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 200 |
| `public-data trials` | search term, or --condition | Status, phase, conditions, interventions, sponsor, enrollment, dates, 34 fields per row ([fields and price](https://quanticdata.io/collectors/clinical-trials-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 200 |
| `public-data fda` | drug name or field:value query | Drugs, reactions, seriousness, outcome, patient sex and age, dates, 22 fields per row ([fields and price](https://quanticdata.io/collectors/fda-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 500 |
| `public-data worldbank` | indicator code + --countries | Country, year, value, indicator name, unit, 10 fields per row ([fields and price](https://quanticdata.io/collectors/world-bank-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 200 |
| `public-data weather` | place name, or --latitude / --longitude | Conditions, temperature, precipitation, wind, UV, sunrise and sunset, 28 fields per row ([fields and price](https://quanticdata.io/collectors/weather-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 30 |
| `public-data wikipedia` | search text, or --titles | Extract, description, image, Wikidata id, coordinates, last edit, 16 fields per row ([fields and price](https://quanticdata.io/collectors/wikipedia-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 50 |
| `public-data wikidata` | name or term | Entity id, label, description, aliases, Wikipedia link, 17 fields per row ([fields and price](https://quanticdata.io/collectors/wikidata-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 50 |
| `public-data books` | title, author:, isbn: or subject: | Authors, first year, ISBN, ratings, editions, subjects, cover, 22 fields per row ([fields and price](https://quanticdata.io/collectors/book-data-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 100 |
| `public-data cve` | keyword, or --cve-id | Description, CVSS score and vector, severity, CWE, affected products, KEV status, 23 fields per row ([fields and price](https://quanticdata.io/collectors/cve-api/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api)) | up to 200 |

`worldbank` needs an indicator code and `--countries`: `public-data worldbank NY.GDP.MKTP.CD --countries IT DE --year-from 2015`. `weather` takes a place name or `--latitude` / `--longitude`, with `--days` ahead (1 to 16) and `--past-days` of history (0 to 92). `wikipedia` and `wikidata` read any language edition with `--lang`; `trials` filters with `--condition` and `--status`; `cve` looks up one record with `--cve-id` or filters with `--severity` and `--known-exploited`.

## Sample output

A real row from `public-data arxiv "retrieval augmented generation" --max-results 2` (2026-10-23):

```json
{
  "doi": null,
  "url": "https://arxiv.org/abs/2506.06962v3",
  "rank": 1,
  "title": "AR-RAG: Autoregressive Retrieval Augmentation for Image Generation",
  "authors": [
    "Jingyuan Qi",
    "Zhiyang Xu",
    "Qifan Wang",
    "Lifu Huang"
  ],
  "comment": "Image Generation, Retrieval Augmented Generation",
  "pdf_url": "https://arxiv.org/pdf/2506.06962v3",
  "updated": "2025-06-14T00:40:34Z",
  "version": 3,
  "abstract": "We introduce Autoregressive Retrieval Augmentation (AR-RAG), a novel paradigm that enhances image generation by autoregressively incorporating knearest neighbor retrievals at the patch level.",
  "arxiv_id": "2506.06962v3",
  "published": "2025-06-08T01:33:05Z",
  "categories": [
    "cs.CV"
  ],
  "journal_ref": null,
  "author_count": 4,
  "primary_category": "cs.CV"
}
```

## Python

```python
from quanticdata_public_data_api import OpenData

data = OpenData()  # saved login, or QUANTICDATA_API_KEY

papers = data.arxiv("retrieval augmented generation", sort="latest", max_results=25)
for p in papers:
    print(p["published"], p["primary_category"], p["title"])

gdp = data.worldbank("NY.GDP.MKTP.CD", countries=["IT", "DE"], year_from=2015)
gdp.to_csv("gdp_it_de.csv")

trials = data.trials("cancer immunotherapy", status="RECRUITING", max_results=50)
print(len(trials), trials.rows[0]["nct_id"], trials.rows[0]["phases"])

rome = data.weather("Rome", days=7)
for d in rome:
    print(d["date"], d["weather"], d["temp_min_c"], d["temp_max_c"])

log4shell = data.cve(cve_id="CVE-2021-44228")
print(log4shell.rows[0]["severity"], log4shell.rows[0]["cvss_score"])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Literature search**: Collect the newest arXiv preprints and the most cited OpenAlex works on a topic into one CSV, with year, authors, DOI, citations and PDF links. See [`examples/literature_search.py`](examples/literature_search.py).
- **Country indicator panel**: Pull several World Bank indicators for a list of countries and write one row per country and year, one column per indicator. See [`examples/country_indicators.py`](examples/country_indicators.py).
- **Known exploited CVEs in your stack**: Check the products you run against the CISA Known Exploited Vulnerabilities catalog, with CVSS score, due date and patch links. See [`examples/kev_check.py`](examples/kev_check.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `public-data run <id> -o out.csv` collects it later.

### `public-data arxiv`

Preprint search on arXiv — abstracts, authors, categories and PDF links.

```
public-data arxiv QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Free text, e.g. "retrieval augmented generation", or arXiv field syntax such as ti:diffusion. |
| `--category` | string |  | Subject class, e.g. cs.AI, cs.CL or stat.ML. |
| `--sort` | relevance / latest / updated | `relevance` | Result order. |
| `--max-results` | integer | `25` | How many papers to deliver at most (1–100). You pay only for delivered papers. |

### `public-data papers`

Scholarly works from OpenAlex: title, authors, year, citations, DOI, venue, open-access link, abstract, topic and institutions.

```
public-data papers QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Search terms across title, abstract and metadata. |
| `--year-from` | integer |  | Only works published this year or later. |
| `--year-to` | integer |  | Only works published up to this year. |
| `--open-access` | boolean | `False` | Only works with a free full text. |
| `--sort` | relevance / cited / newest | `relevance` | relevance (default), cited (most cited first) or newest. |
| `--max-results` | integer | `25` | How many works to deliver at most (1–200). You pay only for delivered works. |

### `public-data trials`

Studies from ClinicalTrials.gov — status, phase, conditions, interventions, sponsor.

```
public-data trials [QUERY] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Free-text search term: a drug, disease or sponsor, e.g. "cancer immunotherapy". |
| `--condition` | string |  | Restrict to a medical condition. |
| `--status` | RECRUITING / NOT_YET_RECRUITING / ACTIVE_NOT_RECRUITING / COMPLETED / ENROLLING_BY_INVITATION / SUSPENDED / TERMINATED / WITHDRAWN |  | Recruitment status filter. |
| `--max-results` | integer | `20` | How many studies to deliver at most (1–200). You pay only for delivered studies. |

### `public-data fda`

Drug adverse-event reports from the FDA FAERS database — drugs, reactions, seriousness.

```
public-data fda QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | A drug name, e.g. ibuprofen, or an openFDA field:value query. |
| `--max-results` | integer | `50` | How many reports to deliver at most (1–500). You pay only for delivered reports. |

### `public-data worldbank`

World Bank development indicators per country and year, by indicator code: GDP, population, inflation and the rest of the World Bank catalog.

```
public-data worldbank INDICATOR [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `INDICATOR` | string |  | World Bank indicator code, e.g. NY.GDP.MKTP.CD (GDP in current US$) or SP.POP.TOTL (population). |
| `--countries` | string[] |  | Country codes, ISO2 or ISO3, e.g. IT DE, or WLD for the world. Required. |
| `--year-from` | integer |  | First year (default: all). |
| `--year-to` | integer |  | Last year (default: latest). |
| `--include-empty` | boolean | `False` | Keep rows whose value is null. |
| `--max-results` | integer | `50` | How many datapoints to deliver at most (1–200). You pay only for delivered datapoints. |

### `public-data weather`

Daily weather for a place name or coordinates, from Open-Meteo: conditions, temperatures, precipitation, wind, UV, sunshine, sunrise and sunset, up to 16 days ahead and 92 days back.

```
public-data weather [LOCATION] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `LOCATION` | string |  | City or place name, e.g. Rome. |
| `--latitude` | number |  | Exact latitude (skips geocoding). |
| `--longitude` | number |  | Exact longitude. |
| `--days` | integer | `7` | Days ahead, 1 to 16 (default 7). |
| `--past-days` | integer | `0` | Days of recent history to add before the forecast, 0 to 92 (default 0). |
| `--max-results` | integer | `16` | How many days to deliver at most (1–30). You pay only for delivered days. |

### `public-data wikipedia`

Wikipedia article summaries, by search query or exact titles, in any language edition: lead extract, short description, images, Wikidata id, coordinates and last edit.

```
public-data wikipedia [QUERY] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Search Wikipedia and read the top results, e.g. "web scraping". Use this or --titles. |
| `--titles` | string[] |  | Exact article titles or /wiki/ URLs to read, e.g. "Web scraping". Use this or QUERY. |
| `--lang` | string |  | Wikipedia language edition (en, it, de…). Default en. |
| `--max-results` | integer | `10` | How many articles to deliver at most (1–50). You pay only for delivered articles. |

### `public-data wikidata`

Resolve a name to a stable Wikidata entity id — the join key for entity linking.

```
public-data wikidata QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Name or term to resolve, e.g. "Leonardo da Vinci". |
| `--lang` | string |  | Language for labels/descriptions (default en). |
| `--include-details` | boolean | `False` | Also read instance-of, country, official website, coordinates and image for each entity. |
| `--max-results` | integer | `10` | How many entities to deliver at most (1–50). You pay only for delivered entities. |

### `public-data books`

Book search over the Open Library catalog — ISBN, authors, ratings, covers.

```
public-data books QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Title or author words, e.g. "dune herbert", or author:, isbn:, subject: syntax. |
| `--sort` | relevance / new / old / rating | `relevance` | Result order. |
| `--max-results` | integer | `25` | How many books to deliver at most (1–100). You pay only for delivered books. |

### `public-data cve`

Vulnerabilities from the NIST NVD — CVE id, description, CVSS score, severity, CWE.

```
public-data cve [KEYWORD] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `KEYWORD` | string |  | Search term: a product, vendor or words of the CVE text, e.g. log4j. |
| `--severity` | LOW / MEDIUM / HIGH / CRITICAL |  | Filter to a CVSS v3 severity. |
| `--cve-id` | string |  | Look up one CVE, e.g. CVE-2021-44228. |
| `--known-exploited` | boolean | `False` | Only CVEs in the CISA Known Exploited Vulnerabilities catalog. |
| `--max-results` | integer | `20` | How many CVEs to deliver at most (1–200). You pay only for delivered CVEs. |

## Output fields

<details><summary><code>public-data arxiv</code>: 16 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `arxiv_id` | string | arXiv identifier (with version). |
| `title` | string or null | Title. |
| `abstract` | string or null | Abstract. |
| `authors` | string[] | Authors (up to 20). |
| `published` | string or null | First submission date. |
| `updated` | string or null | Last version date. |
| `categories` | string[] | Subject categories. |
| `doi` | string or null | DOI when assigned. |
| `pdf_url` | string | Direct PDF. |
| `url` | string | Abstract page. |
| `author_count` | integer | Number of authors. |
| `primary_category` | string or null | Primary arXiv category. |
| `comment` | string or null | Author comment (pages, venue, notes). |
| `journal_ref` | string or null | Journal reference, when published. |
| `version` | integer or null | Version number of this entry. |

</details>

<details><summary><code>public-data papers</code>: 32 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `id` | string | OpenAlex work id. |
| `title` | string | Paper title. |
| `authors` | string[] | Author names in byline order, each author once — the first 15 (author_count counts them all). |
| `year` | integer or null | Publication year. |
| `cited_by_count` | integer or null | Citation count. |
| `doi` | string or null | DOI. |
| `type` | string or null | Work type (article, review…). |
| `venue` | string or null | Host venue/journal. |
| `is_open_access` | boolean | Open-access flag. |
| `oa_url` | string or null | Open-access PDF/landing URL. |
| `abstract` | string or null | Abstract (reconstructed). |
| `url` | string | OpenAlex work URL. |
| `author_count` | integer | Number of distinct authors, all of them (authors lists the first 15). |
| `institutions` | string[] | Author institutions (up to 10). |
| `countries` | string[] | Author countries (ISO codes). |
| `publication_date` | string or null | Publication date (YYYY-MM-DD). |
| `language` | string or null | Language code. |
| `fwci` | number or null | Field-weighted citation impact (1.0 = field average). |
| `referenced_works_count` | integer or null | Number of works cited. |
| `venue_type` | string or null | Venue type (journal, repository, conference…). |
| `issn` | string or null | Linking ISSN of the venue. |
| `volume` | string or null | Volume. |
| `issue` | string or null | Issue. |
| `pages` | string or null | Page range. |
| `oa_status` | string or null | Open-access status (gold, green, hybrid, bronze, closed). |
| `pdf_url` | string or null | Direct PDF link, when one is open. |
| `license` | string or null | License of the open copy. |
| `topic` | string or null | Primary topic. |
| `field` | string or null | Field of the primary topic. |
| `keywords` | string[] | Keywords (up to 10). |
| `is_retracted` | boolean | Whether the work was retracted. |

</details>

<details><summary><code>public-data trials</code>: 34 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `nct_id` | string | ClinicalTrials.gov NCT id. |
| `title` | string or null | Brief title. |
| `status` | string or null | Overall recruitment status. |
| `phases` | string[] | Trial phase(s). |
| `study_type` | string or null | Interventional, Observational… |
| `conditions` | string[] | Conditions studied. |
| `interventions` | string[] | Interventions/treatments. |
| `sponsor` | string or null | Lead sponsor. |
| `enrollment` | integer or null | Planned/actual enrollment. |
| `start_date` | string or null | Study start date. |
| `completion_date` | string or null | Study completion date. |
| `has_results` | boolean | Whether results are posted. |
| `url` | string | Study page URL. |
| `official_title` | string or null | Official title. |
| `acronym` | string or null | Study acronym. |
| `allocation` | string or null | Allocation (RANDOMIZED…). |
| `masking` | string or null | Masking (NONE, DOUBLE…). |
| `primary_purpose` | string or null | Primary purpose (TREATMENT, PREVENTION…). |
| `intervention_types` | string[] | Intervention types (DRUG, DEVICE, BIOLOGICAL…). |
| `sponsor_class` | string or null | Lead sponsor class (INDUSTRY, NIH, OTHER…). |
| `collaborators` | string[] | Collaborating organisations. |
| `enrollment_type` | string or null | ACTUAL or ESTIMATED. |
| `primary_completion_date` | string or null | Primary completion date. |
| `first_posted` | string or null | Date first posted. |
| `last_updated` | string or null | Date last updated. |
| `sex` | string or null | Eligible sex (ALL, FEMALE, MALE). |
| `minimum_age` | string or null | Minimum age. |
| `maximum_age` | string or null | Maximum age. |
| `healthy_volunteers` | boolean or null | Whether healthy volunteers are accepted. |
| `primary_outcomes` | string[] | Primary outcome measures (up to 5). |
| `locations_count` | integer | Number of study sites. |
| `countries` | string[] | Countries with a study site. |
| `summary` | string or null | Brief summary (up to 1,500 characters). |

</details>

<details><summary><code>public-data fda</code>: 22 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `report_id` | string | FAERS safety report id. |
| `serious` | boolean | Whether the report is flagged serious. |
| `serious_reasons` | string[] | Death, hospitalization, life-threatening… |
| `drugs` | string[] | Reported medicinal products. |
| `reactions` | string[] | Reactions (MedDRA terms). |
| `patient_sex` | string or null | male/female when reported. |
| `patient_age` | string or null | Patient age as reported. |
| `country` | string or null | Country of occurrence. |
| `received_date` | string or null | Received date (ISO). |
| `report_type` | string or null | Report type code. |
| `suspect_drugs` | string[] | Drugs the reporter held responsible. |
| `drug_roles` | string[] | Roles present in the report: suspect, concomitant, interacting. |
| `generic_names` | string[] | Generic names of the reported drugs. |
| `brand_names` | string[] | Brand names of the reported drugs. |
| `indications` | string[] | What the drugs were taken for. |
| `reaction_outcomes` | string[] | Outcomes of the reactions (recovered, fatal…). |
| `patient_age_years` | number or null | Patient age in years, when reported in years. |
| `patient_weight_kg` | number or null | Patient weight, kg. |
| `latest_update` | string or null | Date of the latest information on the report. |
| `reporter` | string or null | Who reported: physician, pharmacist, consumer… |
| `manufacturer_report_id` | string or null | Manufacturer's own report number. |

</details>

<details><summary><code>public-data worldbank</code>: 10 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `country` | string or null | Country name. |
| `country_code` | string or null | ISO3 code. |
| `year` | string or null | Year. |
| `value` | number or null | Indicator value. |
| `indicator` | string | Indicator code. |
| `indicator_name` | string or null | Indicator label. |
| `country_iso2` | string or null | ISO 3166-1 alpha-2 country code. |
| `unit` | string or null | Unit, when the Bank states one. |
| `obs_status` | string or null | Observation status flag, when present. |

</details>

<details><summary><code>public-data weather</code>: 28 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `date` | string | Day (YYYY-MM-DD, local time). |
| `weather` | string or null | Conditions label. |
| `weather_code` | integer or null | WMO code. |
| `temp_max_c` | number or null | Max temperature °C. |
| `temp_min_c` | number or null | Min temperature °C. |
| `precipitation_mm` | number or null | Precipitation sum, mm. |
| `precipitation_probability` | number or null | Max precipitation probability %. |
| `wind_max_kmh` | number or null | Max wind speed km/h. |
| `location` | string or null | Resolved place name. |
| `country` | string or null | Country. |
| `latitude` | number | Latitude used. |
| `longitude` | number | Longitude used. |
| `feels_like_max_c` | number or null | Maximum apparent temperature, °C. |
| `feels_like_min_c` | number or null | Minimum apparent temperature, °C. |
| `rain_mm` | number or null | Rain from large-scale weather systems, mm. Showers are not included here; precipitation_mm counts rain, showers and snow. |
| `snowfall_cm` | number or null | Snowfall, cm. |
| `precipitation_hours` | number or null | Hours with precipitation. |
| `wind_gusts_kmh` | number or null | Maximum wind gusts, km/h. |
| `wind_direction_deg` | number or null | Dominant wind direction, degrees. |
| `uv_index_max` | number or null | Maximum UV index. |
| `sunshine_hours` | number or null | Hours of sunshine. |
| `sunrise` | string or null | Sunrise, local time of the place. |
| `sunset` | string or null | Sunset, local time of the place. |
| `region` | string or null | First-level administrative region of the geocoded place. |
| `country_code` | string or null | ISO country code of the geocoded place. |
| `elevation_m` | number or null | Elevation of the forecast grid cell, metres. |
| `timezone` | string or null | IANA timezone of the place. |

</details>

<details><summary><code>public-data wikipedia</code>: 16 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `title` | string | Article title. |
| `page_id` | integer or null | MediaWiki page id. |
| `description` | string or null | Short description (Wikidata). |
| `extract` | string | Lead-section plain-text extract. |
| `url` | string | Canonical article URL. |
| `thumbnail` | string or null | Lead image thumbnail. |
| `lang` | string | Language edition read. |
| `last_modified` | string or null | Last revision time (ISO 8601). |
| `wikidata_id` | string or null | Wikidata item id (Q…). |
| `image` | string or null | Full-size lead image. |
| `revision_id` | integer or null | Revision id of the summary. |
| `page_type` | string or null | standard, disambiguation… |
| `latitude` | number or null | Latitude, for places. |
| `longitude` | number or null | Longitude, for places. |
| `word_count` | integer or null | Article length in words (search runs). |

</details>

<details><summary><code>public-data wikidata</code>: 17 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based relevance rank. |
| `id` | string | Wikidata entity id (Q…). |
| `label` | string or null | Entity label. |
| `description` | string or null | Short description. |
| `concept_uri` | string or null | Canonical entity URI (join key). |
| `url` | string | Wikidata page URL. |
| `matched` | string or null | The text that matched the query. |
| `match_type` | string or null | How it matched (label, alias…). |
| `aliases` | string[] | Alternative names in the requested language and English. |
| `wikipedia_url` | string or null | Wikipedia article in the requested language (English as fallback). |
| `wikipedia_title` | string or null | Title of that article. |
| `instance_of` | string[] or null | Q-ids the entity is an instance of (include_details). |
| `country_id` | string or null | Q-id of the entity's country (include_details). |
| `official_website` | string or null | Official website (include_details). |
| `latitude` | number or null | Latitude (include_details). |
| `longitude` | number or null | Longitude (include_details). |
| `image_url` | string or null | Wikimedia Commons image (include_details). |

</details>

<details><summary><code>public-data books</code>: 22 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `title` | string | Title. |
| `authors` | string[] | Authors (up to 5). |
| `first_publish_year` | integer or null | First publication year. |
| `isbn` | string or null | ISBN (13 preferred). |
| `publishers` | string[] | Publishers (up to 3). |
| `languages` | string[] | Language codes of the editions, all of them. |
| `pages` | integer or null | Median page count. |
| `rating` | number or null | Community rating (0-5). |
| `ratings_count` | integer or null | Number of ratings. |
| `editions` | integer or null | Edition count. |
| `cover_url` | string or null | Cover image. |
| `url` | string | Open Library page. |
| `subtitle` | string or null | Subtitle. |
| `work_id` | string | Open Library work id (OL…W). |
| `want_to_read_count` | integer or null | Readers who shelved it as want-to-read. |
| `already_read_count` | integer or null | Readers who shelved it as read. |
| `subjects` | string[] | Subjects (up to 10). |
| `author_ids` | string[] | Open Library author ids. |
| `ebook_access` | string or null | public, borrowable, printdisabled or no_ebook. |
| `read_url` | string or null | Internet Archive page of the readable/borrowable copy. |
| `cover_url_large` | string or null | Large cover image. |

</details>

<details><summary><code>public-data cve</code>: 23 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `cve_id` | string | CVE identifier. |
| `description` | string or null | English description. |
| `cvss_score` | number or null | CVSS base score. |
| `severity` | string or null | CVSS severity. |
| `cvss_vector` | string or null | CVSS vector string. |
| `cwe` | string[] | CWE weakness ids. |
| `published` | string or null | Publish date. |
| `last_modified` | string or null | Last modified date. |
| `status` | string or null | Vulnerability status. |
| `references` | string[] | Reference URLs. |
| `url` | string | NVD detail page. |
| `cvss_version` | string or null | CVSS version of the score. |
| `exploitability_score` | number or null | CVSS exploitability sub-score. |
| `impact_score` | number or null | CVSS impact sub-score. |
| `attack_vector` | string or null | Attack vector (NETWORK, LOCAL…). |
| `affected_products` | string[] | Vulnerable vendor:product pairs from the CPE configurations. |
| `source` | string or null | Organisation that assigned the CVE. |
| `known_exploited` | boolean | In the CISA Known Exploited Vulnerabilities catalog. |
| `kev_added` | string or null | Date added to the CISA KEV catalog. |
| `kev_due_date` | string or null | CISA remediation due date. |
| `kev_required_action` | string or null | CISA required action. |
| `patch_urls` | string[] | References tagged Patch or Vendor Advisory. |

</details>

## Sign-in and API keys

- `public-data login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `public-data login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `public-data login --api-key`.
- `public-data logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/arxiv_papers/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "retrieval augmented generation", "max_results": 2}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this public data API free?**

The code is free and MIT-licensed. Runs go through your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need an API key for each source?**

No. One QuanticData sign-in covers all ten commands and the requests run on QuanticData's side. Every source here publishes its own public API; what this package adds is one client for all of them, the same flat rows and CSV, JSON or JSONL export for every source, retries on rate limits and dropped connections, and background runs (`--no-wait`) you collect later with `public-data run <run_id>`.

**How many rows can one run return?**

Up to 100 arXiv papers, 200 OpenAlex works, 200 trials, 500 FDA reports, 200 World Bank datapoints, 30 days of weather, 50 Wikipedia articles, 50 Wikidata entities, 100 books or 200 CVEs per run; ask for fewer with --max-results and you pay only for what is delivered.

**Which World Bank indicator codes can I use?**

Any code of the World Bank catalog, for example NY.GDP.MKTP.CD (GDP in current US$) or SP.POP.TOTL (population). Pass the countries with --countries as ISO2 or ISO3 codes; WLD gives the world total.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Lists such as authors, categories, conditions and reactions are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/kev_check.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Financial Data API](https://github.com/quantumproxies/financial-data-api): Financial data API for Python and the command line.
- [Package Registry API](https://github.com/quantumproxies/package-registry-api): Package registry API for Python and the command line.
- [Web Scraper API](https://github.com/quantumproxies/web-scraper-api): Web scraper API for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=public-data-api).
