from conspiracy.scraper import Scraper
from bs4 import BeautifulSoup
import re
import requests


def sanitize_name(str):
    return str.lower().replace("-", "_").replace(" ", "_")


def image_url_from_href(url):
    match = re.search(r"/recolor_carpet/(\d+)/", url)
    if match:
        return f"https://astrocarpetmills.com/replace_colors/{match.group(1)}/?from=&to=&cnt=undefined"


class AstroCarpetScraper(Scraper):
    scraper_name = "astro"

    def __init__(self):
        self._urls_cache = []
        super()

    def scrape_page(self, page):
        page_url = f"https://astrocarpetmills.com/categories/?page={page}"

        resp = requests.get(page_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        for div in soup.find_all("div", class_="carpet_preview"):
            url = image_url_from_href(div.find("a").get("href"))
            if not url:
                continue
            name = sanitize_name(div.find("h3").text) + ".png"
            self._urls_cache.append((url, name))

        # Scrape next page if we need to
        next_page_button = soup.find("a", text="›")
        if next_page_button and not ("disabled" in next_page_button.get("class", [])):
            self.scrape_page(page + 1)

    def build_url_list(self):
        self.scrape_page(1)
        return self._urls_cache


if __name__ == "__main__":
    scraper = AstroCarpetScraper()
    scraper.run()
