from Facade.Selemium.Selenium import Selenium
from Configs.enum import ServerConfig
from CrawlerLib.Pymongo import MongodbClient
import pymongo


host_path = ServerConfig.IP_ADDRESS.value
port = '8080'


def test_selenium():
    Selenium.get_instance().screen_post('YT', '0RH0Xf3Iw5g')
    Selenium.get_instance().screen_post('YT', 'Nk-isYXzUsg')

    #Selenium.get_instance().screen_post('IG', 'BcNyJJLAGOe')
    #Selenium.get_instance().screen_post('IG', 'B2QTaIpJpfe')
    # print('http://188.166.220.11:8080/attachments/%s' % png_name)
    #Selenium.get_instance().screen_post('FB', '100003803082906_1486305034839585')
    #Selenium.get_instance().screen_post('FB', '100003803082906_1526300914173330')
    #Selenium.get_instance().screen_post('FB', '1780299330_10211727153172569')
    # print(png_name)
    # print('http://188.166.220.11:8080/attachments/%s' % png_name)

def test_insert():

    db = MongodbClient.get_instance()
    link_collection = db.get_link_collection()
    try:
        link_collection.insert({"link_id": "123", "type": "ins"})
    except Exception as e:
        print(e)

test_insert()
