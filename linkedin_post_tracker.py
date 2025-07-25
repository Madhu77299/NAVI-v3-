from playwright.sync_api import sync_playwright
import time

def scrape_linkedin_feed(keywords):
    posts = []
    with sync_playwright() as p:
        print("🌐 Launching browser...")
        browser = p.chromium.launch(headless=False, slow_mo=100)
        
        # Load authentication state if available
        try:
            context = browser.new_context(storage_state="linkedin_state.json")
        except Exception as e:
            print(f"⚠️ Couldn't load authentication state: {e}")
            context = browser.new_context()
            
        page = context.new_page()
        
        try:
            print("🔗 Navigating to LinkedIn feed...")
            page.goto("https://www.linkedin.com/feed/", timeout=60000)
            
            # Wait for either feed content or login prompt
            try:
                page.wait_for_selector("div.feed-shared-update-v2", timeout=30000)
                print("✅ Feed loaded successfully.")
            except:
                # Check if we got redirected to login
                if "authwall" in page.url:
                    print("❌ Not logged in. Please authenticate first.")
                    browser.close()
                    return posts
                print("⚠️ Feed items not found, but page loaded. Continuing...")
                
            time.sleep(3)  # Small delay to let content settle
            
            # Get feed items with more robust selector
            feed_items = page.query_selector_all("div.feed-shared-update-v2, div.update-components-text")[:15]
            print(f"🔍 Found {len(feed_items)} feed items.")
            
            for item in feed_items:
                try:
                    # Get text content safely
                    text = item.inner_text().lower()
                    if not text:
                        continue
                        
                    # Get link if available
                    link_element = item.query_selector("a.app-aware-link")
                    link = link_element.get_attribute("href").split('?')[0] if link_element else "#"
                    
                    # Get poster information
                    poster = item.query_selector("span.feed-shared-actor__description, span.update-components-actor__description")
                    poster_text = poster.inner_text().lower() if poster else ""
                    
                    # Check keywords and poster type
                    keyword_match = any(k.lower() in text for k in keywords)
                    poster_match = ("hr" in poster_text or "recruiter" in poster_text or "talent" in poster_text)
                    
                    if keyword_match and poster_match:
                        # Clean up title text
                        title = ' '.join(text.split()[:20])  # First 20 words
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
                    print(f"⚠️ Error parsing post: {str(e)[:100]}...")
                    continue
                    
        except Exception as e:
            print(f"❌ Critical error during scraping: {e}")
            
        finally:
            browser.close()
            
    return posts

if __name__ == "__main__":
    keywords = ["hiring", "internship", "job opening", "software engineer", "opportunity"]
    print("🚀 Starting LinkedIn post scrape...")
    posts = scrape_linkedin_feed(keywords)
    
    if not posts:
        print("📭 No relevant posts found matching the keywords.")
    else:
        print(f"🎉 Found {len(posts)} relevant posts:")
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   👤 Posted by: {post.get('poster', 'Unknown')}")
            print(f"   🔗 {post['link']}")