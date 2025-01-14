"""
  MOTD script that scrapes the Billboard Hot Ten and outputs them to your terminal.
  but-i-am-dominator
  https://github.com/but-i-am-dominator

"""

#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

# CSS Selectors for Billboard Chart Items
tag_0: str = "#post-1479786 > div.pmc-paywall > div > div > div > div.chart-result"
tag_1: str = "s-list.\/\/.lrv-u-padding-t-150.lrv-u-padding-t-050\@mobile-max > div" 
tag_2: str = ":nth-child("
tag_3: str = ") > ul > li.lrv-u-width-100p > ul > li.o-chart-results-list__item.\/"
tag_4: str = "\/.lrv-u-flex-grow-1.lrv-u-flex.lrv-u-flex-direction-column.lrv-u-ju"
tag_5: str = "stify-content-center.lrv-u-border-b-1.u-border-b-0\@mobile-max."
later_1: str = "lrv-u-border-color-grey-light.lrv-u-padding-l-050.lrv-u-padding-l-1"
later_2: str = "\@mobile-max"
top: str = "lrv-u-border-color-grey-light.lrv-u-padding-l-1\@mobile-max"

the_hits: list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]


def fetch_page() -> BeautifulSoup:
    """Fetch the HTML content of billboard.com."""
    try:
        response = requests.get("https://www.billboard.com/charts/hot-100/")
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None


def print_hit(soup: BeautifulSoup, hit_index: str) -> str:
    """Transforms scraped data. Returns artist and song for the place 
    identified in the top ten."""
    if hit_index == "2":
        hit_index = tag_0 + tag_1 + tag_2 + hit_index + tag_3 + tag_4 + tag_5 + top
    else:
        hit_index = tag_0 + tag_1 + tag_2 + hit_index+ tag_3 + tag_4 + tag_5 + later_1 + later_2
    hit_index = soup.select(hit_index)
    my_list = hit_index[0].text.replace("\n", "").split("\t")
    cleaned_list = [item for item in my_list if item]
    return f"{cleaned_list[0]} | {cleaned_list[1]}"


def print_header() -> None:
    """Format output for MOTD."""
    print(36* "*")
    print("The Billboard Top Ten for Today")
    print(36 * "*" + "\n")


def main() -> None:
    """Main function."""
    soup = fetch_page()
    count = 1
    print_header()
    for hit_index in the_hits:
        num = str(count) + " " if count < 10 else str(count)
        print(f"Number {num}: | {print_hit(soup, hit_index)}")
        count = count + 1
    print("\n" + 36 * "*" + "\n")

# Welcome to the party pal!
if __name__ == "__main__":
    main()
