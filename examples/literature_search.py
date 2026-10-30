"""Papers on a topic from arXiv and OpenAlex, in one CSV.

    python literature_search.py "retrieval augmented generation" --since 2023 --top 50

arXiv gives the newest preprints, OpenAlex the most cited published works.
Each row keeps its source, year, title, authors, DOI, citation count (OpenAlex
only), venue and links, so the list can be sorted and deduplicated in a
spreadsheet.
"""

import argparse

from quanticdata_public_data_api import OpenData, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("topic")
    parser.add_argument("--since", type=int, help="OpenAlex: only works published this year or later")
    parser.add_argument("--top", type=int, default=25, help="results per source (max 100)")
    parser.add_argument("--out", default="literature.csv")
    args = parser.parse_args()

    data = OpenData()
    rows = []
    for p in data.arxiv(args.topic, sort="latest", max_results=args.top):
        rows.append({"source": "arxiv", "year": int(p["published"][:4]) if p["published"] else None,
                     "title": p["title"], "authors": p["authors"], "doi": p["doi"], "cited_by": None,
                     "venue": p["journal_ref"], "url": p["url"], "pdf_url": p["pdf_url"]})
    for w in data.papers(args.topic, year_from=args.since, sort="cited", max_results=args.top):
        rows.append({"source": "openalex", "year": w["year"], "title": w["title"], "authors": w["authors"],
                     "doi": w["doi"], "cited_by": w["cited_by_count"], "venue": w["venue"], "url": w["url"],
                     "pdf_url": w["pdf_url"] or w["oa_url"]})

    write(rows, args.out)
    print(f"{len(rows)} papers on {args.topic!r} written to {args.out}")


if __name__ == "__main__":
    main()
