"""World Bank indicators for a set of countries, one row per country and year.

    python country_indicators.py --countries IT DE FR ES --indicators NY.GDP.MKTP.CD SP.POP.TOTL --since 2015

Each indicator code becomes a column, so the CSV reads as a panel: country,
country code, year, then one value per indicator. Years with no value stay
empty.
"""

import argparse

from quanticdata_public_data_api import OpenData, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--countries", nargs="+", required=True, help="ISO2 or ISO3 codes, e.g. IT DE or WLD")
    parser.add_argument("--indicators", nargs="+", required=True, help="World Bank codes, e.g. NY.GDP.MKTP.CD")
    parser.add_argument("--since", type=int, default=2000, help="first year (default 2000)")
    parser.add_argument("--out", default="indicators.csv")
    args = parser.parse_args()

    data = OpenData()
    table = {}
    # One run per indicator and country keeps each run well under its 200 datapoints.
    for code in args.indicators:
        for country in args.countries:
            run = data.worldbank(code, countries=[country], year_from=args.since, max_results=200)
            for point in run:
                key = (point["country_code"], point["year"])
                row = table.setdefault(key, {"country": point["country"], "country_code": point["country_code"],
                                             "year": point["year"], **{c: None for c in args.indicators}})
                row[code] = point["value"]
            print(f"{code} {country}: {len(run)} datapoints")

    rows = sorted(table.values(), key=lambda r: (r["country_code"] or "", r["year"] or ""))
    write(rows, args.out)
    print(f"{len(rows)} country-years written to {args.out}")


if __name__ == "__main__":
    main()
