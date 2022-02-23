import argparse
import progressbar
import os
import requests
from enum import Enum
from multiprocessing.pool import ThreadPool
from urllib.parse import urlparse


def progress_widgets():
    """Progress bar widgets - used for show progress mode of the downloader
    """
    return [
        progressbar.Bar(),
        ' ', progressbar.SimpleProgress(), ' | ',
        progressbar.AdaptiveETA()
    ]


class DownloadResult(Enum):
    SUCCESS = 0
    NOT_FOUND = 1
    FAILED = 2
    ALREADY_EXISTS = 3


class DownloadStats():
    """Helper class used to aggregate a list of DownloadResults
    """
    def __init__(self):
        self._stats = {result.name: 0 for result in DownloadResult}

    def add_result(self, result):
        self._stats[result.name] = self._stats.get(result.name, 0) + 1

    def stats(self):
        return self._stats

    def __add__(self, other):
        result = DownloadStats()
        result._stats = {k.name: self._stats.get(k.name, 0) + other._stats.get(k.name, 0) for k in DownloadResult}
        return result

    def __str__(self):
        total = sum(self._stats.values())
        skipped = self._stats.get(DownloadResult.ALREADY_EXISTS.name, 0)
        successful = self._stats.get(DownloadResult.SUCCESS.name, 0) + skipped
        return f"{successful}/{total} ({skipped} skipped)"


def download_file(entry, max_attempts=3):
    """Attempt to download a file

    Args:
        entry ((str, str)): Tuple containing URL and filename information
        max_attempts (int): Number of times to retry downloading the file. Defaults to 3.

    Returns:
        DownloadResult
    """
    url, filename = entry
    attempt_count = 0
    if os.path.exists(filename):
        return DownloadResult.ALREADY_EXISTS

    while attempt_count < max_attempts:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            # Successful result, save to a file
            with open(filename, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            return DownloadResult.SUCCESS
        elif r.status_code == 404:
            return DownloadResult.NOT_FOUND
        attempt_count += 1

    # We did our best, but it failed for reasons other than 404 error
    return DownloadResult.FAILED


def filename_from_url(url, directory):
    """Given a URL, attempt to guess a filename for it

    Args:
        url (str): URL to extract filename from
        directory (str): Directory for the filename

    Returns:
        str: Full path to a file
    """
    basename = os.path.basename(urlparse(url).path)
    return os.path.join(directory, basename)


def download_batch(urls, directory, poolsize=5, show_progress=False):
    """Download a batch of URLs into a given directory

    Args:
        urls (list): List of URLs or (URL, filename) tuples to download
        directory (str): Directory to save downloaded files to
        poolsize (int, optional): Number of threads. Defaults to 5.
        progress (bool, optional): Render a progress bar? Defaults to False

    Returns:
        DownloadStats: results of all the downloads
    """
    os.makedirs(directory, exist_ok=True)
    if len(urls) < 1:
        return DownloadStats()

    # If we're given a list of URLs, guess the filename & download those
    # We can also accept a list of (url, name) tuples for finer control
    if not isinstance(urls[0], tuple):
        urls = [(url, filename_from_url(url, directory)) for url in urls]
    else:
        urls = [(url, os.path.join(directory, name)) for (url, name) in urls]

    # Run all the URLs and collect results
    results_summary = DownloadStats()
    thread_pool = ThreadPool(poolsize).imap_unordered(download_file, urls)
    if show_progress:
        thread_pool = progressbar.progressbar(thread_pool, widgets=progress_widgets(), max_value=len(urls))

    for result in thread_pool:
        # print('ding')
        results_summary.add_result(result)
    return results_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download all URLs in a given file.")
    parser.add_argument("input_file", help="File containing URLs to download. Each URL should be on a seperate line.")
    parser.add_argument("output_directory", help="Directory to output downloaded content to.")
    parser.add_argument("--pool", help="Number of threads to use", default=5)
    parser.add_argument("--progress", help="Show a progress bar", action="store_true")
    args = parser.parse_args()

    with open(args.input_file) as f:
        urls = f.read().splitlines()
        results = download_batch(urls, args.output_directory, poolsize=args.pool, show_progress=args.progress)
        print(results)
