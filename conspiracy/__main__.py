import argparse
from conspiracy.scrapers import scrapers
from conspiracy.downloader import DownloadStats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a given scraper")
    parser.add_argument("scrapers", help="Scraper(s) to run. Comma seperated for multiple. 'all' to run everything.")
    parser.add_argument("--progress", help="Show a progress bar?", action="store_true")
    args = parser.parse_args()

    # Determine which scrapers to run
    scrapers_to_run = []
    if args.scrapers == "all":
        scrapers_to_run = scrapers.values()
    else:
        scrapers_to_run = [scrapers.get(arg, None) for arg in args.scrapers.split(",")]
        if any([x is None for x in scrapers_to_run]):
            raise ValueError("Invalid scraper list provided.")

    # Run all scrapers & collect results
    print(f"Running {len(scrapers_to_run)} scrapers.")
    combined_results = DownloadStats()
    for scraper in scrapers_to_run:
        scraper_instance = scraper()
        print(f"Starting: {scraper_instance.scraper_name}")
        results = scraper_instance.run(progress=args.progress)
        print(f"[{scraper.scraper_name}] Finished: {results}")
        combined_results = combined_results + results
    print(f"[All] Finished: {combined_results}")
