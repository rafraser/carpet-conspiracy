from conspiracy.scraper import Scraper
from bs4 import BeautifulSoup
import requests


def upscale(url: str) -> str:
    """Convert an emojipedia URL into a higher resolution version
    """
    return url.replace("/thumbs/72/", "/thumbs/320/")


def url_from_image(tag: str) -> str:
    """Fetch the URL from an image tag on Emojipedia

    Emojipedia makes extensive use of lazy-loading images
    which makes this more complicated than just getting the src tag
    """
    src = tag.get("src")
    if src is not None and "lazy.svg" not in src:
        return src

    if src := tag.get("data-src"):
        return src
    raise ValueError("Invalid tag:", tag)


class EmojiScraper(Scraper):
    """Scraper for Windows 10 emoji patterns, sourced from Emojipedia
    https://emojipedia.org/microsoft/windows-10-may-2019-update/

    This scraper can very easily be adapted for other emoji sets if requested
    However, I'm only interested in the Windows 10 emojis personally
    """
    scraper_name = "emoji"
    emoji_root = "https://emojipedia.org/microsoft/windows-10-may-2019-update/"

    def build_url_list(self):
        resp = requests.get(self.emoji_root)
        soup = BeautifulSoup(resp.text, "html.parser")

        images = soup.find(class_="emoji-grid").find_all("img")
        image_urls = [upscale(url_from_image(image)) for image in images]
        return image_urls


if __name__ == "__main__":
    scraper = EmojiScraper()
    scraper.run()
