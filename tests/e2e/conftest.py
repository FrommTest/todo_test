import os
import tempfile

from playwright.sync_api import Playwright
import pytest

from tests.e2e.utils.playwright_config import playwright_config_base, playwright_tear_down_base

HEADLESS = False
PAGE_URL = os.getenv('PAGE_URL', 'https://black-stone-05a57af00.2.azurestaticapps.net/')
LOGIN_URL = f'{PAGE_URL}login'  # f-string 사용


@pytest.fixture(scope='session')
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()


@pytest.fixture(scope='session')
def web_session_driver(browser, playwright: Playwright):
    context = browser.new_context()
    page = context.new_page()

    page.goto(PAGE_URL, wait_until='domcontentloaded')
    page.wait_for_url(LOGIN_URL)
    page.locator('#login-username').fill('admin')
    page.locator('#login-password').fill('admin1!')
    page.click('button.login-btn')
    page.wait_for_url(PAGE_URL)

    storage_file = tempfile.mktemp(suffix='.json')
    context.storage_state(path=storage_file)
    context.close()

    yield storage_file

    os.remove(storage_file)


@pytest.fixture
def todo_onyu_page(browser, playwright: Playwright, request, web_session_driver):
    no_cookie = request.node.get_closest_marker('no_cookie')

    storage = None if no_cookie else web_session_driver
    page, context, browser = playwright_config_base(playwright, PAGE_URL, browser, storage, headless=HEADLESS)
    try:
        yield page
    finally:
        playwright_tear_down_base(context)
