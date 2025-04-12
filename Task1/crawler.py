import os
import logging
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
import threading
from langchain_community.document_loaders import FireCrawlLoader  # Importing the FirecrawlLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class WebCrawler:
    def __init__(self):
        self.api = os.getenv('FIRE_CRAWL_API')

    def get_web_data(self, url, mode):
        """
        Crawl the website data using FireCrawl API.
        Parameters
        ----------
            url (str): The URL of the website to crawl.
        Returns
        -------
            dict: The crawled data.
        """
        try:
            loader = FireCrawlLoader(
                api_key=self.api, # API key for FireCrawl
                url=url,  # Target URL to crawl
                mode= mode # Mode set to 'crawl' to crawl all accessible subpages
            )
            docs = loader.load()
            logger.info(f"successfully crawled {url}")
            return docs
        except Exception as e:
            print(f"Error during web crawling: {e}")
            return None

   

# Example Usage
if __name__ == "__main__":
    crawler = WebCrawler()
    crawler.run_in_background("https://heallabsonline.com")