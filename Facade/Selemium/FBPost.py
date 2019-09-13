from Facade.Selemium.IBase import IBase
from PIL import Image
from io import BytesIO
import time


class FBPost(IBase):
    def screen_post(self, _selenium, post_id):
        try:
            _selenium.driver.set_window_size(height=1080, width=1980)
            _selenium.driver.get('https://www.facebook.com/%s' % post_id)
            time.sleep(2)
            size = _selenium.driver.execute_script("""
                            if (document.getElementById('headerArea')) document.getElementById('headerArea').remove();
                            if (document.getElementById('pagelet_bluebar')) document.getElementById('pagelet_bluebar').remove();
                            if (document.getElementsByTagName('body').length > 0) document.getElementsByTagName('body')[0].style['marginBottom'] = "0px";
                            if (document.getElementById('rightCol')) document.getElementById('rightCol').remove();
                            if (document.getElementsByClassName('userContentWrapper').length > 0) {
                                return document.getElementsByClassName('userContentWrapper')[0].getBoundingClientRect();
                            }
                            return null;
                            """)
            png = _selenium.driver.get_screenshot_as_png()
            im = Image.open(BytesIO(png))
            png_name = 'FB-%s' % post_id

            self.crop_img(im, png_name, size)
            _selenium.driver.quit()
            return png_name
        except Exception as e:
            _selenium.driver.quit()
            return None

    def crop_img(self, im, im_name, size):
        if size is not None:
            img_size = (int(size['x']), int(size['y']), int(size['x']) + int(size['width']), int(size['y']) + int(size['height']))
            # print(img_size)
            im = im.crop(img_size)
        im.save('Screenshot/%s.png' % im_name)
        return im_name


