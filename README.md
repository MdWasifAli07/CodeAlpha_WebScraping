# Web Scraping with BeautifulSoup

## 📌 Repository: `CodeAlpha_WebScraping`

[cite_start]This repository contains a modular, object-oriented Python web scraper built using **BeautifulSoup** and **Requests**[cite: 24]. [cite_start]It is developed as part of the **CodeAlpha Data Analytics Internship** for **Task 1: Web Scraping**[cite: 1, 2, 23]. 

[cite_start]The template is designed to gather data efficiently while handling dynamic web scraping challenges such as request throttling, custom headers, data formatting, and pagination[cite: 27].

---

## 🚀 Features

* **Object-Oriented Architecture:** Encapsulated within a reusable `WebScraper` class.
* **Anti-Bot Configurations:** Dynamic `User-Agent` headers and randomized execution delays to mimic human behavior and bypass basic scraping restrictions.
* **Robust HTML Parsing:** Dual support for CSS selectors (`soup.select`) and traditional BeautifulSoup methods (`soup.find_all`).
* **Error Prevention:** Safe data extraction methods targeting edge cases like empty nodes or structural elements returning nested list items (e.g., class attributes).
* **Multi-Format Exporting:** Automatically structures parsed text arrays into Pandas DataFrames and saves them cleanly into both `.csv` (using BOM encoding `utf-8-sig` for Excel compatibility) and formatted `.json` configurations.

---

## 🛠️ Practical Implementations Covered

The codebase comes equipped with fixed, working examples for several highly structured test websites:

### 1. E-Commerce Pagination (`Example 1`)
* **Target:** `books.toscrape.com`
* **Data Captured:** Title, Price, Star Ratings, and Stock Availability status.
* **Technique:** Automated multi-page crawling using regex/string-pattern configuration schemas.

### 2. Multi-Row Sibling Parsing (`Example 2`)
* **Target:** Hacker News (`news.ycombinator.com`)
* **Data Captured:** Title, URL, Score, Author, and Time Stamp.
* **Technique:** Employs sibling element traversals (`find_next_sibling('tr')`) to parse nested context data when layout items stretch across consecutive horizontal DOM blocks.

### 3. Basic Wikipedia Scraping (`Example 3`)
* **Target:** Wikipedia Web Scraping Page
* **Data Captured:** Core main-header layouts and intro summary paragraph components.

---

## 📦 Setup & Requirements

Ensure you have Python 3.x installed along with the required third-party libraries.

### 1. Installation
[cite_start]Clone this repository to your local directory [cite: 16] and install dependencies:
```bash
pip install requests beautifulsoup4 pandas
