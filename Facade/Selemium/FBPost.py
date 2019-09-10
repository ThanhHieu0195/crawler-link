from Facade.Selemium.IBase import IBase
from PIL import Image
from io import BytesIO


class FBPost(IBase):
    def screen_post(self, _selenium, post_id):
        _selenium.driver.get('https://www.facebook.com/%s' % post_id)
        _selenium.driver.maximize_window()
        size = _selenium.driver.execute_script("""
                let height = 1080;
                let width = 800;
                if (document.getElementById('headerArea')) document.getElementById('headerArea').remove();
                if (document.getElementById('pagelet_bluebar')) document.getElementById('pagelet_bluebar').remove();
                if (document.getElementsByTagName('body').length > 0) document.getElementsByTagName('body')[0].style['marginBottom'] = "0px";
                if (document.getElementById('contentArea')) {
                    height = document.getElementById('contentArea').offsetHeight;
                    width = document.getElementById('contentArea').offsetWidth;
                }
                return {
                    height: height,
                    width: width
                };
                """)
        print('Size: w%s - h%s' % (size['width'], size['height']))
        _selenium.driver.set_window_size(size['width'] + 100, size['height'])

        _selenium.driver.execute_script("""
                if (document.getElementById('contentArea')) document.getElementById('contentArea').scrollIntoView();
        """)

        png = _selenium.driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        png_name = 'FB-%s' % post_id
        im.save('Screenshot/%s.png' % png_name)
        _selenium.driver.quit()
        return png_name

