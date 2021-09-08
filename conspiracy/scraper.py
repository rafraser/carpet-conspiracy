import os
from conspiracy.downloader import download_batch


class Scraper:
    scraper_name = "base"

    poolsize = 5
    cache_base_directory = "cache"
    output_base_directory = "output"

    def build_url_list(self):
        raise NotImplementedError

    def cache_urls(self, urls):
        if len(urls) < 1:
            return

        os.makedirs(self.cache_base_directory, exist_ok=True)
        cache_file = os.path.join(self.cache_base_directory, f"{self.scraper_name}.txt")
        with open(cache_file, "w") as f:
            if isinstance(urls[0], tuple):
                for (url, name) in urls:
                    f.write(f"{url},{name}\n")
            else:
                f.write("\n".join(urls))

    def run(self, cache_urls=True):
        urls = self.build_url_list()

        if cache_urls:
            self.cache_urls(urls)

        output_directory = os.path.join(self.output_base_directory, self.scraper_name)
        results_summary = download_batch(urls, output_directory, poolsize=self.poolsize)
        return results_summary


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
