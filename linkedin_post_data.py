import requests

# LinkedIn session cookies
cookies = {
    "li_at": " AQEDAUYpGZkCUu3aAAABmExNSLQAAAGYcFnMtE4AegcCkcQeWJO0AW-1vWJSu2SxIiNsWjLjpjvQr1l9LZ0WtiAIYO6hae2BBaTu4kJnzyB4U4ZwKUknpgmtkQ38yW5DRt_-EBesz9dhFGHXeY2ObJVi",
    "JSESSIONID": '"ajax:5096130520802218257"'  # keep double quotes
}

# Common headers
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "X-RestLi-Protocol-Version": "2.0.0",
    "Csrf-Token": "ajax:5096130520802218257"  # no quotes here
}

# ---------------------------
# PART 1: Fetch Profile Info
# ---------------------------
print("🔹 Fetching profile info...")

profile_url = "https://www.linkedin.com/voyager/api/identity/dash/profileView?decorationId=com.linkedin.voyager.dash.deco.identity.profile.TopCardSupplementary-105"

headers["Accept"] = "application/json"

profile_response = requests.get(profile_url, cookies=cookies, headers=headers)
print("Profile Status:", profile_response.status_code)

try:
    profile_data = profile_response.json()
    print("✅ Profile Data:")
    print(profile_data)
except Exception as e:
    print("❌ Failed to parse profile data:", e)
    print(profile_response.text[:500])

# ---------------------------
# PART 2: Fetch Feed Updates
# ---------------------------
print("\n🔹 Fetching feed posts...")

feed_url = "https://www.linkedin.com/voyager/api/feed/updatesV2?count=10&q=homepageFeed&start=0"

headers["Accept"] = "application/vnd.linkedin.normalized+json+2.1"

feed_response = requests.get(feed_url, cookies=cookies, headers=headers)
print("Feed Status:", feed_response.status_code)

try:
    feed_data = feed_response.json()
    updates = feed_data.get("included", [])
    print(f"\n🔹 Total Feed Items Fetched: {len(updates)}")

    for idx, item in enumerate(updates):
        if "commentary" in item:
            text = item["commentary"].get("text", {}).get("text", "")
            print(f"\n📝 Post {idx+1}:\n{text}")
except Exception as e:
    print("❌ Failed to parse feed data:", e)
    print(feed_response.text[:500])
