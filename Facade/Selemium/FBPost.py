from Facade.Selemium.IBase import IBase
from PIL import Image
from io import BytesIO
import time


class FBPost(IBase):
    def screen_post(self, _selenium, post_id):
        _selenium.driver.get('https://www.facebook.com/%s' % post_id)
        _selenium.driver.maximize_window()

        size = _selenium.driver.execute_script("""
                if (document.getElementById('headerArea')) document.getElementById('headerArea').remove();
                if (document.getElementById('pagelet_bluebar')) document.getElementById('pagelet_bluebar').remove();
                if (document.getElementsByTagName('body').length > 0) document.getElementsByTagName('body')[0].style['marginBottom'] = "0px";
                if (document.getElementById('rightCol')) document.getElementById('rightCol').remove();
                if (document.getElementById('contentArea')) {
                    return document.getElementById('contentArea').getBoundingClientRect();
                }
                return null;
                """)
        print(size)
        time.sleep(2)
        png = _selenium.driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        png_name = 'FB-%s' % post_id
        img_size = (int(size['x']), int(size['y']), int(size['x']) + int(size['width']), int(size['y']) + int(size['height']));
        print(img_size)
        im.crop(img_size).save('Screenshot/%s.png' % png_name)
#        _selenium.driver.quit()
        return png_name

