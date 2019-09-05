from CrawlerLib.helper import get_utc_time
from Facade.Selemium.IBase import IBase
from PIL import Image
from io import BytesIO
import time


class InstagramPost(IBase):
    def screen_post(self, selenium, post_id):
        selenium.driver.get('https://www.instagram.com/p/%s' % post_id)
        selenium.driver.maximize_window()
        selenium.driver.execute_script("""
                    document.getElementsByTagName('nav')[0].remove()
                """)
        time.sleep(1)
        png = selenium.driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        png_name = '%s-%s' % (get_utc_time('%Y%m%d%H%M'), post_id)
        im.save('Screenshot/%s.png' % png_name)
        selenium.driver.quit()
        return png_name
