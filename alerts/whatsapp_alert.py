from twilio.rest import Client

def send_whatsapp_alert(jobs, config):
    try:
        account_sid = config["twilio_account_sid"]
        auth_token = config["twilio_auth_token"]
        client = Client(account_sid, auth_token)

        from_number = "whatsapp:+14155238886"  # Twilio sandbox number
        to_number = f"whatsapp:{config['whatsapp_number']}"

        for job in jobs:
            body = f"*Job Alert: Internship Opportunity*\n\n{job['description']}\n\nApply here: {job['link']}"
            message = client.messages.create(
                body=body,
                from_=from_number,
                to=to_number
            )
            print(f"✅ WhatsApp alert sent for: {job['title']}")
    except Exception as e:
        print(f"❌ Failed to send WhatsApp alert: {e}")