
# Web Scraping Template with BeautifulSoup
# Repository: CodeAlpha_WebScraping

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import random
from urllib.parse import urljoin, urlparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebScraper:
    # Initialize scraper with base URL, headers, and delay
    def __init__(self, base_url, headers=None, delay=1):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session.headers.update(self.headers)
    
    # Fetch webpage and return BeautifulSoup object
    def fetch_page(self, url):
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            time.sleep(self.delay + random.uniform(0, 1))
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    # Find elements using flexible selectors
    def find_elements(self, soup, element_type, attributes=None, text=None):
        if attributes is None:
            attributes = {}
        if element_type.startswith('.'):
            return soup.select(element_type)
        if element_type.startswith('#'):
            return soup.select(element_type)
        if 'class' in attributes:
            return soup.find_all(element_type, class_=attributes['class'])
        if text:
            return soup.find_all(string=lambda x: x and text.lower() in x.lower())
        return soup.find_all(element_type, **attributes)
    
    # Safely extract text or attribute from an element
    def extract_text_safe(self, element, selector, attribute=None, default=''):
        try:
            found = element.select_one(selector) if '.' in selector or '#' in selector or ' ' in selector else element.find(selector)
            if found:
                if attribute:
                    # Specific fix for lists (like class names)
                    val = found.get(attribute, default)
                    if isinstance(val, list):
                        return " ".join(val).strip()
                    return val.strip()
                return found.get_text(strip=True)
            return default
        except Exception:
            return default
    
    # Scrape data from paginated content
    def scrape_paginated_data(self, url_pattern, num_pages=5, **kwargs):
        all_data = []
        for page in range(1, num_pages + 1):
            url = url_pattern.format(page=page)
            soup = self.fetch_page(url)
            if soup:
                # Custom flag pass-through to assist example 2 if needed
                page_data = self.parse_data(soup, **kwargs)
                all_data.extend(page_data)
                logger.info(f"Scraped page {page}: {len(page_data)} items")
            else:
                logger.warning(f"Failed to fetch page {page}")
                break
        return all_data
    
    # Parse data from soup based on field mappings
    def parse_data(self, soup, item_selector='', fields=None, is_hn=False):
        items = []
        
        # FIX FOR HACKER NEWS (Example 2)
        if is_hn:
            containers = soup.select(item_selector)
            for container in containers:
                item = {}
                # The subtext row containing score, author, and time is the immediate next sibling row
                subtext_container = container.find_next_sibling('tr')
                
                for field_name, selector_info in fields.items():
                    selector = selector_info.get('selector', '')
                    attribute = selector_info.get('attribute', None)
                    default = selector_info.get('default', '')
                    
                    # Core article data lives in the main row
                    if field_name in ['title', 'url']:
                        item[field_name] = self.extract_text_safe(container, selector, attribute, default)
                    # Metadata lives in the sibling row
                    else:
                        if subtext_container:
                            item[field_name] = self.extract_text_safe(subtext_container, selector, attribute, default)
                        else:
                            item[field_name] = default
                if any(item.values()):
                    items.append(item)
            return items

        # DEFAULT PARSING LOGIC
        containers = soup.select(item_selector) if item_selector else [soup]
        for container in containers:
            item = {}
            if fields:
                for field_name, selector_info in fields.items():
                    if isinstance(selector_info, dict):
                        selector = selector_info.get('selector', '')
                        attribute = selector_info.get('attribute', None)
                        default = selector_info.get('default', '')
                        item[field_name] = self.extract_text_safe(container, selector, attribute, default)
                    else:
                        item[field_name] = self.extract_text_safe(container, selector_info)
            else:
                item['text'] = container.get_text(strip=True)
                
            if any(item.values()):
                items.append(item)
        return items
    
    # Extract all links from a page
    def scrape_links(self, soup, base_url=None):
        links = set()
        base = base_url or self.base_url
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(base, link['href'])
            links.add(absolute_url)
        return list(links)
    
    # Save scraped data to CSV file
    def save_to_csv(self, data, filename):
        if not data:
            logger.warning("No data to save")
            return
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logger.info(f"Data saved to {filename} ({len(data)} rows)")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    # Save scraped data to JSON file
    def save_to_json(self, data, filename):
        import json
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")

# Example 1: Scrape product data from an e-commerce website
def example_1_product_scraping():
    scraper = WebScraper(base_url='https://books.toscrape.com', delay=1)
    
    # FIXED: Adjusted selectors to fit standard book element structures
    fields = {
        'title': {'selector': 'h3 a', 'attribute': 'title'},
        'price': {'selector': 'p.price_color', 'default': 'N/A'},
        # 'class' returns an array (e.g., ['star-rating', 'Three']). extract_text_safe joins them into a string.
        'rating': {'selector': 'p.star-rating', 'attribute': 'class'}, 
        'availability': {'selector': 'p.instock.availability', 'default': 'Unknown'}
    }
    
    catalog_data = scraper.scrape_paginated_data(
        url_pattern='https://books.toscrape.com/catalogue/page-{page}.html',
        num_pages=5, 
        item_selector='article.product_pod',
        fields=fields
    )
    
    print(f"Scraped {len(catalog_data)} products")
    scraper.save_to_csv(catalog_data, 'products.csv')
    scraper.save_to_json(catalog_data, 'products.json')
    return catalog_data

# Example 2: Scrape news headlines from a news website
def example_2_news_article_scraping():
    scraper = WebScraper(base_url='https://news.ycombinator.com', delay=0.5)
    soup = scraper.fetch_page('https://news.ycombinator.com/news')
    
    if soup:
        # FIXED: Adjusted subtext metadata selectors to match Hacker News' structures
        fields = {
            'title': {'selector': 'span.titleline > a', 'default': 'No title'},
            'url': {'selector': 'span.titleline > a', 'attribute': 'href', 'default': ''},
            'score': {'selector': 'span.score', 'default': '0 points'},
            'author': {'selector': 'a.hnuser', 'default': 'Unknown'},
            'time': {'selector': 'span.age', 'attribute': 'title', 'default': 'Unknown'}
        }
        
        # Added 'is_hn=True' flag so it parses both the article row and its companion subtext row
        articles = scraper.parse_data(soup, item_selector='tr.athing', fields=fields, is_hn=True)
        print(f"Scraped {len(articles)} articles")
        scraper.save_to_csv(articles, 'news_articles.csv')
        links = scraper.scrape_links(soup)
        print(f"Found {len(links)} unique links")
        return articles
    return None

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("WEB SCRAPING TEMPLATE WITH BEAUTIFULSOUP")
    print("=" * 60)
    
    # Run examples (uncomment the one you want to use)
    
    example_1_product_scraping()
    #example_2_news_article_scraping()

