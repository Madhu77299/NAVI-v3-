# linkedin_login.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    print("🔐 Please log in to LinkedIn manually...")
    page.goto("https://www.linkedin.com/login")
    input("✅ After logging in and reaching your feed, press Enter to save session...")
    context.storage_state(path="linkedin_state.json")
    print("✅ LinkedIn session saved.")
    browser.close()
    