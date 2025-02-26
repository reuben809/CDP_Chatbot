import requests
from bs4 import BeautifulSoup
import os
import time
import logging
import json
import argparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ZeotapScraper:
    def __init__(self, output_file="zeotap_docs.json"):
        self.base_url = "https://docs.zeotap.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.documents = []
        self.output_file = output_file

    def scrape(self):
        """Main method to scrape Zeotap documentation."""
        logger.info("Starting Zeotap documentation scraping.")

        try:
            main_page = self._get_page(self.base_url)
            if not main_page:
                return []

            section_links = self._extract_section_links(main_page)

            for section_url in section_links:
                self._process_section(section_url)
                time.sleep(1)  # Polite delay

            self._save_to_json()
            logger.info(f"Completed scraping Zeotap documentation. Total documents: {len(self.documents)}")
            return self.documents

        except Exception as e:
            logger.error(f"Error scraping Zeotap documentation: {str(e)}")
            return []

    def _get_page(self, url):
        """Fetch page content with error handling."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page {url}: {str(e)}")
            return None

    def _extract_section_links(self, soup):
        """Extract links to main documentation sections."""
        links = []
        nav_elements = soup.select("nav a")
        for link in nav_elements:
            href = link.get("href")
            if href and (href.startswith("/") or href.startswith(self.base_url)):
                full_url = self.base_url + href.lstrip("/") if href.startswith("/") else href
                if full_url not in links:
                    links.append(full_url)
        return links

    def _process_section(self, section_url):
        """Process a documentation section and its pages."""
        soup = self._get_page(section_url)
        if not soup:
            return

        self._extract_page_content(section_url, soup)

        sub_page_links = self._extract_sub_page_links(soup, section_url)
        for sub_url in sub_page_links:
            sub_soup = self._get_page(sub_url)
            if sub_soup:
                self._extract_page_content(sub_url, sub_soup)
                time.sleep(0.5)

    def _extract_sub_page_links(self, soup, parent_url):
        """Extract links to sub-pages from a section page."""
        links = []
        sub_links = soup.select("a.doc-link")
        for link in sub_links:
            href = link.get("href")
            if href:
                if href.startswith("/"):
                    full_url = self.base_url + href.lstrip("/")
                elif href.startswith("http"):
                    full_url = href
                else:
                    parent_dir = "/".join(parent_url.split("/")[:-1])
                    full_url = f"{parent_dir}/{href}"

                if full_url not in links and "docs.zeotap.com" in full_url:
                    links.append(full_url)
        return links

    def _extract_page_content(self, url, soup):
        """Extract relevant content from a documentation page."""
        try:
            title_element = soup.select_one("h1, .page-title")
            title = title_element.get_text().strip() if title_element else "Untitled"

            content_element = soup.select_one("main, .doc-content, article") or soup.select_one("body")

            if content_element:
                for element in content_element.select("nav, footer, .navigation, .sidebar"):
                    element.decompose()

                content = content_element.get_text(" ", strip=True)

                document = {
                    "title": title,
                    "url": url,
                    "content": content,
                    "source": "Zeotap",
                }

                self.documents.append(document)
                logger.info(f"Extracted content from {url}")

        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")

    def _save_to_json(self):
        """Save extracted documents to a JSON file."""
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=4)
            logger.info(f"Saved extracted data to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving data to {self.output_file}: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Zeotap documentation")
    parser.add_argument("--output", type=str, default="zeotap_docs.json", help="Output JSON file name")
    args = parser.parse_args()

    scraper = ZeotapScraper(output_file=args.output)
    scraper.scrape()
