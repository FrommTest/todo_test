import os

from playwright.sync_api import expect


def test_todo_url(todo_page):
    expect(todo_page).to_have_url(os.getenv('PAGE_URL'))
