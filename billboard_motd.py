"""
  MOTD script that scrapes the Billboard Hot Ten and outputs them to your terminal.
  but-i-am-dominator
  https://github.com/but-i-am-dominator

"""

#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import sys


BILLBOARD_HOT_100_URL = "https://www.billboard.com/charts/hot-100/"


def print_header() -> None:
    """Format output for MOTD."""
    print(36* "*")
    print("The Billboard Top Ten for Today")
    print(36 * "*" + "\n")


def fetch_page_html(url: str) -> str:
    """
    Fetch the HTML for a URL, using a desktop browser User-Agent.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.text


def parse_hot_100(html: str) -> List[Dict[str, str]]:
    """Parse the Billboard Hot 100 HTML and return a list of rows with
    ``{"rank", "title", "artist"}``.

    This implementation is tailored to the current Billboard markup, where
    each chart row looks roughly like:

    <div class="o-chart-results-list-row-container">
        <ul class="o-chart-results-list-row ...">
            <li class="o-chart-results-list__item ...">  # rank
                <span class="c-label ...">1</span>
            </li>
            <li class="o-chart-results-list__item ...">  # artwork
                ...
            </li>
            <li class="o-chart-results-list__item ...">  # title / artist
                <h3 id="title-of-a-story" class="c-title ...">Song Title</h3>
                <span class="c-label ...">
                    <a href="/artist/...">Artist Name</a>
                </span>
            </li>
            ... other list items with LW / PEAK / WEEKS ...
        </ul>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    # Each logical chart row is a <ul> with class "o-chart-results-list-row"
    # inside a container div.
    rows = soup.select("div.o-chart-results-list-row-container > ul.o-chart-results-list-row")

    chart_data: List[Dict[str, str]] = []

    for row in rows:
        # Rank: first "rank" item in the row (a li with a numeric c-label).
        rank_el = None
        for li in row.select("li.o-chart-results-list__item"):
            span = li.select_one("span.c-label")
            if not span:
                continue
            text = span.get_text(strip=True)
            if text.isdigit():
                rank_el = span
                break

        if not rank_el:
            continue

        rank_text = rank_el.get_text(strip=True)
        if not rank_text.isdigit():
            # Skip non-numeric ranks just in case.
            continue

        # Title: main song title is in an <h3> with id="title-of-a-story".
        title_el = row.select_one("h3#title-of-a-story") or row.select_one("h3.c-title")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)

        # Artist: the primary artist link lives inside a span.c-label under the
        # title block. Prefer an <a> whose href contains "/artist/".
        artist = ""
        artist_link = row.select_one("span.c-label a[href*='/artist/']")
        if artist_link:
            artist = artist_link.get_text(strip=True)
        else:
            # Fallback: any non-numeric c-label text near the title.
            for span in row.select("span.c-label"):
                text = span.get_text(strip=True)
                # Normalize whitespace and case for comparison
                normalized = " ".join(text.split()).lower()
                compact = normalized.replace(" ", "")  # handles "RE-\nENTRY" -> "re-entry"

                non_artist_markers = {
                    "lw",       # last week position label
                    "peak",     # peak position label
                    "weeks",    # weeks on chart label
                    "new",      # new entry label
                    "re-entry", # re-entry label
                    "reentry",  # just in case markup omits the hyphen
                    "re-peak",  # re-peak label
                }

                if not text or text.isdigit():
                    continue

                # If, after removing spaces, the text matches a known non-artist marker,
                # skip it. This catches variants like "RE- ENTRY" or "RE-\nENTRY".
                if compact in non_artist_markers:
                    continue

                artist = text
                break

        chart_data.append({"rank": rank_text, "title": title, "artist": artist})

    # Keep only rows where rank is numeric and within top 100
    cleaned: List[Dict[str, str]] = []
    for row in chart_data:
        try:
            r = int(row["rank"])
        except ValueError:
            continue
        if 1 <= r <= 100:
            cleaned.append(row)

    # Sort by rank just in case
    cleaned.sort(key=lambda x: int(x["rank"]))

    return cleaned

def main():
    try:
        html = fetch_page_html(BILLBOARD_HOT_100_URL)
    except requests.HTTPError as e:
        print(f"HTTP error fetching Billboard page: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Network error fetching Billboard page: {e}", file=sys.stderr)
        sys.exit(1)

    rows = parse_hot_100(html)

    if not rows:
        print(
            "No rows were parsed. Billboard may have changed their HTML structure; "
            "inspect the page source and adjust the CSS selectors in parse_hot_100().",
            file=sys.stderr,
        )
        sys.exit(1)

    print_header()

    for hit in rows:
        print(f"Number {hit['rank']}: | {hit['title']} | {hit['artist']}")
    print("\n" + 36 * "*" + "\n")
    


# Welcome to the party pal!
if __name__ == "__main__":
    main()
