# Carpet Conspiracy

Carpet Conspiracy is a collection of web-scrapers for various fabric patterns.

## Running

Help:

```bash
python -m conspiracy -h
```

To run a single scraper:

```bash
python -m conspiracy astro
```

To run all scrapers:

```bash
python -m conspiracy all
```

## Process

- Scraper collects list of image URLs from the source website
- URLs are cached to a .txt for easier retrieval
- Downloader extracts images in parallel

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

### Miscellaneous

| Source | Description | Approx. Count |
| ------ | ----------- | ------------- |
| [Emojipedia](https://originalstitch.com/) | Windows 10 emojis | 3,250 |
