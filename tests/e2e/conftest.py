import os
from pathlib import Path
import tempfile

from playwright.sync_api import Playwright
import pytest

from tests.e2e.utils.playwright_config import playwright_config_base, playwright_tear_down_base

HEADLESS = False
PAGE_URL = os.getenv('PAGE_URL', 'https://black-stone-05a57af00.2.azurestaticapps.net/')
LOGIN_URL = f'{PAGE_URL.rstrip("/")}/login'  # f-string 사용


@pytest.fixture(scope='session')
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()


@pytest.fixture(scope='session')
def web_session_driver(browser, playwright: Playwright):
    temp_browser = browser.new_context()  # 임시 브라우저 세션 생성
    temp_page = temp_browser.new_page()

    temp_page.goto(PAGE_URL, wait_until='domcontentloaded')
    temp_page.wait_for_url(LOGIN_URL)
    temp_page.locator('#login-username').fill('admin')
    temp_page.locator('#login-password').fill('admin1!')
    temp_page.click('button.login-btn')
    temp_page.wait_for_url(PAGE_URL)

    cookie_file = tempfile.mktemp(suffix='.json')
    temp_browser.storage_state(path=cookie_file)
    temp_browser.close()

    yield cookie_file

    Path(cookie_file).unlink(missing_ok=True)


@pytest.fixture
def todo_onyu_page(browser, playwright: Playwright, request, web_session_driver):
    no_cookie = request.node.get_closest_marker('no_cookie')

    storage = None if no_cookie else web_session_driver
    page, context, browser = playwright_config_base(playwright, PAGE_URL, browser, storage, headless=HEADLESS)
    try:
        yield page
    finally:
        playwright_tear_down_base(context)
