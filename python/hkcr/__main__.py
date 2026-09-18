#!/usr/bin/env python3
"""CLI entry point for hkcr."""

import argparse
import json
import sys
import unicodedata
from dataclasses import asdict

from .api import search_local, search_foreign
from .types import SearchOptions


def display_width(text: str) -> int:
    """Return the terminal display width of Unicode text."""
    return sum(
        2 if unicodedata.east_asian_width(char) in "WF" else 1
        for char in text
    )


def pad(text: str, width: int) -> str:
    """Pad text to a terminal display width."""
    return text + " " * max(0, width - display_width(text))


def _split_to_width(text: str, width: int) -> list[str]:
    """Split text into terminal-width-safe chunks."""
    chunks = []
    current = ""
    current_width = 0

    for char in text:
        char_width = display_width(char)

        if current and current_width + char_width > width:
            chunks.append(current)
            current = ""
            current_width = 0

        current += char
        current_width += char_width

    if current or not chunks:
        chunks.append(current)

    return chunks


def wrap_text(s: str, width: int) -> list[str]:
    """Wrap text according to terminal display width."""
    if not s:
        return [""]

    lines = []
    current = ""

    for word in s.split():
        candidate = word if not current else f"{current} {word}"

        if display_width(candidate) <= width:
            current = candidate
            continue

        if current:
            lines.append(current)
            current = ""

        if display_width(word) <= width:
            current = word
        else:
            chunks = _split_to_width(word, width)
            lines.extend(chunks[:-1])
            current = chunks[-1]

    if current or not lines:
        lines.append(current)

    return lines


def format_local_table(companies) -> str:
    if not companies:
        return "No results found."

    cols = [
        ("brn", "BRN", 10),
        ("english_name", "English Name", 30),
        ("chinese_name", "Chinese Name", 16),
        ("company_type", "Type", 18),
        ("date_of_incorporation", "Incorporated", 12),
    ]

    header = " │ ".join(pad(h, w) for _, h, w in cols)
    divider = "─┼─".join("─" * w for _, _, w in cols)

    rows = []

    for company in companies:
        wrapped = [
            wrap_text(getattr(company, key) or "", width)
            for key, _, width in cols
        ]

        max_lines = max(len(value) for value in wrapped)

        for index in range(max_lines):
            row_parts = []

            for column_index, (_, _, width) in enumerate(cols):
                line = (
                    wrapped[column_index][index]
                    if index < len(wrapped[column_index])
                    else ""
                )
                row_parts.append(pad(line, width))

            rows.append(" │ ".join(row_parts))

    return "\n".join([header, divider] + rows)


def format_foreign_table(companies) -> str:
    if not companies:
        return "No results found."

    cols = [
        ("brn", "BRN", 10),
        ("corporate_name", "Corporate Name", 30),
        ("hk_name", "HK Name", 20),
        ("place_of_incorporation", "Origin", 12),
        ("date_of_registration", "Registered", 12),
    ]

    header = " │ ".join(pad(h, w) for _, h, w in cols)
    divider = "─┼─".join("─" * w for _, _, w in cols)

    rows = []

    for company in companies:
        wrapped = [
            wrap_text(getattr(company, key) or "", width)
            for key, _, width in cols
        ]

        max_lines = max(len(value) for value in wrapped)

        for index in range(max_lines):
            row_parts = []

            for column_index, (_, _, width) in enumerate(cols):
                line = (
                    wrapped[column_index][index]
                    if index < len(wrapped[column_index])
                    else ""
                )
                row_parts.append(pad(line, width))

            rows.append(" │ ".join(row_parts))

    return "\n".join([header, divider] + rows)


def main():
    parser = argparse.ArgumentParser(
        prog="hkcr",
        description="Hong Kong Companies Registry Search",
    )

    parser.add_argument(
        "query",
        help="Search query (company name or BRN)",
    )
    parser.add_argument(
        "-f",
        "--foreign",
        action="store_true",
        help="Search non-HK companies",
    )
    parser.add_argument(
        "-b",
        "--brn",
        action="store_true",
        help="Search by BRN",
    )
    parser.add_argument(
        "-e",
        "--exact",
        action="store_true",
        help="Exact match",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    options = SearchOptions(
        by_brn=args.brn,
        exact=args.exact,
    )

    try:
        if args.foreign:
            results = search_foreign(args.query, options)

            if args.json:
                print(
                    json.dumps(
                        [asdict(result) for result in results],
                        indent=2,
                        ensure_ascii=False,
                    )
                )
            else:
                print(format_foreign_table(results))
        else:
            results = search_local(args.query, options)

            if args.json:
                print(
                    json.dumps(
                        [asdict(result) for result in results],
                        indent=2,
                        ensure_ascii=False,
                    )
                )
            else:
                print(format_local_table(results))

    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
