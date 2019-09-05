from CrawlerLib.show_notify import show_debug
from Facade.Selemium.builder.ChormeBuilder import ChromeBuilder
from Facade.Selemium.builder.FirefoxBuilder import FirefoxBuilder


class SeleniumBuilder:
    @staticmethod
    def build(selenium_type):
        show_debug(selenium_type)
        driver = None
        if selenium_type == 'firefox':
            driver = FirefoxBuilder.build()
        if selenium_type == 'chrome':
            driver = ChromeBuilder.build()
        return driver
