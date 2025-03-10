import math

from CrawlerLib.helper import get_utc_time
from Facade.Selemium.IBase import IBase
from PIL import Image
from io import BytesIO
import time


class InstagramPost(IBase):
    def screen_post(self, selenium, post_id):
        try:
            selenium.driver.get('https://www.instagram.com/p/%s' % post_id)
            selenium.driver.maximize_window()
            size = selenium.driver.execute_script("""
                                document.getElementsByTagName('nav')[0].remove();
                                if (document.getElementsByTagName('article').length > 0) return document.getElementsByTagName('article')[0].getBoundingClientRect();
                                return null;
                            """)

            time.sleep(1)
            png = selenium.driver.get_screenshot_as_png()

            im = Image.open(BytesIO(png))
            png_name = 'IG-%s' % post_id

            self.crop_img(im, png_name, size)
            selenium.driver.quit()
            return png_name
        except Exception as e:
            selenium.driver.quit()
            return None

    def crop_img(self, im, im_name, size):
        if size is not None:
            img_size = (int(size['x']), int(size['y']), int(size['x']) + int(size['width']), int(size['y']) + int(size['height']));
            # print(img_size)
            im = im.crop(img_size)
        x, y = im.size
        x2, y2 = math.floor(x / 1.5), math.floor(y / 1.5)
        im = im.resize((x2, y2), Image.ANTIALIAS)
        im.save('Screenshot/%s.png' % im_name, optimize=True, quality=90)
        return im_name
