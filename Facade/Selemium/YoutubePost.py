from CrawlerLib.helper import get_utc_time
from Facade.Selemium.IBase import IBase
from PIL import Image
from io import BytesIO
import time


class YoutubePost(IBase):
    height = 1500
    width = 1200

    def screen_post(self, selenium, post_id):
        try:
            selenium.driver.set_window_size(self.width, self.height)
            selenium.driver.get('https://www.youtube.com/watch?v=%s' % post_id)
            time.sleep(2)
            size = selenium.driver.execute_script("""
                            if (document.getElementById('comments')) document.getElementById('comments').remove();
                            if (document.getElementById('primary-inner')) return document.getElementById('primary-inner').getBoundingClientRect();
                            return null;
                            """)
            png = selenium.driver.get_screenshot_as_png()
            im = Image.open(BytesIO(png))
            png_name = 'YT-%s' % post_id

            self.crop_img(im, png_name, size)
            selenium.driver.quit()
            return png_name
        except Exception as e:
            selenium.driver.quit()
            return None

    def crop_img(self, im, im_name, size):  
        if size is not None:  
            img_size = (int(size['x']), int(size['y']), int(size['x']) + int(size['width']), int(size['y']) + int(size['height']));  
            im = im.crop(img_size)
        im.save('Screenshot/%s.png' % im_name)  
        return im_name
