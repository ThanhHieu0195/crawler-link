
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from Facade.Selemium.FBPost import FBPost
from Facade.Selemium.InstagramPost import InstagramPost
from Facade.Selemium.YoutubePost import YoutubePost


class Selenium:
    main_selenium = None

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(service_log_path='Log/selenium.log', options=options)
        self.selenium_types = {
            'fb': FBPost(),
            'ins': InstagramPost(),
            'ytb': YoutubePost()
        }

    @staticmethod
    def get_instance():
        if Selenium.main_selenium is None:
            Selenium.main_selenium = Selenium()
        return Selenium.main_selenium

    def screen_post(self, post_type, post_id):
        if post_type in self.selenium_types:
            return self.selenium_types[post_type].screen_post(self, post_id)
        return None


