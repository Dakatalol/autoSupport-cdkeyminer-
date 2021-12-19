import inspect
import logging
import os
import time
from datetime import datetime

from selenium.common.exceptions import (NoAlertPresentException, NoSuchElementException, TimeoutException,
                                        WebDriverException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from utils.utils import Config
from .decorators import log_exception

if os.path.exists(Config.RESULT_PATH):
    fileList = os.listdir(Config.RESULT_PATH)
    for fileName in fileList:
        try:
            os.remove(Config.RESULT_PATH + "\\" + fileName)
        except:
            print('failed to remove result file {}'.format(Config.RESULT_PATH + "\\" + fileName))
            pass
else:
    os.makedirs(Config.RESULT_PATH)

result_file = Config.RESULT_PATH + "\\" + Config.TIME_NOW + ".log"
logging.basicConfig(filename=result_file, level=logging.INFO)
pil_log = logging.getLogger('PIL')
pil_log.setLevel(logging.INFO)


class BasePage(object):
    """
    Base page representation.
    Contains all actions related to UI interaction.
    All pages may be inherited from this class.
    """

    def __init__(self, driver, results):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.timeout = 15

    @log_exception('Failed to get web element with xpath: {}')
    def _get_element(self, element, expected_condition=expected_conditions.presence_of_element_located, wait=None):
        if wait is None:
            wait = self.timeout
        if isinstance(element, str):
            ####
            if self.driver.name in 'internet explorer':
                self.wait_for_page_loaded()
            ####
            wd_wait = WebDriverWait(self.driver, wait)
            element = wd_wait.until(expected_condition((By.XPATH, element)))
        if element:
            try:
                self._highlight(element)
            except:
                pass
        return element

    def _highlight(self, element):
        if not Config.HIGHLIGHT:
            pass
        else:  # highlight differently according to what you are trying to do to the element
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            try:
                if 'get_text' in calframe[3][3]:
                    self.execute_script(
                        'setAttribute("style", "background-color: goldenrod; outline: solid darkorange;");', element)
                    time.sleep(.05)
                    self.execute_script('setAttribute("style", null);', element)
                elif '_get_element' in calframe[1][3]:
                    self.execute_script('setAttribute("style", "color: red; outline: red dotted;");', element)
                    time.sleep(.05)
                    self.execute_script('setAttribute("style", null);', element)
            except:
                pass

    @log_exception('Failed to get web elements with xpath: {}')
    def get_elements(self, xpath):
        self._get_element(xpath)
        elements = self.driver.find_elements_by_xpath(xpath)
        return elements

    @log_exception('Failed presence check of web element with xpath: {}')
    def wait_for_element_present(self, xpath, wait=None):
        expected_condition = expected_conditions.presence_of_element_located
        if self._get_element(xpath, expected_condition, wait):
            self.logger.info('element {} is present, wait: {}'.format(xpath, wait))
            return True

    @log_exception('Failed presence check of web element with xpath: {}')
    def is_present(self, xpath, wait=None, expected=True):
        found = False
        expected_condition = expected_conditions.presence_of_element_located
        if not expected:
            expected_condition = expected_conditions.staleness_of
        found = self._get_element(xpath, expected_condition, wait) is not None
        if Config.HIGHLIGHT:
            self._highlight(self._get_element(xpath, expected_condition, wait))
        self.logger.info('element {} is present: expected: {} , wait: {}'.format(xpath, expected, wait))
        return found

    @log_exception('Failed visible check of web element with xpath: {}')
    def is_visible(self, xpath, wait=None, expected=True):
        expected_condition = expected_conditions.visibility_of_element_located
        if not expected:
            expected_condition = expected_conditions.invisibility_of_element_located
        found = self._get_element(xpath, expected_condition, wait).is_displayed()
        self.logger.info('element {} is visible: expected: {} , wait: {}'.format(xpath, expected, wait))
        return found

    def is_stale(self, xpath):
        element = self._get_element(xpath)
        for i in range(5):
            if expected_conditions.staleness_of(element):
                self.logger.info("element is stale: {}.".format(xpath))
                return True
            else:
                time.sleep(1)
        self.logger.info("element is not stale after 5 seconds: {}.".format(xpath))
        return False

    @log_exception('Failed to click web element with xpath: {}')
    def click(self, xpath):
        try:
            self.logger.info("clicking element with text '{}' and href of '{}'".format(self.get_text(xpath),
                                                                                       self.get_attribute(xpath,
                                                                                                          'href')))
        except:
            pass
        self._get_element(xpath, expected_conditions.element_to_be_clickable).click()

    def click_and_wait(self, xpath_click, xpath_wait, wait=1):
        i = 0
        while not self.is_element_present(xpath_wait):
            self.click(xpath_click)
            i += 1
            time.sleep(wait)
            if i > 10:
                self.logger.info(
                    "Expected element {} not present within {} seconds after clicking {}.".format(xpath_wait, wait,
                                                                                                  xpath_click))
                return False
        return True

    def is_clickable(self, xpath):
        if self._get_element(xpath, expected_conditions.element_to_be_clickable):
            self.logger.info('element {} is clickable'.format(xpath))
            return True
        self.logger.info("element is not clickable: {}.".format(xpath))
        return False

    @log_exception('Failed to type text into web element with xpath: {}')
    def type(self, xpath, text):
        if 'Login' not in self.__class__.__name__:  # let's not log the passwords when logging in
            self.logger.info('Type "{}" into field with xpath: {}'.format(text, xpath))
        self._get_element(xpath, expected_conditions.visibility_of_element_located).send_keys(text)

    def is_active(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        return element.is_enabled()

    def wait_for_element_to_disappear(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        WebDriverWait(self.driver, 15).until(expected_conditions.invisibility_of_element_located(element))

    def wait_for_element_to_be_clickable(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        WebDriverWait(self.driver, 20).until(expected_conditions.visibility_of(element))

    def execute_script(self, script, element=""):
        if not element:
            # self.logger.info("execute script: '{}'".format(script))   # this becomes too noisy in the logs
            return self.driver.execute_script(format(script))
        else:
            # self.logger.info("execute script: '{}' on element '{}'".format(script, element))  ## too noisy in the logs
            return self.driver.execute_script("return arguments[0].{}".format(script), element)

    @log_exception('Failed to mouse over web element with xpath: {}')
    def mouse_over(self, xpath):
        actions = ActionChains(self.driver)
        actions.move_to_element(self._get_element(xpath)).perform()
        self.logger.info('move mouse over element {}'.format(xpath))

    @log_exception('Failed to mouse over web element with xpath: {}')
    def mouse_double_click(self, xpath):
        actions = ActionChains(self.driver)
        actions.double_click(self._get_element(xpath)).perform()
        self.logger.info('double click on element {}'.format(xpath))

    @log_exception('Failed open URL: {}')
    def open(self, url):
        self.driver.get(url)
        self.logger.info('Opened URL: {}'.format(url))

    @log_exception('Cannot switch to frame: {}')
    def switch_to_frame(self, xpath):
        self.logger.info('switch to frame xpath {}'.format(xpath))
        self.driver.switch_to.frame(self._get_element(xpath))

    @log_exception('frame was not found')
    def switch_to_frame_when_available(self, element,
                                       expected_condition=expected_conditions.frame_to_be_available_and_switch_to_it,
                                       wait=None):
        i = 0
        while i < 10:
            i += 1
            try:
                self.driver.switch_to.frame(self.driver.find_element_by_xpath(element))
                self.logger.info('successful switch to frame {}'.format(element))
                break
            except WebDriverException:
                self.switch_to_default_frame()
                self.logger.info('unsuccessful switch to frame {}, switching back to default frame'.format(element))

    @log_exception('Cannot switch to default frame')
    def switch_to_default_frame(self):
        self.driver.switch_to.default_content()
        time.sleep(.5)
        self.logger.info('successful switch to default frame')

    @log_exception('Cannot get text located: {}')
    def get_text(self, xpath):
        try:
            self.logger.info("found text: '{}' for element '{}'".format(self._get_element(xpath).text, xpath))
        except:
            pass
        return self._get_element(xpath).text

    @log_exception('Cannot send_keys to the web element with xpath: {}')
    def send_keys(self, xpath, key):
        self._get_element(xpath).send_keys(key)
        try:
            self.logger.info('send keys: {} to element {}'.format(key, xpath).encode("utf-8"))
        except:
            pass

    def get_selected_text(self, xpath):
        text = 'Text Not Found'
        for option in self.get_elements(xpath + "/option"):
            if self.execute_script('selected', option):
                text = self.execute_script('text', option)
                self.logger.info('text {} is currently selected for xpath: {}'.format(text, xpath))
                break
        return text

    def is_selected(self, xpath):
        self.logger.info('xpath {} is selected? {}'.format(xpath, self._get_element(xpath).is_selected()))
        return self._get_element(xpath).is_selected()

    def get_attribute(self, xpath, attribute):
        target_attribute = self._get_element(xpath).get_attribute(attribute)
        try:
            self.logger.info(
                "attribute '{} ' from element with  xpath: {} is '{}'".format(attribute, xpath, target_attribute))
        except:
            self.logger.info("attribute '{}' from element with  xpath: {} ".format(attribute, xpath))
        return target_attribute

    def clear(self, xpath):
        i = 0
        while i < 10:
            i += 1
            try:
                self._get_element(xpath).clear()
                self.logger.info('cleared text from element {}'.format(xpath))
                break
            except WebDriverException:
                pass

    def select_value(self, xpath, value):
        i = 0
        while i < 10:
            i += 1
            try:
                Select(
                    self._get_element(xpath)).select_by_value(value)
                self.logger.info('selected value {} from select{}'.format(value, xpath))
                break
            except WebDriverException:
                pass

    def select_text(self, xpath, text):
        i = 0
        while i < 10:
            i += 1
            try:
                Select(
                    self._get_element(xpath)).select_by_visible_text(text)
                self.logger.info('selected text {} from select{}'.format(text, xpath))
                break
            except WebDriverException:
                pass
        self.logger.info('failed to select text {} from select{}'.format(text, xpath))

    def select_index(self, xpath, index):
        i = 0
        while i < 10:
            i += 1
            try:
                Select(
                    self._get_element(xpath)).select_by_index(int(index))
                self.logger.info('selected index {} from select{}'.format(index, xpath))
                return True
            except WebDriverException:
                # pass
                return False
        self.logger.info('failed to select index {} from select{}'.format(index, xpath))

    def select_last_index(self, xpath):
        select = Select(self._get_element(xpath))
        select_len = len(select.options)
        select.select_by_index(select_len - 1)

    def deselect_all(self, xpath):
        i = 0
        while i < 10:
            i += 1
            try:
                Select(self._get_element(xpath)).deselect_all()
                self.logger.info('deselected all from {}'.format(xpath))
                break
            except WebDriverException:
                pass

    def close_alert_and_get_its_text(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(expected_conditions.alert_is_present())
            for i in range(5):
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                self.logger.info("alert closed: %s" % alert_text)
                self.wait_for_lifeline()
        except NoAlertPresentException:
            return alert_text
        except TimeoutException:
            self.logger.error('no alert found')

    def is_alert_present(self):
        try:
            WebDriverWait(self.driver, 5).until(expected_conditions.alert_is_present())
            alert = self.driver.switch_to.alert
            self.logger.error('alert found')
            yield True
            self.switch_to_default_frame()
        except TimeoutException:
            yield False

    def hover(self, xpath):
        hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(xpath))
        hover.perform()
        self.logger.info('hover performed'.format(xpath))

    def move_slider(self, xpath, x, y):
        move = ActionChains(self.driver).drag_and_drop_by_offset(self.driver.find_element_by_xpath(xpath), x, y)
        move.perform()
        self.logger.info('moving slider by x:{} and y{}'.format(x, y))

    def move_to_element(self, xpath):
        move = ActionChains(self.driver).move_to_element(xpath)
        move.perform()
        self.logger.info('move mouse to element{}'.format(xpath))

    def is_element_present(self, xpath):
        self.driver.implicitly_wait(0)
        try:
            if self.driver.find_element_by_xpath(xpath):
                self.logger.info("Presence check for element:'{}' is successful".format(xpath))
                return True
        except NoSuchElementException:
            self.logger.info("Presence check for element:'{}' is not successful".format(xpath))
            return False
        finally:
            self.driver.implicitly_wait(10)

    def element_height(self, xpath):
        self.logger.info("element {} height: {}".format(xpath, self._get_element(xpath).size['height']))
        return self._get_element(xpath).size['height']

    def element_width(self, xpath):
        self.logger.info("element {} width: {}".format(xpath, self._get_element(xpath).size['width']))
        return self._get_element(xpath).size['width']

    def is_page_loaded(self, script2=""):
        if script2:
            page_state = self.driver.execute_script(script2)
        else:
            page_state = self.driver.execute_script('return document.readyState;')
        self.logger.info("page is loaded")
        return page_state == 'complete'

    def wait_for_page_loaded(self, script=""):
        self.logger.info('wait for page to load')
        if script:
            WebDriverWait(self.driver, self.timeout).until(lambda s: self.is_page_loaded(script2=script))
        else:
            WebDriverWait(self.driver, self.timeout).until(lambda s: self.is_page_loaded)

    def browser_back(self):
        self.driver.back()
        self.logger.info('Browser BACK command')

    @log_exception('Failed to move by offset')
    def move_by_offset(self, x, y):
        actions = ActionChains(self.driver)
        actions.move_by_offset(x, y).perform()
        self.logger.info('moved cursor by offset')

    @log_exception('Failed to mouse click')
    def mouse_click(self):
        actions = ActionChains(self.driver)
        actions.click().perform()
        self.logger.info('performed a mouse click where the cursor was located')

    @log_exception('Failed to click and hold')
    def mouse_click_and_hold(self, xpath):
        actions = ActionChains(self.driver)
        actions.click_and_hold(self._get_element(xpath)).perform()
        self.logger.info('performed a click and hold')

    @log_exception('Failed release mouse')
    def mouse_release(self, xpath=''):
        actions = ActionChains(self.driver)
        if xpath:
            actions.release(self._get_element(xpath)).perform()
        else:
            actions.release().perform()
        self.logger.info('performed a click and hold')

    def save_screenshot(self, path):
        self.driver.save_screenshot(path)
        self.logger.info("saved screenshot")

    def get_window_size(self):
        self.logger.info("window size: %s" % self.driver.get_window_size())
        return self.driver.get_window_size()

    def scroll_into_view(self, element):
        self.execute_script('scrollIntoView(true);', element)
        self.logger.info("element scrolled into view: %s" % element)

    def wait_for_ajax(self):
        for i in range(30):
            ajaxIsComplete = self.driver.execute_script("return jQuery.active == 0")
            if ajaxIsComplete:
                self.logger.info("return jQuery.active == 0 is TRUE")
                break
            time.sleep(1)
        # self.logger.info("Failed after 30 tries: return jQuery.active == 0 is TRUE")

    def wait_for_lifeline(self):
        if self.is_element_present("//iframe[@id='LifeLine_iframe']"):
            time.sleep(1)
        for i in range(100):
            try:
                if self.is_element_present("//iframe[@id='LifeLine_iframe']"):
                    self.logger.info("Lifeline loaded")
                    return True
                else:
                    time.sleep(.1)
                    continue
            except NoSuchElementException:
                self.logger.info("LifeLine never loaded")
                return False
        if i >= 99:
            self.logger.info("Lifeline never loaded")
            return False

    def uncheck_all(self, xpath):
        selects = self.driver.find_elements_by_xpath(xpath)
        for select in selects:
            if self.driver.execute_script("return arguments[0].checked", select):
                select.click()
                self.logger.info("element was deselected: {}".format(xpath))

    def current_url(self):
        return self.driver.current_url

    def url_contains(self, text):
        return expected_conditions.url_contains(text)

    def page_title(self):
        return self.driver.title

    def get_page_header_text(self):
        self.logger.info("Find page header text")
        if self.is_element_present("//td[@class='page_header']"):
            return self.get_text("//td[@class='page_header']")
        elif self.is_element_present("//div[@class='page_header']"):
            return self.get_text("//div[@class='page_header']")
        else:
            return "header not found"

    def get_test_info(self):
        try:
            self.logger.info("current url : %s" % str(self.driver.current_url))
        except:
            self.logger.info('current url not found{}')
        try:
            self.logger.info("Page Title: %s" % self.driver.title)
        except:
            self.logger.info('Page Title not found{}')
        try:
            if self.is_element_present("//td[@class='user_name']"):
                self.logger.info("userID : %s" % self.get_text("//td[@class='user_name']"))
            else:
                self.logger.info("userID : %s" % self.get_attribute("//div[@id='profile-tooltip']", 'data-title'))
        except:
            self.logger.info('userID not found{}')
        try:
            self.logger.info("Browser: %s" % str(self.driver.name))
        except:
            self.logger.info('Browser not found{}')

    def maximize_browser(self):
        self.driver.maximize_window()

    def refresh_browser(self):
        self.logger.info("refresh browser")
        self.driver.refresh()

    def add_cookie(self, cookie):
        self.driver.add_cookie(cookie)

    def get_cookies(self):
        return self.driver.get_cookies()

    def is_checked(self, xpath):
        is_element_checked = self.driver.execute_script("return arguments[0].checked", self._get_element(xpath))
        self.logger.info('element {} is checked = {}'.format(xpath, is_element_checked))
        return is_element_checked

    def get_list_of_numbers_from_string_regex(self, string):
        import re
        r = re.compile('[0-9]+')
        self.logger.info('found numbers {} in string {}'.format(r.findall(string), string))
        return r.findall(string)

    def compare_lists(self, expected, actual):
        results = []
        for e in expected:
            if e in actual:
                pass
            else:
                results.append('did not find in actual list: ' + format(e))
        for a in actual:
            if a in expected:
                pass
            else:
                results.append('did not find in expected list: ' + format(a))
        if len(results) == 0:
            self.logger.info("expected list values = actual list values")
            return True
        else:
            print('expected: ', expected)
            print('actual:   ', actual)
            return False

    def myclick(self, locator):
        element = self.driver.find_element_by_xpath(locator)
        return self.driver.execute_script("arguments[0].click();", element)

    def space_click(self, locator):
        return self.driver.find_element_by_xpath(locator).send_keys(Keys.SPACE)

    def get_current_hour(self):
        return int(datetime.now().hour)
