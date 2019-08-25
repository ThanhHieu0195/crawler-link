# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re
import requests
import pprint
import json
regex = r"window._sharedData = {(.*)};</script>"
test_str=requests.get('https://www.instagram.com/p/BsLBV22AzyT/').text
matches = re.findall(regex, test_str, re.DOTALL)
if matches:
    # data=json.loads('{'+matches[0]+'}')
    f=open('/home/hieutct/syn/crawler-link/data.json', 'w')
    f.write('{'+matches[0]+'}')
    f.close()

