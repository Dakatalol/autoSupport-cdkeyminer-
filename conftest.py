import logging
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

from utils.utils import Config

LOGGER.setLevel(logging.WARNING)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="", help="Type in browser type")


@pytest.fixture(scope="session")
def base_url():
    return "https://app.cdkeyminer.com/"


@pytest.fixture(scope='session')
def sensitive_url():
    return False


@pytest.mark.hookwrapper
@pytest.mark.usefixtures('driver')
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            selenium = item.funcargs['driver']
            url = selenium.current_url
            screenshot = selenium.get_screenshot_as_base64()
            if sys.version_info[0] < 3:
                report.extra.append(pytest_html.extras.url(url))
                report.extra.append(pytest_html.extras.image(screenshot, 'Screenshot'))
            else:
                extra.append(pytest_html.extras.url(url))
                extra.append(pytest_html.extras.image(screenshot, 'Screenshot'))
        report.extra = extra


@pytest.fixture(scope="session", autouse=True)
def driver(base_url, request):
    browser = request.config.getoption("--browser")
    drivers = sys.path[0] + "\\drivers"
    if not browser:
        browser = Config.BROWSER
    if browser == 'chrome':
        from webdriver_manager.chrome import ChromeDriverManager
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        browser = webdriver.Chrome(ChromeDriverManager().install(drivers), chrome_options=chrome_options)
    elif browser == 'firefox':
        from webdriver_manager.firefox import GeckoDriverManager
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(drivers))
    elif browser == 'ie':
        from webdriver_manager.microsoft import IEDriverManager
        caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
        caps['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
        browser = webdriver.Ie(IEDriverManager(os_type='Win32').install(drivers), desired_capabilities=caps)
    # elif browser == 'edge':
    #     from msedge.selenium_tools import Edge, EdgeOptions
    #     options_edge = EdgeOptions()
    #     options_edge.use_chromium = True
    #     options_edge.add_argument("--disable-backgrounding-occluded-windows")
    #     driver_path = '\\drivers\\MicrosoftWebDriver.exe'
    #     browser = Edge(driver_path, options=options_edge)
    # elif browser == 'remote':
    #     browser = webdriver.Remote(command_executor='url',
    #                                desired_capabilities=webdriver.DesiredCapabilities.CHROME)
    elif browser == 'headless':
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920,1080')
        browser = webdriver.Chrome(chrome_options=options)

    def teardown():
        browser.close()
        browser.quit()

    browser.maximize_window()
    browser.get(base_url)
    request.addfinalizer(teardown)
    return browser
