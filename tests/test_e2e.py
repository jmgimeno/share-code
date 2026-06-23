import pytest
from playwright.sync_api import BrowserContext, Page, expect


def test_submission_appears_in_show_tab(server_url: str, page: Page, context: BrowserContext):
    student = page
    teacher = context.new_page()

    student.goto(server_url)
    teacher.goto(server_url)

    student.fill("#display-name", "Alice")
    student.select_option("#language", "python")
    student.fill("#code-input", "print('hello')")
    student.click("#submit-btn")

    teacher.click("#tab-show")
    expect(teacher.locator("#submission-list")).to_contain_text("Alice")
    expect(teacher.locator("#code-display")).to_contain_text("print")


def test_first_submission_auto_selected(server_url: str, page: Page):
    page.goto(server_url)
    page.fill("#code-input", "x = 42")
    page.click("#submit-btn")
    page.click("#tab-show")

    expect(page.locator(".submission-item.selected")).to_be_visible()
    expect(page.locator("#code-display")).to_contain_text("x = 42")


def test_current_selection_stable_when_new_submission_arrives(
    server_url: str, page: Page, context: BrowserContext
):
    student = page
    teacher = context.new_page()

    student.goto(server_url)
    teacher.goto(server_url)
    teacher.click("#tab-show")

    student.fill("#code-input", "first = 1")
    student.click("#submit-btn")
    teacher.wait_for_selector(".submission-item.selected")

    student.fill("#code-input", "second = 2")
    student.click("#submit-btn")
    teacher.wait_for_selector(".submission-item:nth-child(2)")

    expect(teacher.locator("#code-display")).to_contain_text("first = 1")
    expect(teacher.locator(".submission-item.selected")).to_contain_text("1")


def test_submit_confirmation_appears_and_clears_textarea(server_url: str, page: Page):
    page.goto(server_url)
    page.fill("#code-input", "hello world")
    page.click("#submit-btn")

    expect(page.locator("#confirmation")).to_be_visible()
    expect(page.locator("#code-input")).to_have_value("")


def test_badge_increments_while_on_submit_tab(
    server_url: str, page: Page, context: BrowserContext
):
    sender = page
    receiver = context.new_page()

    sender.goto(server_url)
    receiver.goto(server_url)

    sender.fill("#code-input", "a = 1")
    sender.click("#submit-btn")
    sender.fill("#code-input", "b = 2")
    sender.click("#submit-btn")

    expect(receiver.locator("#badge")).to_have_text("2")


def test_badge_clears_on_switch_to_show_tab(
    server_url: str, page: Page, context: BrowserContext
):
    sender = page
    receiver = context.new_page()

    sender.goto(server_url)
    receiver.goto(server_url)

    sender.fill("#code-input", "x = 1")
    sender.click("#submit-btn")
    receiver.wait_for_selector("#badge:not(.hidden)")

    receiver.click("#tab-show")
    expect(receiver.locator("#badge")).to_have_class("badge hidden")


def test_localStorage_persists_name_and_language(server_url: str, page: Page):
    page.goto(server_url)
    page.fill("#display-name", "TestUser")
    page.select_option("#language", "rust")
    page.reload()

    expect(page.locator("#display-name")).to_have_value("TestUser")
    expect(page.locator("#language")).to_have_value("rust")
