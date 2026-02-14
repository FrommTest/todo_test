import os

from playwright.sync_api import Playwright
import pytest

from tests.e2e.utils.playwright_config import playwright_config_base, playwright_tear_down_base

HEADLESS = False
PAGE_URL = os.getenv('PAGE_URL')


@pytest.fixture(scope='session')
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()


def do_sign_in(page):
    page.goto(PAGE_URL)
    page.locator('#login-username').fill(os.getenv('ID'))
    page.locator('#login-password').fill(os.getenv('PW'))
    page.get_by_text("로그인",exact=True).click()


@pytest.fixture
def set_up(browser) -> str:
    context = browser.new_context()
    page = context.new_page()
    do_sign_in(page)
    context.storage_state(path='state.json')
    context.close()
    return 'state.json'


@pytest.fixture
def todo_page(browser, playwright: Playwright, request, set_up):
    no_cookie = request.node.get_closest_marker('no_cookie')

    storage = None if no_cookie else set_up
    page, context, browser = playwright_config_base(playwright, PAGE_URL, browser, storage, headless=HEADLESS)
    try:
        yield page
    finally:
        playwright_tear_down_base(context)
