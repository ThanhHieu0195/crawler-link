from Configs.enum import ServerConfig
from Facade.Selemium.builder.IBuilder import IBuilder
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ChromeBuilder(IBuilder):
    @staticmethod
    def build():
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        exec_path = ChromeBuilder.get_chrome_driver_path()
        driver = webdriver.Chrome(service_log_path='Log/selenium.log', options=chrome_options, executable_path=exec_path)
        return driver

    @staticmethod
    def get_chrome_driver_path():
        return ServerConfig.SELENIUM_CHROME_DRIVER_PATH.value
