from playwright.sync_api import sync_playwright

def save_linkedin_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.linkedin.com/login")
        print("🔐 Please log in manually...")
        page.wait_for_timeout(60000) # 60 seconds for manual login
        # Save cookies and session state
        context.storage_state(path="linkedin_state.json")
        print("✅ Session saved to linkedin_state.json")
        browser.close()
if __name__ == "__main__":
    save_linkedin_session()
