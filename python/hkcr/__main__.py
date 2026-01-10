#!/usr/bin/env python3
"""CLI entry point for hkcr."""
import argparse
import json
import sys
from dataclasses import asdict
from .api import search_local, search_foreign
from .types import SearchOptions

def truncate(s: str, length: int) -> str:
    if not s:
        return ""
    return s[:length-1] + "…" if len(s) > length else s

def format_local_table(companies) -> str:
    if not companies:
        return "No results found."
    cols = [
        ("brn", "BRN", 12),
        ("english_name", "English Name", 40),
        ("chinese_name", "Chinese Name", 20),
        ("company_type", "Type", 20),
        ("date_of_incorporation", "Incorporated", 12),
    ]
    header = " │ ".join(h.ljust(w) for _, h, w in cols)
    divider = "─┼─".join("─" * w for _, _, w in cols)
    rows = []
    for co in companies:
        row = " │ ".join(truncate(getattr(co, k) or "", w).ljust(w) for k, _, w in cols)
        rows.append(row)
    return "\n".join([header, divider] + rows)

def format_foreign_table(companies) -> str:
    if not companies:
        return "No results found."
    cols = [
        ("brn", "BRN", 12),
        ("corporate_name", "Corporate Name", 35),
        ("hk_name", "HK Name", 25),
        ("place_of_incorporation", "Origin", 15),
        ("date_of_registration", "Registered", 12),
    ]
    header = " │ ".join(h.ljust(w) for _, h, w in cols)
    divider = "─┼─".join("─" * w for _, _, w in cols)
    rows = []
    for co in companies:
        row = " │ ".join(truncate(getattr(co, k) or "", w).ljust(w) for k, _, w in cols)
        rows.append(row)
    return "\n".join([header, divider] + rows)

def main():
    parser = argparse.ArgumentParser(
        prog="hkcr",
        description="Hong Kong Companies Registry Search",
    )
    parser.add_argument("query", help="Search query (company name or BRN)")
    parser.add_argument("-f", "--foreign", action="store_true", help="Search non-HK companies")
    parser.add_argument("-b", "--brn", action="store_true", help="Search by BRN")
    parser.add_argument("-e", "--exact", action="store_true", help="Exact match")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    options = SearchOptions(by_brn=args.brn, exact=args.exact)

    try:
        if args.foreign:
            results = search_foreign(args.query, options)
            if args.json:
                print(json.dumps([asdict(r) for r in results], indent=2, ensure_ascii=False))
            else:
                print(format_foreign_table(results))
        else:
            results = search_local(args.query, options)
            if args.json:
                print(json.dumps([asdict(r) for r in results], indent=2, ensure_ascii=False))
            else:
                print(format_local_table(results))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
