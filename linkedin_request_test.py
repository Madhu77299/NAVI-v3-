import requests

# Your extracted cookies dictionary (copy the part from your script output)
cookies = {
    "li_rm": "AQGmjkRuv9x_UwAAAZg8AqdIgB-09RuUXF_2lxSWnB4BbBscR5tqGgWrpzZBDW7x7FQpT5d8R_JDov76GuuSBnHovt1P9x2GhvUG9HwM8N6hpEoGxtsRG4gn",
    "lang": "v=2&lang=en-us",
    "JSESSIONID": '"ajax:7098330991712074144"',
    "li_at": "AQEDAUYpGZkDM-ZtAAABmDwC_e0AAAGYYA-B7U0Any9prHutg9t5ByzAZu9OrAXVO5Xx3hdlDklAri1EF-egZh-FABExzUBatwvThSo_ALHEcjjqq-apq1xbidZCUh8H1tq9sUC3PX2ksJTKsDopcykb",
    # ... Add the rest of the cookies here
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Test URL — for example, the LinkedIn homepage
url = "https://www.linkedin.com/feed/"

response = requests.get(url, cookies=cookies, headers=headers)

# Print status and a preview of the content
print("Status Code:", response.status_code)
print(response.text[:1000])  # First 1000 characters of the response HTML
