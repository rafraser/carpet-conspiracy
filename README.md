# Carpet Conspiracy

Carpet Conspiracy is a collection of web-scrapers for various fabric patterns.

## Running

To run a specific scraper, execute the file as a Python module:

```bash
python -m conspiracy.scrapers.camira
```

To download a list of URLs, you can run the downloader script directly:

```bash
python -m conspiracy.downloader urls.txt output/ --progress
```

## Process

- Scraper collects list of image URLs from the source website
- URLs are cached to a file
- Downloader saves images in parallel

## Scrapers List

### Carpets

| Source | Description | Approx. Count |
| ------ | ----------- | ------------- |
| [Astro Carpet Mills](https://www.astrocarpetmills.com/) | Printed carpets for family fun venues | 250 |
| [Omega Pattern Works](https://www.omegapatternworks.com/) | Printed carpets for family fun venues | 800 |

### Fabrics

| Source | Description | Approx. Count |
| ------ | ----------- | ------------- |
| [Camira](https://www.camirafabrics.com/) | Bus, coach, and rail textiles | 550 |
| [OriginalStitch](https://originalstitch.com/) | Printed carpets for family fun venues | 400 |
| [Spotlight](https://www.spotlightstores.com/sewing-fabrics/fabric-by-the-metre) | Sewing fabric | 3,800 |

### Miscellaneous

| Source | Description | Approx. Count |
| ------ | ----------- | ------------- |
| [Emojipedia](https://originalstitch.com/) | Windows 10 emojis | 3,250 |
