import requests
from bs4 import BeautifulSoup
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MParticleScraper:
    def __init__(self):
        self.base_url = "https://docs.mparticle.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.documents = []

    def scrape(self):
        """Main method to scrape mParticle documentation"""
        logger.info("Starting mParticle documentation scraping")

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

            logger.info(f"Completed scraping mParticle documentation. Total documents: {len(self.documents)}")
            return self.documents

        except Exception as e:
            logger.error(f"Error scraping mParticle documentation: {str(e)}")
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
            if href and (href.startswith("/") or href.startswith("https://docs.mparticle.com")):
                if href.startswith("/"):
                    full_url = f"https://docs.mparticle.com{href}"
                else:
                    full_url = href
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
                    full_url = f"https://docs.mparticle.com{href}"
                elif href.startswith("http"):
                    full_url = href
                else:
                    # Handle relative URLs based on parent
                    parent_dir = "/".join(parent_url.split("/")[:-1])
                    full_url = f"{parent_dir}/{href}"

                if full_url not in links and "docs.mparticle.com" in full_url:
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
                    "source": "mParticle",
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
                "title": "Creating a user profile in mParticle",
                "url": "https://docs.mparticle.com/guides/identity/",
                "content": """
                Creating a user profile in mParticle:

                User profiles in mParticle are created automatically when user data is collected.
                To create and manage user profiles effectively:

                1. Implement proper user identification:
                   - Use the identify() method to set user identifiers
                   - Call login() when a user authenticates
                   - Use the setUserAttribute() method to add profile attributes

                2. Example implementation for web:
                ```javascript
                // Set user identifiers
                mParticle.Identity.getCurrentUser().setUserAttribute("name", "John Doe");
                mParticle.Identity.getCurrentUser().setUserAttribute("premium_user", true);
                mParticle.Identity.getCurrentUser().setUserAttribute("last_purchase_date", "2023-04-15");

                // Set user identities
                var identityRequest = {
                    userIdentities: {
                        email: "john.doe@example.com",
                        customerid: "CID-12345"
                    }
                };

                mParticle.Identity.login(identityRequest);
                ```

                3. Best practices:
                   - Use consistent identity types across platforms
                   - Associate anonymous users with known users properly
                   - Implement an identity strategy before sending data

                mParticle's Identity API will automatically merge user profiles when
                identifiers match, creating a unified customer view.
                """,
                "source": "mParticle",
            },
            {
                "title": "Setting up data feeds in mParticle",
                "url": "https://docs.mparticle.com/guides/data-master/",
                "content": """
                Setting up data feeds in mParticle:

                Data feeds in mParticle allow you to ingest data from various sources:

                1. Go to Setup > Inputs > Data Feeds in the mParticle dashboard
                2. Select the data feed type you want to configure
                3. Follow the specific configuration steps for that feed:
                   - For API-based feeds: Generate API credentials
                   - For file-based feeds: Configure file format and delivery settings
                   - For partner feeds: Connect through the partner's interface

                4. Common data feed types include:
                   - CRM data (like Salesforce)
                   - Email service provider data
                   - Offline purchase data
                   - Loyalty program data

                5. Advanced features:
                   - Data transformations before ingestion
                   - Scheduled vs. real-time ingestion
                   - Profile unification with existing user profiles

                Best practices include regular data quality monitoring and
                setting up appropriate data governance rules.
                """,
                "source": "mParticle",
            },
            {
                "title": "Creating audience segments in mParticle",
                "url": "https://docs.mparticle.com/guides/platform-guide/audiences/",
                "content": """
                Creating audience segments in mParticle:

                To create powerful audience segments:

                1. Navigate to Audiences in your mParticle dashboard
                2. Click "Create Audience"
                3. Define your audience using criteria types:
                   - User attributes (demographics, preferences)
                   - Event behaviors (actions taken or not taken)
                   - Frequency and recency (how often and how recently)
                   - Advanced calculations and formulas

                4. Set audience output settings:
                   - Real-time calculation vs. batch processing
                   - Audience refresh frequency
                   - Connected destinations

                5. Example criteria:
                   - Users who purchased in the last 30 days AND viewed a specific product
                   - Users with cart abandonment in last 7 days
                   - Premium users who haven't used a key feature

                6. Activate your audience to make it available to marketing destinations

                mParticle's audience builder allows you to preview audience size and
                composition before activating it to your marketing channels.
                """,
                "source": "mParticle",
            },
            {
                "title": "Implementing real-time event tracking in mParticle",
                "url": "https://docs.mparticle.com/developers/sdk/web/event-tracking/",
                "content": """
                Implementing real-time event tracking in mParticle:

                To track user events across different platforms:

                1. Web SDK implementation:
                ```javascript
                // Track custom event
                mParticle.logEvent(
                    'Button Clicked',
                    mParticle.EventType.Navigation,
                    {
                        buttonName: 'Submit',
                        pageSection: 'Checkout',
                        timestamp: Date.now()
                    }
                );

                // Track commerce event
                var product = mParticle.eCommerce.createProduct(
                    'Product Name',
                    'SKU-1234',
                    19.99,
                    1
                );

                mParticle.eCommerce.logProductAction(
                    mParticle.ProductActionType.AddToCart,
                    [product]
                );
                ```

                2. Mobile SDK implementation (iOS example):
                ```swift
                // Track custom event
                let eventAttributes = ["buttonName": "Submit", "pageSection": "Checkout"]
                MPEvent(name: "Button Clicked", type: MPEventType.navigation, attributes: eventAttributes)

                // Track commerce event
                let product = MPProduct.init(name: "Product Name", sku: "SKU-1234", quantity: 1, price: 19.99)
                let event = MPCommerceEvent.init(action: .addToCart, product: product)
                MParticle.sharedInstance().logEvent(event)
                ```

                3. Best practices:
                   - Use consistent event names across platforms
                   - Include consistent properties with each event type
                   - Follow a naming convention for all events
                   - Use the appropriate event type (navigation, transaction, etc.)

                mParticle's real-time tracking can power personalization, analytics,
                and marketing automation across your entire technology stack.
                """,
                "source": "mParticle",
            }
        ]