from conspiracy.scraper import Scraper


class OriginalStitchScraper(Scraper):
    scraper_name = "pokemon"

    def build_url_list(self):
        return [f"https://pokemon.originalstitch.com/en/img/pattern_all/{i}.jpg" for i in range(1, 397)]


if __name__ == "__main__":
    scraper = OriginalStitchScraper()
    scraper.run()
