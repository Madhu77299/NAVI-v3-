from playwright.sync_api import sync_playwright
import time

def scrape_linkedin_feed(keywords):
    posts = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(storage_state="linkedin_state.json")
        page = context.new_page()

        page.goto("https://www.linkedin.com/feed/")
        page.wait_for_selector("div.feed-shared-update-v2", timeout=30000)
        time.sleep(5)

        feed_items = page.query_selector_all("div.feed-shared-update-v2")[:15]

        for item in feed_items:
            try:
                text = item.inner_text().lower()
                link_element = item.query_selector("a.app-aware-link")
                link = link_element.get_attribute("href") if link_element else "#"

                poster = item.query_selector("span.feed-shared-actor__description")
                poster_text = poster.inner_text().lower() if poster else ""

                if any(k.lower() in text for k in keywords) and ("hr" in poster_text or "recruiter" in poster_text):
                    posts.append({
                        "title": text[:80].replace("\n", " ") + "...",
                        "link": link,
                        "source": "LinkedIn Post"
                    })
            except:
                continue

        browser.close()
    return posts