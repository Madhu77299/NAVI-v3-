import requests
import json

cookies = {
    "li_at": " AQEDAUYpGZkEjMeRAAABmEylgm8AAAGYcLIGb00Apzt3Y6rOX_uWtqzlBz5d_EXS3PpkK4iJUY03GicuTpcPQOMi9dcFtuFhZPt0424VQCmRGCJyDwU3jvhWfqOMB0BZIwCbfX7yiKwonGDqDsr8raiW",
    "JSESSIONID": '"ajax:5096130520802218257"'
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "X-RestLi-Protocol-Version": "2.0.0",
    "Csrf-Token": "ajax:5096130520802218257"
}

url = "https://www.linkedin.com/voyager/api/identity/profiles/me"

response = requests.get(url, cookies=cookies, headers=headers)

print("Status:", response.status_code)
try:
    print("JSON:", response.json())
except:
    print("❌ Not valid JSON. Response:")
    print(response.text[:500])
