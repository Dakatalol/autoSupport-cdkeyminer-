import pytest

from pages.login_page import Login


@pytest.mark.smoke
def test_verify_login_account_field_is_present(driver):
    Login(driver).logger.info("Verify login account field is present")
    Login(driver).navigate_to_login_page()
    assert Login(driver).is_element_present(Login._login_account_field)


def test_verify_login_password_field_is_present(driver):
    Login(driver).logger.info("Verify login password field is present")
    Login(driver).navigate_to_login_page()
    assert Login(driver).is_element_present(Login._login_password_field)


def test_verify_login_button_is_present(driver):
    Login(driver).logger.info("Verify login button is present")
    Login(driver).navigate_to_login_page()
    assert Login(driver).is_element_present(Login._login_login_button)


def test_verify_register_link_is_present(driver):
    Login(driver).logger.info("Verify register link is present")
    Login(driver).navigate_to_login_page()
    assert Login(driver).is_element_present(Login._register_link)


def test_verify_password_reset_link_is_present(driver):
    Login(driver).logger.info("Verify password reset link is present")
    Login(driver).navigate_to_login_page()
    assert Login(driver).is_element_present(Login._password_reset_link)


def test_verify_logo_is_present(driver):
    Login(driver).logger.info("Verify register link is present")
    Login(driver).navigate_to_login_page()
    assert Login(driver).is_element_present(Login._logo_image)


@pytest.mark.smoke
def test_verify_empty_fields_validation(driver):
    Login(driver).logger.info("Verify login field form validations for empty fields")
    Login(driver).navigate_to_login_page()
    Login(driver).click(Login._login_login_button)
    Login(driver).wait_for_page_loaded()
    Login(driver).wait_for_element_to_be_clickable(Login._login_error_field)
    assert "Username or password incorrect" in Login(driver).get_text(Login._login_error_field)


@pytest.mark.smoke
def test_verify_empty_account_validation(driver):
    Login(driver).logger.info("Verify login field form validations for empty account field")
    Login(driver).navigate_to_login_page()
    Login(driver).type(Login._login_account_field, "test")
    Login(driver).click(Login._login_login_button)
    Login(driver).wait_for_page_loaded()
    Login(driver).wait_for_element_to_be_clickable(Login._login_error_field)
    assert "Username or password incorrect" in Login(driver).get_text(Login._login_error_field)


@pytest.mark.smoke
def test_verify_empty_password_validation(driver):
    Login(driver).logger.info("Verify login field form validations for empty password field")
    Login(driver).navigate_to_login_page()
    Login(driver).type(Login._login_password_field, "test")
    Login(driver).click(Login._login_login_button)
    Login(driver).wait_for_page_loaded()
    Login(driver).wait_for_element_to_be_clickable(Login._login_error_field)
    assert "Username or password incorrect" in Login(driver).get_text(Login._login_error_field)


@pytest.mark.smoke
def test_verify_user_is_able_to_login(driver):
    Login(driver).logger.info("Verify user is logged in successfully")
    Login(driver).navigate_to_login_page()
    Login(driver).login("testacc", "159357")
    Login(driver).wait_for_element_to_be_clickable(Login._dashboard_menu_icon)
    is_logged = Login(driver).is_element_present(Login._dashboard_menu_icon)
    Login(driver).logout()
    Login(driver).wait_for_page_loaded()
    assert is_logged is True
