import json
from scraping.linkedin_post_tracker import scrape_linkedin_feed
from alerts.email_alert import send_email
from alerts.whatsapp_alert import send_whatsapp_alert

# 🔧 Load configuration
with open("config.json") as f:
    config = json.load(f)

# 🔍 Fetch jobs from LinkedIn feed posts
# jobs = scrape_linkedin_feed(config["keywords"])
jobs = [{
    "title": "Python Developer Internship - Google",
    "link": "https://www.linkedin.com/jobs/view/test-python-job",
    "description": "🚀 Google is hiring a Python intern to join their remote engineering team. Great opportunity to work on real-world projects. #python #internship #remote"
}]

# 📤 Alert via Email & WhatsApp
if jobs:
    print(f"✅ Found {len(jobs)} job(s) from LinkedIn posts")
    send_email(jobs, config)

    if config["send_whatsapp"]:
        send_whatsapp_alert(jobs, config)
else:
    print("📭 No jobs to send.")