from playwright.sync_api import sync_playwright

def scrape_jobs(keyword):
    print(f"🌐 Scraping: https://www.linkedin.com/jobs/search/?keywords={keyword}&f_TPR=r86400")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(storage_state="linkedin_state.json")
        context = browser.new_context(
            storage_state="linkedin_state.json", # ✅ Reuse login session
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
            )
        page = context.new_page()
        page.goto(f"https://www.linkedin.com/jobs/search/?keywords={keyword}&f_TPR=r86400")
        page.wait_for_timeout(500)
        try:
            page.wait_for_selector("ul.jobs-search__results-list li", timeout=10000)
            print(f"✅ Loaded job results for '{keyword}'")
        except Exception as e:
            print(f"⚠️ Failed to scrape LinkedIn for '{keyword}':", e)
        browser.close()

if __name__ == "__main__":
    for kw in ["hiring", "internship", "job opening", "software engineer"]:
        scrape_jobs(kw)
# from playwright.sync_api import sync_playwright

# def scrape_linkedin(keywords):
#     jobs = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=300)
#         context = browser.new_context(storage_state="linkedin_state.json")
#         page = context.new_page()

#         for keyword in keywords:
#             query = keyword.replace(" ", "%20")
#             url = f"https://www.linkedin.com/jobs/search/?keywords={query}&f_TPR=r86400"
#             print(f"🌐 Scraping: {url}")
#             page.goto(url)

#             # ⏳ Wait for job result list
#             try:
#                 page.wait_for_selector("ul.jobs-search__results-list li", timeout=20000)
#                 cards = page.query_selector_all("ul.jobs-search__results-list li")[:5]

#                 for card in cards:
#                     title_tag = card.query_selector("h3")
#                     company_tag = card.query_selector("h4")
#                     link_tag = card.query_selector("a")

#                     title = title_tag.inner_text().strip() if title_tag else "No title"
#                     company = company_tag.inner_text().strip() if company_tag else "Unknown company"
#                     link = link_tag.get_attribute("href") if link_tag else "#"

#                     jobs.append({
#                         "title": f"{title} at {company}",
#                         "link": link,
#                         "source": "LinkedIn"
#                     })

#             except Exception as e:
#                 print(f"⚠️ Failed to scrape LinkedIn for '{keyword}': {e}")

#         browser.close()
#     return jobs
# if __name__ == "__main__":
#     keywords = ["hiring", "internship", "job opening", "software engineer"]
#     jobs = scrape_linkedin(keywords)
#     for job in jobs:
#         print(f"🔹 {job['title']}\n🔗 {job['link']}\n") 
