"""Known exploited vulnerabilities for the products you run.

    python kev_check.py nginx openssl "apache http server" --out kev.csv

For each product keyword it asks the NIST NVD for the CVEs that are in the
CISA Known Exploited Vulnerabilities catalog and writes one row per CVE: the
keywords that matched, severity, CVSS score, the date CISA added it, the
remediation due date, the required action and the patch links. Newest
additions first.
"""

import argparse

from quanticdata_public_data_api import OpenData, write

FIELDS = ["cve_id", "severity", "cvss_score", "published", "kev_added", "kev_due_date", "kev_required_action",
          "affected_products", "patch_urls", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keywords", nargs="+", help="product or vendor names, e.g. nginx openssl")
    parser.add_argument("--severity", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"], help="only this CVSS v3 severity")
    parser.add_argument("--top", type=int, default=100, help="CVEs per keyword (max 200)")
    parser.add_argument("--out", default="kev.csv")
    args = parser.parse_args()

    data = OpenData()
    found = {}
    for keyword in args.keywords:
        run = data.cve(keyword, severity=args.severity, known_exploited=True, max_results=args.top)
        print(f"{keyword!r}: {len(run)} known exploited CVEs")
        for c in run:
            row = found.setdefault(c["cve_id"], {"matched": [], **{field: c.get(field) for field in FIELDS}})
            row["matched"].append(keyword)

    rows = sorted(found.values(), key=lambda r: r["kev_added"] or "", reverse=True)
    write(rows, args.out)
    print(f"{len(rows)} CVEs written to {args.out}")


if __name__ == "__main__":
    main()
