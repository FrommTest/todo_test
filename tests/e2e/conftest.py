import os

from playwright.sync_api import Playwright
import pytest

from tests.e2e.utils.playwright_config import playwright_config_base, playwright_tear_down_base

HEADLESS = False

PAGE_URL = os.getenv('PAGE_URL', 'https://gray-cliff-009510f00.4.azurestaticapps.net/')


@pytest.fixture(scope='session')
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=HEADLESS)

    yield browser

    browser.close()


@pytest.fixture(scope='session')
def logged_in(browser):
    context = browser.new_context()
    page = context.new_page()

    page.goto(PAGE_URL)

    id_input = page.locator('#login-username')
    pw_input = page.locator('#login-password')

    id_input.fill('admin')
    pw_input.fill('admin1!')

    page.click("button[type='submit']")

    yield context

    context.close()


@pytest.fixture
def jinsol_test(browser, playwright: Playwright, request):
    # no_cookie = request.node.get_closest_marker('no_cookie')
    # storage = None if no_cookie else web_session_driver
    page, context, browser = playwright_config_base(playwright, PAGE_URL, browser, headless=HEADLESS)

    try:
        yield page

    finally:
        playwright_tear_down_base(context)
