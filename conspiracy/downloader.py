import argparse
import os
import requests
from enum import Enum
from multiprocessing.pool import ThreadPool
from urllib.parse import urlparse


class DownloadResult(Enum):
    SUCCESS = 0
    NOT_FOUND = 1
    FAILED = 2
    ALREADY_EXISTS = 3


class DownloadStats():
    def __init__(self):
        self._stats = {result.name: 0 for result in DownloadResult}

    def add_result(self, result):
        self._stats[result.name] = self._stats.get(result.name, 0) + 1

    def stats(self):
        return self._stats

    def __add__(self, other):
        result = DownloadStats()
        result._stats = {k: self._stats.get(k, 0) + other._stats.get(k, 0) for k in DownloadResult}
        return result

    def __str__(self):
        total = sum(self._stats.values())
        skipped = self._stats.get(DownloadResult.ALREADY_EXISTS.name)
        successful = self._stats.get(DownloadResult.SUCCESS.name) + skipped
        return f"{successful}/{total} ({skipped} skipped)"


def download_file(entry):
    url, filename = entry
    attempt_count = 0
    if os.path.exists(filename):
        return DownloadResult.ALREADY_EXISTS

    while attempt_count < 5:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            return DownloadResult.SUCCESS
        elif r.status_code == 404:
            return DownloadResult.NOT_FOUND
        attempt_count += 1

    return DownloadResult.FAILED


def filename_from_url(url, directory):
    basename = os.path.basename(urlparse(url).path)
    return os.path.join(directory, basename)


def download_batch(urls, directory, poolsize=5):
    os.makedirs(directory, exist_ok=True)
    if len(urls) < 1:
        return DownloadStats()

    # If we're given a list of URLs, guess the filename & download those
    # We can also accept a list of (url, name) tuples for finer control
    if not isinstance(urls[0], tuple):
        urls = [(url, filename_from_url(url, directory)) for url in urls]

    results_summary = DownloadStats()
    for result in ThreadPool(poolsize).imap_unordered(download_file, urls):
        results_summary.add_result(result)
    return results_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download all URLs in a given file.")
    parser.add_argument("input_file", help="File containing URLs to download. Each URL should be on a seperate line.")
    parser.add_argument("output_directory", help="Directory to output downloaded content to.")
    args = parser.parse_args()

    with open(args.input_file) as f:
        urls = f.read().splitlines()
        results = download_batch(urls, args.output_directory)
        print(results)
