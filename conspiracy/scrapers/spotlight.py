from conspiracy.scraper import Scraper
from bs4 import BeautifulSoup
import requests


def sanitize_name(str):
    return str.replace("/", " ").replace("\\", " ").replace(",", "")


class SpotlightScraper(Scraper):
    """Scraper for fabrics from Spotlight
    https://www.spotlightstores.com/sewing-fabrics/fabric-by-the-metre
    """
    scraper_name = "spotlight"

    def scrape_page(self, page, found_urls=[]):
        page_url = f"https://www.spotlightstores.com/sewing-fabrics/fabric-by-the-metre?q=:latest&page={page}"

        resp = requests.get(page_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        image_tags = soup.find_all("img", id="productdetailimg")
        for img in image_tags:
            url = img.get("content")
            name = img.get("alt")
            if not url or not name:
                continue
            found_urls.append((url, f"{sanitize_name(name)}.jpg"))

        # Keep progressing through the pages until we run out of images
        if len(image_tags) > 0:
            return self.scrape_page(page + 1, found_urls)
        else:
            return found_urls

    def build_url_list(self):
        return self.scrape_page(0)


if __name__ == "__main__":
    scraper = SpotlightScraper()
    scraper.run()
