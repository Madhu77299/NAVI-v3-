import feedparser

def scrape_upwork(keywords):
    jobs = []
    base_url = "https://www.upwork.com/ab/feed/jobs/rss?q="

    for keyword in keywords:
        url = base_url + keyword.replace(" ", "+")
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:  # Limit to top 5 jobs per keyword
            jobs.append({
                "title": entry.title,
                "link": entry.link,
                "source": "Upwork"
            })

    return jobs