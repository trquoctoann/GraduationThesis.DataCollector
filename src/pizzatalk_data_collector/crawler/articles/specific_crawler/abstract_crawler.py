import html
import json
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class AbstractArticleCrawler(ABC):
    def __init__(self, source_url, session=None, user_agent=None):
        self.source_url = source_url
        self.session = session if session else requests.Session()
        default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76"
        self.headers = {
            "User-Agent": user_agent if user_agent else default_user_agent
        }

    def fetch(self):
        try:
            response = self.session.get(self.source_url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.HTTPError as http_err:
            self.logger.error(f"HTTP Error for {self.source_url}: {http_err}")
        except requests.RequestException as req_err:
            self.logger.error(
                f"Request to {self.source_url} failed: {req_err}"
            )
        return None

    def parse_json(self, script_tag):
        try:
            return json.loads(script_tag.string)
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Failed to parse JSON: {e}. Data: {script_tag.string}"
            )
            return None

    @staticmethod
    def get_90min_link(url):
        if "fotmob.com" in url and "/embed/" in url:
            response = requests.get(url)
            if response:
                source_html = html.unescape(response.text)
                soup = BeautifulSoup(source_html, "html5lib")
                return soup.find("link", {"rel": "canonical"})["href"]
        return url

    @abstractmethod
    def parse_html(self, source_html):
        # Parse the HTML content and extract news articles.
        pass

    def crawl(self):
        self.logger.debug(f"Start crawling {self.source_url}")
        response = self.fetch()
        if response:
            html_content = response.text
            article = self.parse_html(html_content)
            if article:
                self.logger.debug(
                    f"Successfully crawled and parsed article from {self.source_url}"
                )
                return article
        self.logger.error(f"Failed to crawl {self.source_url}")
        return None
