import smtplib
from email.message import EmailMessage

# Configure sender
EMAIL_ADDRESS = "phantompothoneypot@gmail.com"
EMAIL_PASSWORD = "bdgb xukm roxd mrxw "
TO_EMAIL = "anandhuvihar@gmail.com"

def send_alert(subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("[+] Email alert sent.")
    except Exception as e:
        print(f"[!] Failed to send email alert: {e}")
