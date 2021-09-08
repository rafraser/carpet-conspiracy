import os
from conspiracy.downloader import download_batch


class Scraper:
    scraper_name = "base"

    poolsize = 5
    cache_base_directory = "cache"
    output_base_directory = "output"

    def build_url_list(self):
        raise NotImplementedError

    def run(self, cache_urls=True, download=True):
        urls = self.build_url_list()

        if cache_urls:
            os.makedirs(self.cache_base_directory, exist_ok=True)
            cache_file = os.path.join(self.cache_base_directory, f"{self.scraper_name}.txt")
            with open(cache_file, "w") as f:
                f.write("\n".join(urls))

        if download:
            output_directory = os.path.join(self.output_base_directory, self.scraper_name)
            results_summary = download_batch(urls, output_directory, poolsize=self.poolsize)
            print(f"[{self.scraper_name}] Finished: {results_summary}")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
