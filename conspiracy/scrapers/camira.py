from conspiracy.scraper import Scraper
from bs4 import BeautifulSoup
import json
import requests


class CamiraFabricsScraper(Scraper):
    """Scraper for camira's range of Bus & Coach fabrics
    https://www.camirafabrics.com/en/fabrics/bus-and-coach
    """
    scraper_name = "camira"
    root_url = "https://www.camirafabrics.com/"

    @staticmethod
    def url_and_name_for_colourway(colourway: dict):
        title = colourway["title"].replace(": ", "_").replace(" ", "_")
        sku = colourway["sku"].replace(": ", "_").replace(" ", "_")
        name = title + sku + ".png"
        name = name.lower()

        # Images are specified in srcset format, we're pretty safe to take the first in the list
        srcset = colourway["image"]
        url = srcset.split(" ")[0]

        # Bump up the width parameter so we get super high-res images
        url = url.replace("width=320", "width=2048")
        return (CamiraFabricsScraper.root_url + url, name)

    @staticmethod
    def items_in_category(category_url: str):
        full_url = CamiraFabricsScraper.root_url + category_url
        resp = requests.get(full_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        # nothing in life is ever easy, huh?
        base_container = soup.find("div", id="productColourways")
        colourways_data = json.loads(base_container.get("data-dc-colourways-options"))

        options = colourways_data["colourways"]
        return [CamiraFabricsScraper.url_and_name_for_colourway(option) for option in options]

    @staticmethod
    def get_categories():
        base_url = CamiraFabricsScraper.root_url + "/api/category-results/buscoach?page=1"
        resp = requests.get(base_url)

        # This endpoint returns something like "{}"
        # So we need to 'double decode' the json
        data = resp.json()
        data = json.loads(data)
        return [category["url"] for category in data["items"]]

    def build_url_list(self):
        categories = self.get_categories()
        all_items = [item for cat in categories for item in self.items_in_category(cat)]
        return all_items


if __name__ == "__main__":
    scraper = CamiraFabricsScraper()
    scraper.run()
