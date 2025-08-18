# Princeton Facebook Scraper

A web scraper for downloading profile photos from Princeton's face directory to help club officers memorize club members.

## Usage

1. Add names to `names.txt` (one per line)
2. Run: `python scraper.py`
3. Login when the browser opens
4. Type 'y' to start scraping
5. Photos will be saved to `output/` as `First_Last.jpg`

## Requirements

- Python 3
- Chrome browser
- `pip install selenium requests`