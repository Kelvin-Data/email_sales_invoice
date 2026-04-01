import smtplib, ssl
import os
from email.message import EmailMessage
import mimetypes
import dotenv

dotenv.load_dotenv()

SMTP_HOST = "smtp.gmail.com"   
SMTP_PORT = 587             
SMTP_USER = "your email account"
SMTP_PASS = os.getenv("GMAIL_PASSWORD") 

def send_email_with_attachment(from_addr, to_addrs, subject, body, attachment_path=None):
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs) if isinstance(to_addrs, (list, tuple)) else to_addrs
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment_path:
        mime_type, _ = mimetypes.guess_type(attachment_path)
        mime_type = mime_type or "application/octet-stream"
        maintype, subtype = mime_type.split('/', 1)

        with open(attachment_path, "rb") as f:
            msg.add_attachment(f.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=os.path.basename(attachment_path))

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
