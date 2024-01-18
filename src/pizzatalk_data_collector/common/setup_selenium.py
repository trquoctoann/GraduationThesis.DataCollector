from constants.webdriver_type import WebDriverType
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def setup_selenium(webdriver_type, options=None):
    if not options:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76"
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={user_agent}")

    if webdriver_type == WebDriverType.EDGE_DRIVER:
        return webdriver.Edge(
            service=Service(EdgeChromiumDriverManager().install()),
            options=options,
        )
    elif webdriver_type == WebDriverType.CHROME_DRIVER:
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
    else:
        return None
