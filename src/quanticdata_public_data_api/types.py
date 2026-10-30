"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class ArxivPapersRow(TypedDict, total=False):
    """One row of `public-data arxiv` (arxiv_papers v1.1.0)."""

    rank: int
    """1-based position."""
    arxiv_id: str
    """arXiv identifier (with version)."""
    title: Optional[str]
    """Title."""
    abstract: Optional[str]
    """Abstract."""
    authors: List[str]
    """Authors (up to 20)."""
    published: Optional[str]
    """First submission date."""
    updated: Optional[str]
    """Last version date."""
    categories: List[str]
    """Subject categories."""
    doi: Optional[str]
    """DOI when assigned."""
    pdf_url: str
    """Direct PDF."""
    url: str
    """Abstract page."""
    author_count: int
    """Number of authors."""
    primary_category: Optional[str]
    """Primary arXiv category."""
    comment: Optional[str]
    """Author comment (pages, venue, notes)."""
    journal_ref: Optional[str]
    """Journal reference, when published."""
    version: Optional[int]
    """Version number of this entry."""

class OpenalexRow(TypedDict, total=False):
    """One row of `public-data papers` (openalex v1.1.1)."""

    rank: int
    """1-based position."""
    id: str
    """OpenAlex work id."""
    title: str
    """Paper title."""
    authors: List[str]
    """Author names in byline order, each author once — the first 15 (author_count counts them all)."""
    year: Optional[int]
    """Publication year."""
    cited_by_count: Optional[int]
    """Citation count."""
    doi: Optional[str]
    """DOI."""
    type: Optional[str]
    """Work type (article, review…)."""
    venue: Optional[str]
    """Host venue/journal."""
    is_open_access: bool
    """Open-access flag."""
    oa_url: Optional[str]
    """Open-access PDF/landing URL."""
    abstract: Optional[str]
    """Abstract (reconstructed)."""
    url: str
    """OpenAlex work URL."""
    author_count: int
    """Number of distinct authors, all of them (authors lists the first 15)."""
    institutions: List[str]
    """Author institutions (up to 10)."""
    countries: List[str]
    """Author countries (ISO codes)."""
    publication_date: Optional[str]
    """Publication date (YYYY-MM-DD)."""
    language: Optional[str]
    """Language code."""
    fwci: Optional[float]
    """Field-weighted citation impact (1.0 = field average)."""
    referenced_works_count: Optional[int]
    """Number of works cited."""
    venue_type: Optional[str]
    """Venue type (journal, repository, conference…)."""
    issn: Optional[str]
    """Linking ISSN of the venue."""
    volume: Optional[str]
    """Volume."""
    issue: Optional[str]
    """Issue."""
    pages: Optional[str]
    """Page range."""
    oa_status: Optional[str]
    """Open-access status (gold, green, hybrid, bronze, closed)."""
    pdf_url: Optional[str]
    """Direct PDF link, when one is open."""
    license: Optional[str]
    """License of the open copy."""
    topic: Optional[str]
    """Primary topic."""
    field: Optional[str]
    """Field of the primary topic."""
    keywords: List[str]
    """Keywords (up to 10)."""
    is_retracted: bool
    """Whether the work was retracted."""

class ClinicalTrialsRow(TypedDict, total=False):
    """One row of `public-data trials` (clinical_trials v1.1.0)."""

    rank: int
    """1-based position."""
    nct_id: str
    """ClinicalTrials.gov NCT id."""
    title: Optional[str]
    """Brief title."""
    status: Optional[str]
    """Overall recruitment status."""
    phases: List[str]
    """Trial phase(s)."""
    study_type: Optional[str]
    """Interventional, Observational…"""
    conditions: List[str]
    """Conditions studied."""
    interventions: List[str]
    """Interventions/treatments."""
    sponsor: Optional[str]
    """Lead sponsor."""
    enrollment: Optional[int]
    """Planned/actual enrollment."""
    start_date: Optional[str]
    """Study start date."""
    completion_date: Optional[str]
    """Study completion date."""
    has_results: bool
    """Whether results are posted."""
    url: str
    """Study page URL."""
    official_title: Optional[str]
    """Official title."""
    acronym: Optional[str]
    """Study acronym."""
    allocation: Optional[str]
    """Allocation (RANDOMIZED…)."""
    masking: Optional[str]
    """Masking (NONE, DOUBLE…)."""
    primary_purpose: Optional[str]
    """Primary purpose (TREATMENT, PREVENTION…)."""
    intervention_types: List[str]
    """Intervention types (DRUG, DEVICE, BIOLOGICAL…)."""
    sponsor_class: Optional[str]
    """Lead sponsor class (INDUSTRY, NIH, OTHER…)."""
    collaborators: List[str]
    """Collaborating organisations."""
    enrollment_type: Optional[str]
    """ACTUAL or ESTIMATED."""
    primary_completion_date: Optional[str]
    """Primary completion date."""
    first_posted: Optional[str]
    """Date first posted."""
    last_updated: Optional[str]
    """Date last updated."""
    sex: Optional[str]
    """Eligible sex (ALL, FEMALE, MALE)."""
    minimum_age: Optional[str]
    """Minimum age."""
    maximum_age: Optional[str]
    """Maximum age."""
    healthy_volunteers: Optional[bool]
    """Whether healthy volunteers are accepted."""
    primary_outcomes: List[str]
    """Primary outcome measures (up to 5)."""
    locations_count: int
    """Number of study sites."""
    countries: List[str]
    """Countries with a study site."""
    summary: Optional[str]
    """Brief summary (up to 1,500 characters)."""

class OpenfdaRow(TypedDict, total=False):
    """One row of `public-data fda` (openfda v1.2.1)."""

    rank: int
    """1-based position."""
    report_id: str
    """FAERS safety report id."""
    serious: bool
    """Whether the report is flagged serious."""
    serious_reasons: List[str]
    """Death, hospitalization, life-threatening…"""
    drugs: List[str]
    """Reported medicinal products."""
    reactions: List[str]
    """Reactions (MedDRA terms)."""
    patient_sex: Optional[str]
    """male/female when reported."""
    patient_age: Optional[str]
    """Patient age as reported."""
    country: Optional[str]
    """Country of occurrence."""
    received_date: Optional[str]
    """Received date (ISO)."""
    report_type: Optional[str]
    """Report type code."""
    suspect_drugs: List[str]
    """Drugs the reporter held responsible."""
    drug_roles: List[str]
    """Roles present in the report: suspect, concomitant, interacting."""
    generic_names: List[str]
    """Generic names of the reported drugs."""
    brand_names: List[str]
    """Brand names of the reported drugs."""
    indications: List[str]
    """What the drugs were taken for."""
    reaction_outcomes: List[str]
    """Outcomes of the reactions (recovered, fatal…)."""
    patient_age_years: Optional[float]
    """Patient age in years, when reported in years."""
    patient_weight_kg: Optional[float]
    """Patient weight, kg."""
    latest_update: Optional[str]
    """Date of the latest information on the report."""
    reporter: Optional[str]
    """Who reported: physician, pharmacist, consumer…"""
    manufacturer_report_id: Optional[str]
    """Manufacturer's own report number."""

class WorldBankRow(TypedDict, total=False):
    """One row of `public-data worldbank` (world_bank v1.1.0)."""

    rank: int
    """1-based position."""
    country: Optional[str]
    """Country name."""
    country_code: Optional[str]
    """ISO3 code."""
    year: Optional[str]
    """Year."""
    value: Optional[float]
    """Indicator value."""
    indicator: str
    """Indicator code."""
    indicator_name: Optional[str]
    """Indicator label."""
    country_iso2: Optional[str]
    """ISO 3166-1 alpha-2 country code."""
    unit: Optional[str]
    """Unit, when the Bank states one."""
    obs_status: Optional[str]
    """Observation status flag, when present."""

class WeatherForecastRow(TypedDict, total=False):
    """One row of `public-data weather` (weather_forecast v1.2.1)."""

    rank: int
    """1-based position."""
    date: str
    """Day (YYYY-MM-DD, local time)."""
    weather: Optional[str]
    """Conditions label."""
    weather_code: Optional[int]
    """WMO code."""
    temp_max_c: Optional[float]
    """Max temperature °C."""
    temp_min_c: Optional[float]
    """Min temperature °C."""
    precipitation_mm: Optional[float]
    """Precipitation sum, mm."""
    precipitation_probability: Optional[float]
    """Max precipitation probability %."""
    wind_max_kmh: Optional[float]
    """Max wind speed km/h."""
    location: Optional[str]
    """Resolved place name."""
    country: Optional[str]
    """Country."""
    latitude: float
    """Latitude used."""
    longitude: float
    """Longitude used."""
    feels_like_max_c: Optional[float]
    """Maximum apparent temperature, °C."""
    feels_like_min_c: Optional[float]
    """Minimum apparent temperature, °C."""
    rain_mm: Optional[float]
    """Rain from large-scale weather systems, mm. Showers are not included here; precipitation_mm counts rain, showers and snow."""
    snowfall_cm: Optional[float]
    """Snowfall, cm."""
    precipitation_hours: Optional[float]
    """Hours with precipitation."""
    wind_gusts_kmh: Optional[float]
    """Maximum wind gusts, km/h."""
    wind_direction_deg: Optional[float]
    """Dominant wind direction, degrees."""
    uv_index_max: Optional[float]
    """Maximum UV index."""
    sunshine_hours: Optional[float]
    """Hours of sunshine."""
    sunrise: Optional[str]
    """Sunrise, local time of the place."""
    sunset: Optional[str]
    """Sunset, local time of the place."""
    region: Optional[str]
    """First-level administrative region of the geocoded place."""
    country_code: Optional[str]
    """ISO country code of the geocoded place."""
    elevation_m: Optional[float]
    """Elevation of the forecast grid cell, metres."""
    timezone: Optional[str]
    """IANA timezone of the place."""

class WikipediaArticlesRow(TypedDict, total=False):
    """One row of `public-data wikipedia` (wikipedia_articles v1.1.1)."""

    rank: int
    """1-based position."""
    title: str
    """Article title."""
    page_id: Optional[int]
    """MediaWiki page id."""
    description: Optional[str]
    """Short description (Wikidata)."""
    extract: str
    """Lead-section plain-text extract."""
    url: str
    """Canonical article URL."""
    thumbnail: Optional[str]
    """Lead image thumbnail."""
    lang: str
    """Language edition read."""
    last_modified: Optional[str]
    """Last revision time (ISO 8601)."""
    wikidata_id: Optional[str]
    """Wikidata item id (Q…)."""
    image: Optional[str]
    """Full-size lead image."""
    revision_id: Optional[int]
    """Revision id of the summary."""
    page_type: Optional[str]
    """standard, disambiguation…"""
    latitude: Optional[float]
    """Latitude, for places."""
    longitude: Optional[float]
    """Longitude, for places."""
    word_count: Optional[int]
    """Article length in words (search runs)."""

class WikidataRow(TypedDict, total=False):
    """One row of `public-data wikidata` (wikidata v1.1.0)."""

    rank: int
    """1-based relevance rank."""
    id: str
    """Wikidata entity id (Q…)."""
    label: Optional[str]
    """Entity label."""
    description: Optional[str]
    """Short description."""
    concept_uri: Optional[str]
    """Canonical entity URI (join key)."""
    url: str
    """Wikidata page URL."""
    matched: Optional[str]
    """The text that matched the query."""
    match_type: Optional[str]
    """How it matched (label, alias…)."""
    aliases: List[str]
    """Alternative names in the requested language and English."""
    wikipedia_url: Optional[str]
    """Wikipedia article in the requested language (English as fallback)."""
    wikipedia_title: Optional[str]
    """Title of that article."""
    instance_of: Optional[List[str]]
    """Q-ids the entity is an instance of (include_details)."""
    country_id: Optional[str]
    """Q-id of the entity's country (include_details)."""
    official_website: Optional[str]
    """Official website (include_details)."""
    latitude: Optional[float]
    """Latitude (include_details)."""
    longitude: Optional[float]
    """Longitude (include_details)."""
    image_url: Optional[str]
    """Wikimedia Commons image (include_details)."""

class OpenlibraryBooksRow(TypedDict, total=False):
    """One row of `public-data books` (openlibrary_books v1.1.1)."""

    rank: int
    """1-based position."""
    title: str
    """Title."""
    authors: List[str]
    """Authors (up to 5)."""
    first_publish_year: Optional[int]
    """First publication year."""
    isbn: Optional[str]
    """ISBN (13 preferred)."""
    publishers: List[str]
    """Publishers (up to 3)."""
    languages: List[str]
    """Language codes of the editions, all of them."""
    pages: Optional[int]
    """Median page count."""
    rating: Optional[float]
    """Community rating (0-5)."""
    ratings_count: Optional[int]
    """Number of ratings."""
    editions: Optional[int]
    """Edition count."""
    cover_url: Optional[str]
    """Cover image."""
    url: str
    """Open Library page."""
    subtitle: Optional[str]
    """Subtitle."""
    work_id: str
    """Open Library work id (OL…W)."""
    want_to_read_count: Optional[int]
    """Readers who shelved it as want-to-read."""
    already_read_count: Optional[int]
    """Readers who shelved it as read."""
    subjects: List[str]
    """Subjects (up to 10)."""
    author_ids: List[str]
    """Open Library author ids."""
    ebook_access: Optional[str]
    """public, borrowable, printdisabled or no_ebook."""
    read_url: Optional[str]
    """Internet Archive page of the readable/borrowable copy."""
    cover_url_large: Optional[str]
    """Large cover image."""

class NvdCveRow(TypedDict, total=False):
    """One row of `public-data cve` (nvd_cve v1.1.0)."""

    rank: int
    """1-based position."""
    cve_id: str
    """CVE identifier."""
    description: Optional[str]
    """English description."""
    cvss_score: Optional[float]
    """CVSS base score."""
    severity: Optional[str]
    """CVSS severity."""
    cvss_vector: Optional[str]
    """CVSS vector string."""
    cwe: List[str]
    """CWE weakness ids."""
    published: Optional[str]
    """Publish date."""
    last_modified: Optional[str]
    """Last modified date."""
    status: Optional[str]
    """Vulnerability status."""
    references: List[str]
    """Reference URLs."""
    url: str
    """NVD detail page."""
    cvss_version: Optional[str]
    """CVSS version of the score."""
    exploitability_score: Optional[float]
    """CVSS exploitability sub-score."""
    impact_score: Optional[float]
    """CVSS impact sub-score."""
    attack_vector: Optional[str]
    """Attack vector (NETWORK, LOCAL…)."""
    affected_products: List[str]
    """Vulnerable vendor:product pairs from the CPE configurations."""
    source: Optional[str]
    """Organisation that assigned the CVE."""
    known_exploited: bool
    """In the CISA Known Exploited Vulnerabilities catalog."""
    kev_added: Optional[str]
    """Date added to the CISA KEV catalog."""
    kev_due_date: Optional[str]
    """CISA remediation due date."""
    kev_required_action: Optional[str]
    """CISA required action."""
    patch_urls: List[str]
    """References tagged Patch or Vendor Advisory."""
