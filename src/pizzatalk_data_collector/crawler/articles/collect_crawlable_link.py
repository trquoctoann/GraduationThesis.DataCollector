from crawler.articles.utils.date_utils import (
    convert_datetext_to_datetime,
    convert_fotmob_datetext_to_datetime,
)
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def setup_selenium():
    # this code is running on microsoft edge
    edgeOption = webdriver.EdgeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76"
    edgeOption.add_argument(f"user-agent={user_agent}")
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=edgeOption)
    return driver


def extract_link(driver):
    articles = driver.find_elements(By.TAG_NAME, "article")
    urls = set()
    for article in articles:
        links = article.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href:
                urls.add(href)
    return urls


def is_later_than_last_crawl_datetime(
    last_crawl_datetime, current_crawl_datetime
):
    current_crawl_datetime = convert_fotmob_datetext_to_datetime(
        current_crawl_datetime
    )

    if last_crawl_datetime > current_crawl_datetime:
        return False
    return True


def click_load_more_button(driver, wait, number_of_articles):
    try:
        load_more_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".css-1pia8e3-BrowseButton.e15lpzb72")
            )
        )
        driver.execute_script(
            "arguments[0].scrollIntoView();", load_more_button
        )
        driver.execute_script("arguments[0].click();", load_more_button)

        list_articles = driver.find_elements(By.TAG_NAME, "article")
        wait.until(lambda d: len(list_articles) > number_of_articles)

        return list_articles
    except (TimeoutException, ElementClickInterceptedException):
        return None


def collect_crawlable_link(last_crawl_datetime, league_link_list):
    urls = []

    for league_link in league_link_list:
        print(league_link)
        driver = setup_selenium()
        wait = WebDriverWait(driver, 20)
        driver.get(league_link)
        number_of_articles = len(driver.find_elements(By.TAG_NAME, "article"))

        while True:
            list_articles = click_load_more_button(
                driver, wait, number_of_articles
            )
            if not list_articles:
                break

            last_article = list_articles[-1]
            last_article_datetime = last_article.find_element(
                By.CLASS_NAME, "css-1noqf91-ArticleSourceTime"
            )

            if not is_later_than_last_crawl_datetime(
                last_crawl_datetime, last_article_datetime.text
            ):
                break

            number_of_articles = len(list_articles)

        urls.append(extract_link(driver))

        driver.quit()
    return urls
