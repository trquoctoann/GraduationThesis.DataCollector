import json
from abc import ABC, abstractmethod

import requests


class AbstractCrawler(ABC):
    def __init__(self, request_url, session=None, user_agent=None):
        default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76"
        self.request_url = request_url
        self.session = session if session else requests.Session()
        self.headers = {
            "User-Agent": user_agent if user_agent else default_user_agent
        }

    def fetch(self):
        try:
            response = self.session.get(self.request_url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.HTTPError as http_err:
            self.logger.error(f"HTTP Error for {self.request_url}: {http_err}")
        except requests.RequestException as req_err:
            self.logger.error(
                f"Request to {self.request_url} failed: {req_err}"
            )
        return None

    @abstractmethod
    def extract_data(self, json_response):
        pass

    def crawl(self):
        self.logger.debug(f"Start crawling {self.request_url}")
        response = self.fetch()
        if response:
            data = self.extract_data(response.json())
            if data:
                self.logger.debug(
                    f"Successfully crawled and extracted data from {self.request_url}"
                )
                return data
        self.logger.error(f"Failed to crawl {self.request_url}")
        return None
