
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from Configs.enum import ServerConfig
from CrawlerLib.show_notify import show_debug, show_warning
from Facade.Selemium.FBPost import FBPost
from Facade.Selemium.InstagramPost import InstagramPost
from Facade.Selemium.YoutubePost import YoutubePost


class Selenium:
    main_selenium = None

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Firefox(service_log_path='Log/selenium.log', options=options)
        self.selenium_types = {
            'fb': FBPost(),
            'ins': InstagramPost(),
            'ytb': YoutubePost()
        }

    @staticmethod
    def get_instance():
        Selenium.main_selenium = Selenium()
        return Selenium.main_selenium

    def screen_post(self, post_type, post_id):
        if ServerConfig.ENABLE_SCREENSHOT.value and post_type in self.selenium_types:
            show_debug('Process take screenshot ...')
            try:
                return self.selenium_types[post_type].screen_post(self, post_id)
            except Exception as e:
                show_warning(format(e))
        return None


