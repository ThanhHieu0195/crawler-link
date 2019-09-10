from CrawlerLib.helper import get_utc_time
from Facade.Selemium.IBase import IBase
from PIL import Image
from io import BytesIO
import time


class YoutubePost(IBase):
    height = 700
    width = 800

    def screen_post(self, selenium, post_id):
        selenium.driver.set_window_size(self.width, self.height)
        selenium.driver.get('https://www.youtube.com/watch?v=%s' % post_id)
        time.sleep(2)
        selenium.driver.maximize_window()
        png = selenium.driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        png_name = '%s' % post_id
        im.save('Screenshot/YT-%s.png' % png_name)
        selenium.driver.quit()
        return png_name
