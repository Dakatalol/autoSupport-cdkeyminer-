from core.base_page import BasePage
import logging


class Login(BasePage):
    _login_account_field = "//input[@id='loginUsername']"
    _login_password_field = "//input[@id='loginPassword']"
    _login_login_button = "//button[@id='login']"
    _login_error_field = "//*[@id='loginError']"
    _register_link = "//p[@id='registerPrompt']/a[@href='#registerForm']"
    _password_reset_link = "//p[@id='registerPrompt']/a[@href='#pwResetForm']"
    _logo_image = "//div[@id='loginForm']/img[@class='logo']"
    _dashboard_menu_icon = "//div[@id='menuButton']/i"
    _dashboard_logo = "//div[@id='dashboard']/img[@class='logo']"
    _dashboard_menu_button = "//div[@id='menuButton']"
    _dashboard_logout_button = "//div[@id='logoutBtn']"

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.timeout = 5

    # def login_override(driver, user=''):  # use this when you are not conforming to the created user
    #

    def login(self, acc, pw):
        self.navigate_to_login_page()
        self.type(self._login_account_field, acc)
        self.type(self._login_password_field, pw)
        self.click(self._login_login_button)
        self.wait_for_page_loaded()

    def navigate_to_login_page(self):
        self.driver.get("https://app.cdkeyminer.com/#loginForm")

    def logout(self):
        try:
            self.click(self._dashboard_menu_button)
            self.is_clickable(self._dashboard_logout_button)
            self.click(self._dashboard_logout_button)
            self.wait_for_page_loaded()
            self.driver.get("https://app.cdkeyminer.com/#registerForm")
        except:
            pass
