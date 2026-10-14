# Book Scraper

Scrapes every book listed on [books.toscrape.com](https://books.toscrape.com), a practice site built for web scraping, and saves the results to a SQLite database.

## What it does

1. Visits each catalogue page in turn until a page no longer exists.
2. For every book, collects:
   - **name**
   - **price**, in £
   - **in_stock**, the availability text
   - **rating**, 1–5 stars
   - **link**, the full URL of the cover image
3. Waits half a second between pages so it doesn't overload the site.
4. Saves everything to `books.db`, in a table called `books`.
5. Runs a sample query, books under £20 sorted by price, and prints the first few rows.

## Setup

```bash
pip install requests beautifulsoup4 pandas
```

`sqlite3` is built into Python, so it needs no install.

## Run

```bash
python scraper.py
```

It prints a line for each page as it goes, about 50 pages and 1,000 books in total. Then it shows the sample query results.

## Query the data yourself

```python
import sqlite3, pandas as pd

with sqlite3.connect("books.db") as conn:
    print(pd.read_sql("SELECT * FROM books WHERE rating = 5", conn))
```
