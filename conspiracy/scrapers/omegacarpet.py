from conspiracy.scraper import Scraper
from bs4 import BeautifulSoup
import re
import requests


def sanitize_name(str):
    return str.lower().strip().replace("-", "_").replace(" ", "_")


def image_url_from_href(url):
    match = re.search(r"/recolor_carpet/(\d+)/", url)
    if match:
        return f"https://www.omegapatternworks.com/replace_colors/{match.group(1)}/?from=&to=&cnt=undefined"


class OmegaCarpetScraper(Scraper):
    """Scraper for carpet textures from Omega Pattern Works
    https://www.omegapatternworks.com/
    """
    scraper_name = "omega"

    def __init__(self):
        self._urls_cache = []
        super()

    def scrape_page(self, page):
        page_url = f"https://omegapatternworks.com/categories/?page={page}"

        resp = requests.get(page_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        for div in soup.find_all("div", class_="carpet_preview"):
            url = image_url_from_href(div.find("a").get("href"))
            if not url:
                continue

            title_element = div.find("p", class_="carpet_name")
            name = sanitize_name(title_element.text) + ".png"
            self._urls_cache.append((url, name))

        # Scrape next page if we need to
        next_page_button = soup.find("a", text="›")
        if next_page_button and not ("disabled" in next_page_button.get("class", [])):
            self.scrape_page(page + 1)

    def build_url_list(self):
        self.scrape_page(1)
        return self._urls_cache


if __name__ == "__main__":
    scraper = OmegaCarpetScraper()
    scraper.run()
