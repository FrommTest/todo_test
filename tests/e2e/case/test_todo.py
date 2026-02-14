import time

from playwright.sync_api import expect


def test_todo_url(todo_page):
    expect(todo_page).to_have_url('https://black-stone-05a57af00.2.azurestaticapps.net/')