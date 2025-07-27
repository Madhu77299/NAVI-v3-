import requests
import json

cookies = {
    "li_at": "AQEDAUYpGZkD3KTKAAABmEw7L1cAAAGYcEezV04ATLC9xTNJ_J1DbvVYoqOrodHS0dHwcQLoel5yzpKSO_JLrUPBAP6i2_QQReP1ddO30PFhTdrKMOjpuJzcLjl4d2lCI6oUucmL8-12A-8PRAcJyDW0",
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
