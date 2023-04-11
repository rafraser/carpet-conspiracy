import csv
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

        urls_have_name = isinstance(urls[0], tuple)
        cache_extension = "csv" if urls_have_name else "txt"
        cache_file = os.path.join(self.cache_base_directory, f"{self.scraper_name}.{cache_extension}")
        with open(cache_file, "w") as f:
            if urls_have_name:
                writer = csv.writer(f, delimiter=",")
                writer.writerows(urls)
            else:
                # i'm sure there's a reason i'm not using writelines here...
                f.write("\n".join(urls))

    def run(self, cache_urls=True, progress=True):
        urls = self.build_url_list()

        if cache_urls:
            self.cache_urls(urls)

        output_directory = os.path.join(self.output_base_directory, self.scraper_name)
        results_summary = download_batch(urls, output_directory, poolsize=self.poolsize, show_progress=progress)
        return results_summary


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
