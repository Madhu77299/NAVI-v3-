import smtplib
from email.message import EmailMessage

def send_email(jobs, config):
    if not jobs:
        print("📭 No jobs to send.")
        return

    msg = EmailMessage()
    msg["Subject"] = "🔔 NAVI Job Alerts"
    msg["From"] = config["email"]
    msg["To"] = config["to_email"]

    body = "\n\n".join([f"{job['title']}\n{job['link']}" for job in jobs])
    msg.set_content(f"Hi, here are your latest job updates from NAVI:\n\n{body}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(config["email"], config["email_password"])
            smtp.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)