"""
Created on 30/08/2021
@author: dancho
"""
import configparser
import sys
import os
import datetime
import selenium.webdriver as webdriver


class Config(object):
    """
    Config class for storing values from config.ini and browser types.
    """
    browser_types = \
        dict(chrome=webdriver.Chrome, firefox=webdriver.Firefox, ie=webdriver.Ie,  edge=webdriver.Edge,
             phantomjs=webdriver.PhantomJS)
    config = configparser.ConfigParser()
    config.read(sys.path[0] + "\\pytest.ini")

    BROWSER = config.get('SELENIUM', 'Browser').lower()
    HIGHLIGHT = config.getboolean('SELENIUM', 'Highlight')
    REUSE = config.getboolean('SELENIUM', 'Reuse')
    USE_TEMP_USER = config.getboolean('USER_SETUP', 'use_temp_user')
    TEMP_USER_ADMIN_NAME = config.get('USER_SETUP', 'admin_name')
    TEMP_USER_ADMIN_PASS = config.get('USER_SETUP', 'admin_pass')
    DELETE_TEMP_USER = config.getboolean('USER_SETUP', 'delete_temp_user')

    TIMEOUT = config.getint('SELENIUM', 'Timeout')
    RESULT_PATH = os.path.join(sys.path[0] + "\\" + "results")
    TIME_NOW = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
