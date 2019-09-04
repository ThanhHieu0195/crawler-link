from CrawlerLib.helper import get_utc_time
from Facade.Selemium.IBase import IBase
from PIL import Image
from io import BytesIO
import time
from selenium import webdriver


class FBPost(IBase):
    def screen_post(self, _selenium, post_id):
        _selenium.driver.get('https://www.facebook.com/%s' % post_id)
        _selenium.driver.maximize_window()
        _selenium.driver.execute_script("""
                document.getElementById('headerArea').remove();
                document.getElementById('pagelet_bluebar').remove();
                window.scrollTo(0, document.body.scrollHeight);
                document.getElementsByTagName('body')[0].style['marginBottom'] = "0px";
                return screen.height;
                """)

        e = _selenium.driver.find_element_by_id('contentArea')
        location = e.location
        size = e.size

        png = _selenium.driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))

        left = location['x']
        top = 0
        right = location['x'] + size['width']

        im = im.crop((left, top, right, im.height))

        png_name = '%s-%s' % (get_utc_time('%Y%m%d%H%M'), post_id)
        im.save('Screenshot/%s.png' % png_name)
        _selenium.driver.quit()
        return png_name

