from playwright.sync_api import sync_playwright
import time
import json

def scrape_linkedin_feed(keywords):
    posts = []
    with sync_playwright() as p:
        print("🌐 Launching browser...")
        browser = p.chromium.launch(headless=False, slow_mo=100)

        # Load cookies from previously authenticated session
        try:
            context = browser.new_context(storage_state="linkedin_state.json")
        except Exception as e:
            print(f"⚠️ Couldn't load linkedin_state.json: {e}")
            return posts

        page = context.new_page()

        try:
            print("🔗 Navigating to LinkedIn feed...")
            page.goto("https://www.linkedin.com/feed/", timeout=60000)

            # Wait for feed items or login redirect
            try:
                page.wait_for_selector("div.feed-shared-update-v2", timeout=30000)
                print("✅ Feed loaded successfully.")
            except:
                if "authwall" in page.url or "login" in page.url:
                    print("❌ Not logged in. Please generate linkedin_state.json first.")
                    browser.close()
                    return posts
                print("⚠️ Feed items not found. Continuing anyway...")

            # Scroll to load more content
            for _ in range(3):
                page.mouse.wheel(0, 2000)
                time.sleep(2)

            # Grab top ~45 posts (3 scrolls)
            feed_items = page.query_selector_all("div.feed-shared-update-v2, div.update-components-text")
            print(f"🔍 Found {len(feed_items)} feed items.")

            for item in feed_items:
                try:
                    text = item.inner_text().lower().strip()
                    if not text:
                        continue

                    # Post link
                    link = "#"
                    link_element = item.query_selector("a.app-aware-link")
                    if link_element:
                        raw_link = link_element.get_attribute("href")
                        if raw_link:
                            link = raw_link.split("?")[0]

                    # Poster info
                    poster = item.query_selector("span.feed-shared-actor__description, span.update-components-actor__description")
                    poster_text = poster.inner_text().lower().strip() if poster else ""

                    # Keyword & HR filter
                    keyword_match = any(k.lower() in text for k in keywords)
                    poster_match = any(x in poster_text for x in ["hr", "recruiter", "talent", "hiring"])

                    if keyword_match and poster_match:
                        title = ' '.join(text.split()[:20])
                        title = title[:80].replace("\n", " ").strip()
                        if len(title) >= 80:
                            title += "..."

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

    return posts

if __name__ == "__main__":
    keywords = ["hiring", "internship", "job opening", "software engineer", "opportunity"]
    print("🚀 Starting LinkedIn feed scrape...")
    posts = scrape_linkedin_feed(keywords)

    if not posts:
        print("📭 No relevant posts found.")
    else:
        print(f"\n🎉 Found {len(posts)} matching posts:")
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   👤 {post['poster']}")
            print(f"   🔗 {post['link']}")

        # Save to file
        with open("linkedin_results.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print("\n💾 Saved to linkedin_results.json")

