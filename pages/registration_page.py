from core.base_page import BasePage
import logging


class Registration(BasePage):
    _username_field = "//input[@id='registerUsername']"
    _password_field = "//input[@id='registerPassword']"
    _repeat_password_field = "//input[@id='repeatPassword']"
    _email_field = "//input[@id='registerEmail']"
    _terms_and_condition_check_box = "//input[@id='agreeTos']"
    _privacy_policy_check_box = "//input[@id='agreePriv']"
    _i_am_18_years_older_check_box = "//input[@id='agree18']"
    _register_button = "//button[@id='register']"
    _validation_error_username = "//p[@id='registerUsernameError']"
    _validation_error_password = "//p[@id='registerPasswordError']"
    _validation_must_agree_to_terms = "//p[@id='registerTOSError']"
    _validation_for_age = "//p[@id='registerTOSError']"
    _validation_password_doesnt_match = "//p[@id='registerPasswordError']"
    _validation_invalid_email = "//p[@id='registerEmailError']"
    _terms_and_condition_link = "/html/body/div[2]/div[2]/p[6]/a"
    _privacy_policy_link = "/html/body/div[2]/div[2]/p[7]/a"
    _download_button = "//button[@class='downloadButton formButton']"

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.timeout = 5

    def register(self, acc, pw, rpw, email):
        self.navigate_to_register_page()
        self.type(self._username_field, acc)
        self.type(self._password_field, pw)
        self.type(self._repeat_password_field, rpw)
        self.type(self._email_field, email)
        self.click(self._terms_and_condition_check_box)
        self.click(self._privacy_policy_check_box)
        self.click(self._i_am_18_years_older_check_box)
        self.click(self._register_button)
        self.wait_for_page_loaded()

    def navigate_to_register_page(self):
        self.driver.get("https://app.cdkeyminer.com/#registerForm")

