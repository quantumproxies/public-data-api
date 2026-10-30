"""Public Data API: Public data API for Python and the command line: arXiv and OpenAlex papers, clinical trials, openFDA adverse events, World Bank indicators, weather, Wikipedia, Wikidata, Open Library books and NVD CVEs in one client, with one sign-in and the same JSON or CSV rows. Free and open source; runs on your QuanticData account.

    from quanticdata_public_data_api import OpenData

    scraper = OpenData()   # saved login (`public-data login`) or QUANTICDATA_API_KEY
    run = scraper.arxiv(...)   # arXiv preprint search
    run = scraper.papers(...)   # scholarly works from OpenAlex
    run = scraper.trials(...)   # ClinicalTrials.gov studies
    run = scraper.fda(...)   # FDA adverse-event reports from openFDA
    run = scraper.worldbank(...)   # World Bank indicators per country and year
    run = scraper.weather(...)   # daily weather forecast and recent history by place
    run = scraper.wikipedia(...)   # Wikipedia article summaries by search or title
    run = scraper.wikidata(...)   # Wikidata entities for a name
    run = scraper.books(...)   # Open Library book search
    run = scraper.cve(...)   # CVE records from the NIST NVD
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["OpenData", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class OpenData:
    """Public Data API on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="public-data/0.1.0 (+https://github.com/quantumproxies/public-data-api)", timeout=timeout)

    def arxiv(
        self, query: str,
        *,
        category: Optional[str] = None,
        sort: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Preprint search on arXiv — abstracts, authors, categories and PDF links.

        Args:
            query: Free text, e.g. "retrieval augmented generation", or arXiv field syntax such as ti:diffusion.
            category: Subject class, e.g. cs.AI, cs.CL or stat.ML.
            sort: Result order. One of: relevance, latest, updated.
            max_results: How many papers to deliver at most (1–100). You pay only for delivered papers.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per paper: see ``types.ArxivPapersRow``.
        """
        payload = {
            "query": query,
            "category": category,
            "sort": sort,
            "max_results": max_results,
        }
        return self.client.run_collector("arxiv_papers", payload, wait=wait, timeout=timeout)

    def papers(
        self, query: str,
        *,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        open_access: Optional[bool] = None,
        sort: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Scholarly works from OpenAlex: title, authors, year, citations, DOI, venue, open-access link, abstract, topic and institutions.

        Args:
            query: Search terms across title, abstract and metadata.
            year_from: Only works published this year or later.
            year_to: Only works published up to this year.
            open_access: Only works with a free full text.
            sort: relevance (default), cited (most cited first) or newest. One of: relevance, cited, newest.
            max_results: How many works to deliver at most (1–200). You pay only for delivered works.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 200 rows, one per work: see ``types.OpenalexRow``.
        """
        payload = {
            "query": query,
            "year_from": year_from,
            "year_to": year_to,
            "open_access": open_access,
            "sort": sort,
            "max_results": max_results,
        }
        return self.client.run_collector("openalex", payload, wait=wait, timeout=timeout)

    def trials(
        self, query: Optional[str] = None,
        *,
        condition: Optional[str] = None,
        status: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Studies from ClinicalTrials.gov — status, phase, conditions, interventions, sponsor.

        Args:
            query: Free-text search term: a drug, disease or sponsor, e.g. "cancer immunotherapy".
            condition: Restrict to a medical condition.
            status: Recruitment status filter. One of: RECRUITING, NOT_YET_RECRUITING, ACTIVE_NOT_RECRUITING, COMPLETED, ENROLLING_BY_INVITATION, SUSPENDED, TERMINATED, WITHDRAWN.
            max_results: How many studies to deliver at most (1–200). You pay only for delivered studies.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 200 rows, one per study: see ``types.ClinicalTrialsRow``.
        """
        payload = {
            "query": query,
            "condition": condition,
            "status": status,
            "max_results": max_results,
        }
        return self.client.run_collector("clinical_trials", payload, wait=wait, timeout=timeout)

    def fda(
        self, query: str,
        *,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Drug adverse-event reports from the FDA FAERS database — drugs, reactions, seriousness.

        Args:
            query: A drug name, e.g. ibuprofen, or an openFDA field:value query.
            max_results: How many reports to deliver at most (1–500). You pay only for delivered reports.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 500 rows, one per report: see ``types.OpenfdaRow``.
        """
        payload = {
            "query": query,
            "max_results": max_results,
        }
        return self.client.run_collector("openfda", payload, wait=wait, timeout=timeout)

    def worldbank(
        self, indicator: str,
        *,
        countries: Union[str, Sequence[str]],
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        include_empty: Optional[bool] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """World Bank development indicators per country and year, by indicator code: GDP, population, inflation and the rest of the World Bank catalog.

        Args:
            indicator: World Bank indicator code, e.g. NY.GDP.MKTP.CD (GDP in current US$) or SP.POP.TOTL (population).
            countries: Country codes, ISO2 or ISO3, e.g. IT DE, or WLD for the world.
            year_from: First year (default: all).
            year_to: Last year (default: latest).
            include_empty: Keep rows whose value is null.
            max_results: How many datapoints to deliver at most (1–200). You pay only for delivered datapoints.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 200 rows, one per datapoint: see ``types.WorldBankRow``.
        """
        payload = {
            "indicator": indicator,
            "countries": _as_list(countries),
            "year_from": year_from,
            "year_to": year_to,
            "include_empty": include_empty,
            "max_results": max_results,
        }
        return self.client.run_collector("world_bank", payload, wait=wait, timeout=timeout)

    def weather(
        self, location: Optional[str] = None,
        *,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        days: Optional[int] = None,
        past_days: Optional[int] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Daily weather for a place name or coordinates, from Open-Meteo: conditions, temperatures, precipitation, wind, UV, sunshine, sunrise and sunset, up to 16 days ahead and 92 days back.

        Args:
            location: City or place name, e.g. Rome.
            latitude: Exact latitude (skips geocoding).
            longitude: Exact longitude.
            days: Days ahead, 1 to 16 (default 7).
            past_days: Days of recent history to add before the forecast, 0 to 92 (default 0).
            max_results: How many days to deliver at most (1–30). You pay only for delivered days.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 30 rows, one per day: see ``types.WeatherForecastRow``.
        """
        payload = {
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "days": days,
            "past_days": past_days,
            "max_results": max_results,
        }
        return self.client.run_collector("weather_forecast", payload, wait=wait, timeout=timeout)

    def wikipedia(
        self, query: Optional[str] = None,
        *,
        titles: Optional[Union[str, Sequence[str]]] = None,
        lang: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Wikipedia article summaries, by search query or exact titles, in any language edition: lead extract, short description, images, Wikidata id, coordinates and last edit.

        Args:
            query: Search Wikipedia and read the top results, e.g. "web scraping". Use this or --titles.
            titles: Exact article titles or /wiki/ URLs to read, e.g. "Web scraping". Use this or QUERY.
            lang: Wikipedia language edition (en, it, de…). Default en.
            max_results: How many articles to deliver at most (1–50). You pay only for delivered articles.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per article: see ``types.WikipediaArticlesRow``.
        """
        payload = {
            "query": query,
            "titles": _as_list(titles),
            "lang": lang,
            "max_results": max_results,
        }
        return self.client.run_collector("wikipedia_articles", payload, wait=wait, timeout=timeout)

    def wikidata(
        self, query: str,
        *,
        lang: Optional[str] = None,
        include_details: Optional[bool] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Resolve a name to a stable Wikidata entity id — the join key for entity linking.

        Args:
            query: Name or term to resolve, e.g. "Leonardo da Vinci".
            lang: Language for labels/descriptions (default en).
            include_details: Also read instance-of, country, official website, coordinates and image for each entity.
            max_results: How many entities to deliver at most (1–50). You pay only for delivered entities.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per entity: see ``types.WikidataRow``.
        """
        payload = {
            "query": query,
            "lang": lang,
            "include_details": include_details,
            "max_results": max_results,
        }
        return self.client.run_collector("wikidata", payload, wait=wait, timeout=timeout)

    def books(
        self, query: str,
        *,
        sort: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Book search over the Open Library catalog — ISBN, authors, ratings, covers.

        Args:
            query: Title or author words, e.g. "dune herbert", or author:, isbn:, subject: syntax.
            sort: Result order. One of: relevance, new, old, rating.
            max_results: How many books to deliver at most (1–100). You pay only for delivered books.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per book: see ``types.OpenlibraryBooksRow``.
        """
        payload = {
            "query": query,
            "sort": sort,
            "max_results": max_results,
        }
        return self.client.run_collector("openlibrary_books", payload, wait=wait, timeout=timeout)

    def cve(
        self, keyword: Optional[str] = None,
        *,
        severity: Optional[str] = None,
        cve_id: Optional[str] = None,
        known_exploited: Optional[bool] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Vulnerabilities from the NIST NVD — CVE id, description, CVSS score, severity, CWE.

        Args:
            keyword: Search term: a product, vendor or words of the CVE text, e.g. log4j.
            severity: Filter to a CVSS v3 severity. One of: LOW, MEDIUM, HIGH, CRITICAL.
            cve_id: Look up one CVE, e.g. CVE-2021-44228.
            known_exploited: Only CVEs in the CISA Known Exploited Vulnerabilities catalog.
            max_results: How many CVEs to deliver at most (1–200). You pay only for delivered CVEs.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 200 rows, one per CVE: see ``types.NvdCveRow``.
        """
        payload = {
            "keyword": keyword,
            "severity": severity,
            "cve_id": cve_id,
            "known_exploited": known_exploited,
            "max_results": max_results,
        }
        return self.client.run_collector("nvd_cve", payload, wait=wait, timeout=timeout)
