import requests
from bs4 import BeautifulSoup
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SegmentScraper:
    def __init__(self):
        self.base_url = "https://segment.com/docs"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.documents = []

    def scrape(self):
        """Main method to scrape Segment documentation"""
        logger.info("Starting Segment documentation scraping")

        try:
            # Start with the main documentation page
            main_page = self._get_page(self.base_url)
            if not main_page:
                return []

            # Extract links to main sections
            section_links = self._extract_section_links(main_page)

            # Process each section
            for section_url in section_links:
                self._process_section(section_url)
                # Be respectful with rate limiting
                time.sleep(1)

            logger.info(f"Completed scraping Segment documentation. Total documents: {len(self.documents)}")
            return self.documents

        except Exception as e:
            logger.error(f"Error scraping Segment documentation: {str(e)}")
            return []

    def _get_page(self, url):
        """Get page content with error handling"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page {url}: {str(e)}")
            return None

    def _extract_section_links(self, soup):
        """Extract links to main documentation sections"""
        links = []
        # This is a placeholder implementation - would need to be adapted to actual site structure
        nav_elements = soup.select("nav a")
        for link in nav_elements:
            href = link.get('href')
            if href and href.startswith("/docs"):
                full_url = f"https://segment.com{href}"
                if full_url not in links:
                    links.append(full_url)
        return links

    def _process_section(self, section_url):
        """Process a documentation section and its pages"""
        soup = self._get_page(section_url)
        if not soup:
            return

        # Extract content from current page
        self._extract_page_content(section_url, soup)

        # Find and process sub-pages
        sub_page_links = self._extract_sub_page_links(soup, section_url)
        for sub_url in sub_page_links:
            sub_soup = self._get_page(sub_url)
            if sub_soup:
                self._extract_page_content(sub_url, sub_soup)
                time.sleep(0.5)  # Polite delay

    def _extract_sub_page_links(self, soup, parent_url):
        """Extract links to sub-pages from a section page"""
        links = []
        # Extract links that might be sub-pages (implementation depends on site structure)
        sub_links = soup.select("a.doc-link")  # Adjust selector based on actual HTML
        for link in sub_links:
            href = link.get('href')
            if href:
                # Handle relative and absolute URLs
                if href.startswith("/"):
                    full_url = f"https://segment.com{href}"
                elif href.startswith("http"):
                    full_url = href
                else:
                    # Handle relative URLs based on parent
                    parent_dir = "/".join(parent_url.split("/")[:-1])
                    full_url = f"{parent_dir}/{href}"

                if full_url not in links and "segment.com/docs" in full_url:
                    links.append(full_url)
        return links

    def _extract_page_content(self, url, soup):
        """Extract relevant content from a documentation page"""
        try:
            # Extract title
            title_element = soup.select_one("h1, .page-title")
            title = title_element.get_text().strip() if title_element else "Untitled"

            # Extract main content
            content_element = soup.select_one("main, .doc-content, article")
            if not content_element:
                content_element = soup.select_one("body")

            if content_element:
                # Clean up the content (remove navigation, footers, etc.)
                for element in content_element.select("nav, footer, .navigation, .sidebar"):
                    element.decompose()

                # Extract text content
                content = content_element.get_text(" ", strip=True)

                # Create document
                document = {
                    "title": title,
                    "url": url,
                    "content": content,
                    "source": "Segment",
                }

                self.documents.append(document)
                logger.info(f"Extracted content from {url}")

        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")

    @staticmethod
    def get_mock_data():
        """Return mock data for testing purposes"""
        return [
            {
                "title": "Setting up a new source in Segment",
                "url": "https://segment.com/docs/connections/sources/",
                "content": """
                Setting up a new source in Segment:

                1. Navigate to the Segment dashboard and log in
                2. Click on 'Sources' in the main navigation
                3. Click the 'Add Source' button
                4. Search for and select the type of source you want to add
                5. Name your source and click 'Add Source'
                6. Follow the configuration steps for your specific source type
                7. Complete any additional settings like tracking plan assignment
                8. Save your configuration

                For website sources, you'll need to add the Segment snippet to your site.
                For server-side sources, you'll need to install the appropriate library.
                For mobile sources, you'll need to integrate the Segment SDK.

                Best practices include using descriptive names for your sources and
                implementing proper tracking plans before sending data.
                """,
                "source": "Segment",
            },
            {
                "title": "Implementing event tracking in Segment",
                "url": "https://segment.com/docs/connections/sources/catalog/libraries/website/javascript/",
                "content": """
                Implementing event tracking in Segment:

                After setting up your source, you can track events using:

                1. For website:
                ```javascript
                analytics.track('Event Name', {
                  property1: 'value1',
                  property2: 'value2'
                });
                ```

                2. For server-side (Node.js example):
                ```javascript
                analytics.track({
                  userId: 'user123',
                  event: 'Event Name',
                  properties: {
                    property1: 'value1',
                    property2: 'value2'
                  }
                });
                ```

                3. For mobile (iOS example):
                ```swift
                Analytics.shared().track("Event Name", properties: [
                  "property1": "value1",
                  "property2": "value2"
                ])
                ```

                Make sure to follow a consistent naming convention for your events
                and properties to ensure data quality.
                """,
                "source": "Segment",
            },
            {
                "title": "Creating and managing destinations in Segment",
                "url": "https://segment.com/docs/connections/destinations/",
                "content": """
                Creating and managing destinations in Segment:

                1. Go to the Destination catalog in your Segment workspace
                2. Search for and select your desired destination
                3. Choose which Source(s) you want to connect to this destination
                4. Configure the destination-specific settings:
                   - API keys or credentials
                   - Data mapping settings
                   - Event filtering options
                5. Enable the destination when ready

                Advanced features include:
                - Transformation functions to modify data before it reaches destinations
                - Event filtering to control which events go to which destinations
                - Device-mode vs cloud-mode destination options

                You can also use the Segment Protocols feature to enforce
                data quality standards across all your destinations.
                """,
                "source": "Segment",
            },
            {
                "title": "Building audiences in Segment",
                "url": "https://segment.com/docs/audiences/",
                "content": """
                Building audience segments in Segment:

                1. Navigate to the Audience section in your Segment workspace
                2. Click "Create New Audience"
                3. Define your audience using the following criteria types:
                   - User properties
                   - Event behaviors
                   - Computed traits
                   - Recency and frequency
                4. Set up real-time sync with your marketing destinations
                5. Activate the audience

                Effective audience strategies include:
                - Creating behavior-based segments (like "viewed product but didn't purchase")
                - Using frequency criteria to identify power users
                - Combining demographic and behavioral data
                - Creating exclusion rules for more precise targeting

                You can also use the A/B testing features to measure the
                effectiveness of different audience segments.
                """,
                "source": "Segment",
            }
        ]