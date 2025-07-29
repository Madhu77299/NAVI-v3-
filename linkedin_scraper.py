from playwright.sync_api import sync_playwright
import json

def scrape_jobs(keyword):
    print(f"\n🌐 Scraping: https://www.linkedin.com/jobs/search/?keywords={keyword}&f_TPR=r86400")
    jobs_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(
            storage_state="linkedin_state.json",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
    )
        page = context.new_page()
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&f_TPR=r86400"
        page.goto(url, timeout=60000)
        print(f"🔗 Navigated to {url}")
        
        try:
            page.wait_for_selector("ul.jobs-search__results-list li", timeout=15000)
            print(f"✅ Loaded job results for '{keyword}'")
            job_cards = page.query_selector_all("ul.jobs-search__results-list li")
            for job in job_cards:
                title = job.query_selector(".job-card-list__title")
                company = job.query_selector(".job-card-container__company-name")
                location = job.query_selector(".job-card-container__metadata-item")
                link_tag = job.query_selector("a")
                jobs_data.append({
                    "title": title.inner_text().strip() if title else "N/A",
                    "company": company.inner_text().strip() if company else "N/A",
                    "location": location.inner_text().strip() if location else "N/A",
                    "link": link_tag.get_attribute("href") if link_tag else "N/A"
                })
        except Exception as e:
            print(f"⚠️ Failed to load job results for '{keyword}': {e}")
            page.screenshot(path=f"error_{keyword}.png")
            print(f"🖼 Screenshot saved: error_{keyword}.png")
        
        browser.close()

    # Save to JSON
    filename = f"jobs_{keyword.replace(' ', '_')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(jobs_data)} jobs to {filename}")

if __name__ == "__main__":
    keywords = ["hiring", "internship", "job opening", "software engineer"]
    for kw in keywords:
        scrape_jobs(kw)
