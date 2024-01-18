import json
import time

from common.setup_selenium import setup_selenium
from constants.webdriver_type import WebDriverType
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def collect_api_request_url(original_url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--ignore-certificate-errors")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = setup_selenium(WebDriverType.CHROME_DRIVER, options=options)

    driver.get(original_url)
    time.sleep(10)

    logs = driver.get_log("performance")
    api_requests = set()

    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if "Network.requestWillBeSent" in log["method"]:
            if "request" in log["params"]:
                request = log["params"]["request"]
                url = request["url"]
                if "https://api.alfrescos.com.vn/api/" in url:
                    api_requests.add(url)
    driver.quit()
    return api_requests
