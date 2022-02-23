from conspiracy.scraper import Scraper
from bs4 import BeautifulSoup
import requests


def upscale(url):
    return url.replace("/thumbs/72/", "/thumbs/320/")


def url_from_image(tag):
    src = tag.get("src")
    if src is not None and "lazy.svg" not in src:
        return src

    if src := tag.get("data-src"):
        return src
    raise ValueError("Invalid tag:", tag)


class EmojiScraper(Scraper):
    scraper_name = "emoji"
    emoji_root = "https://emojipedia.org/microsoft/windows-10-may-2019-update/"

    def build_url_list(self):
        resp = requests.get(self.emoji_root)
        soup = BeautifulSoup(resp.text, "html.parser")

        images = soup.find(class_="emoji-grid").find_all("img")
        image_urls = [upscale(url_from_image(image)) for image in images]
        print(image_urls)
        return image_urls


if __name__ == "__main__":
    scraper = EmojiScraper()
    scraper.run()
