import smtplib
from email.message import EmailMessage
import re

def is_valid_email(email):
    """Return True if email looks valid."""
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def send_bulk_email(sender_email, sender_password, recipient_list, subject, body):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, sender_password)

    print("\n--- Bulk Email Sending Started ---\n")
    
    for idx, email in enumerate(recipient_list[:500]):
        email = str(email).strip()

        # Step 1: Validate email format
        if not is_valid_email(email):
            print(f"[{idx+1}] ❌ Wrong email: {email}")
            continue

        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = email
            msg.set_content(body.encode('ascii', 'ignore').decode())

            server.send_message(msg)
            print(f"[{idx+1}] ✅ Sent to: {email}")
        
        except Exception as e:
            print(f"[{idx+1}] ⚠️ Failed to send: {email} → Reason: {str(e)}")
            with open("failed_emails.txt", "a") as log:
                log.write(f"{email}: {str(e)}\n")

    server.quit()
    print("\n--- Bulk Email Sending Complete ---\n")
