from conspiracy.scraper import Scraper


class AstroCarpetScraper(Scraper):
    scraper_name = "astro"

    def build_url_list(self):
        return [("https://astrocarpetmills.com/replace_colors/950/?from=&to=&cnt=undefined", "skate.png")]
        return [("https://astrocarpetmills.com/replace_colors/156/?from=&to=&cnt=undefined", "strike.png")]


if __name__ == "__main__":
    scraper = AstroCarpetScraper()
    scraper.run()
