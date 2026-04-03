# import smtplib
# from email.mime.text import MIMEText


# def send_email(to_email, subject, body):
#     try:
#         sender_email = "ashrithavennu@gmail.com"
#         sender_password = "idpf tieo wmhz hzww"   # app password

#         msg = MIMEText(body)
#         msg["Subject"] = subject
#         msg["From"] = sender_email
#         msg["To"] = to_email

#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.send_message(msg)
#         server.quit()

#         print("✅ Email sent successfully")

#     except Exception as e:
#         print("❌ Email failed:", e)

#         # fallback preview
#         print("\n📧 EMAIL PREVIEW")
#         print("To:", to_email)
#         print("Subject:", subject)
#         print("Body:\n", body)

# # import os
# # import smtplib
# # from email.mime.text import MIMEText

# # def send_email(to_email, subject, body):
# #     try:
# #         sender_email = os.getenv("EMAIL_USER")
# #         sender_password = os.getenv("EMAIL_PASS")

# #         msg = MIMEText(body)
# #         msg["Subject"] = subject
# #         msg["From"] = sender_email
# #         msg["To"] = to_email

# #         server = smtplib.SMTP("smtp.gmail.com", 587)
# #         server.starttls()
# #         server.login(sender_email, sender_password)
# #         server.send_message(msg)
# #         server.quit()

# #         print("✅ Email sent successfully")

# #     except Exception as e:
# #         print("❌ Email failed:", e)

import smtplib
from email.mime.text import MIMEText
import os

def send_email(to_email, subject, body):
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("✅ Email actually sent")
        return True

    except Exception as e:
        print("❌ Email error:", e)
        return str(e)