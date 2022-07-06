from conspiracy.scraper import Scraper


class OriginalStitchScraper(Scraper):
    """Scraper for Original Stitch's Pokemon shirt patterns
    https://originalstitch.com/pokemon/pokemon_shirts#section-pokemon
    """
    scraper_name = "pokemon"

    @staticmethod
    def pattern_url(id: int) -> str:
        """Given a Pokedex number, return a URL for the corresponding fabric pattern
        """
        return f"https://os-cdn.ec-ffmt.com/gl/pokemon/dedicate/pattern-flat/{id}.jpg"

    def build_url_list(self):
        urls = [self.pattern_url(id) for id in range(1, 397)]

        # At the time of writing, only some Sinnoh patterns have been released
        # In an ideal world I'd have some error checking rather than hard-coding these IDs
        sinnoh_ids = [387, 390, 393, 399, 400, 403, 404, 405, 415, 416, 417, 447, 448]
        urls += [self.pattern_url(id) for id in sinnoh_ids]

        return urls


if __name__ == "__main__":
    scraper = OriginalStitchScraper()
    scraper.run()
