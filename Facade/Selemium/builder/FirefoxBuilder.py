from Facade.Selemium.builder.IBuilder import IBuilder
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class FirefoxBuilder(IBuilder):
    @staticmethod
    def build():
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Firefox(service_log_path='Log/selenium.log', options=options)
        return driver
