from playwright.sync_api import sync_playwright
import time
import json
import datetime

def scrape_linkedin_feed(keywords, require_hr_match=True):
    posts = []
    seen_titles = set()

    with sync_playwright() as p:
        print("🌐 Launching browser...")
        browser = p.chromium.launch(headless=False, slow_mo=100)

        try:
            context = browser.new_context(storage_state="linkedin_state.json")
        except Exception as e:
            print(f"⚠️ Couldn't load linkedin_state.json: {e}")
            return posts

        page = context.new_page()

        try:
            print("🔗 Navigating to LinkedIn feed...")
            timestamp = int(time.time())
            page.goto(f"https://www.linkedin.com/feed/?_={timestamp}", timeout=60000)

            # Clear cached data
            page.evaluate("localStorage.clear(); sessionStorage.clear();")

            try:
                page.wait_for_selector("div.feed-shared-update-v2", timeout=30000)
                print("✅ Feed loaded successfully.")
            except:
                if "authwall" in page.url or "login" in page.url:
                    print("❌ Not logged in. Please generate linkedin_state.json first.")
                    browser.close()
                    return posts
                print("⚠️ Feed items not found. Continuing anyway...")

            all_scraped_raw = []

            for scroll_round in range(3):
                print(f"🔄 Scrolling round {scroll_round + 1}")
                page.mouse.wheel(0, 3000)
                time.sleep(3)
                page.reload()
                time.sleep(2)

                feed_items = page.query_selector_all("div.feed-shared-update-v2")
                print(f"🔍 Round {scroll_round + 1}: Found {len(feed_items)} feed items.")

                for item in feed_items:
                    try:
                        text = item.inner_text().lower().strip()
                        if not text:
                            continue

                        link = "#"
                        link_element = item.query_selector("a.app-aware-link")
                        if link_element:
                            raw_link = link_element.get_attribute("href")
                            if raw_link:
                                link = raw_link.split("?")[0]

                        poster = item.query_selector("span.feed-shared-actor__description, span.update-components-actor__description")
                        poster_text = poster.inner_text().lower().strip() if poster else ""

                        # Debug output
                        print(f"\n📝 Text: {text[:100]}...")
                        print(f"👤 Poster: {poster_text}")

                        keyword_match = any(k.lower() in text for k in keywords)
                        poster_match = any(x in poster_text for x in ["hr", "recruiter", "talent", "hiring"])

                        # Save raw data
                        all_scraped_raw.append({
                            "text": text,
                            "poster": poster_text,
                            "link": link
                        })

                        if keyword_match and (poster_match if require_hr_match else True):
                            title = ' '.join(text.split()[:20])
                            title = title[:80].replace("\n", " ").strip()
                            if len(title) >= 80:
                                title += "..."

                            if title not in seen_titles:
                                seen_titles.add(title)
                                posts.append({
                                    "title": title,
                                    "link": link,
                                    "source": "LinkedIn Post",
                                    "poster": poster_text[:50]
                                })
                    except Exception as e:
                        print(f"⚠️ Error parsing post: {e}")
                        continue

        except Exception as e:
            print(f"❌ Critical error: {e}")
        finally:
            browser.close()

    # Save raw scraped data
    with open("linkedin_all_scraped_raw.json", "w", encoding="utf-8") as f:
        json.dump(all_scraped_raw, f, ensure_ascii=False, indent=2)

    return posts

if __name__ == "__main__":
    keywords = [
        "hiring", "we are hiring", "job opening", "open position", "recruiting", 
        "vacancy", "opportunity", "intern", "internship", "software engineer", 
        "full-time", "fresher", "graduate", "walk-in"
    ]

    print("🚀 Starting LinkedIn feed scrape...")

    # Set to False to ignore HR-only filter
    posts = scrape_linkedin_feed(keywords, require_hr_match=False)

    if not posts:
        print("📭 No relevant posts found.")
    else:
        print(f"\n🎉 Found {len(posts)} matching posts:")
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   👤 {post['poster']}")
            print(f"   🔗 {post['link']}")

        with open("linkedin_results.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print("\n💾 Saved to linkedin_results.json")
