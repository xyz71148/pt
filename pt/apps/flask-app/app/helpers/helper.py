from flask_caching import Cache
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from email.mime.base import MIMEBase
from email import encoders


cache = Cache(config={
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": "./.cache",
    "CACHE_DEFAULT_TIMEOUT": 300
})


def mail_send(to_email, subject, content,attach_content=None, attach_filename="attach_filename.txt", **params):
    from .setting import Setting
    smtp_server = Setting.get("SMTP_SERVER", default="smtp.gmail.com", update=True)
    port = Setting.get("SMTP_PORT", default="587", update=True)
    from_name = Setting.get("SMTP_FROM_NAME", default="FROM_NAME", update=True)
    from_email = Setting.get("SMTP_FROM_EMAIL", default="user@example.com", update=True)
    from_email = "{from_name} <{from_email}>".format(
        from_name=from_name,
        from_email=from_email
    )

    sender_email = Setting.get("SMTP_USER_NAME", default="SMTP_USER_NAME", update=True)
    password = Setting.get("SMTP_PASSWORD", default="SMTP_PASSWORD", update=True)
    message = MIMEMultipart("alternative")
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    if params:
        html = content.format(**params)
    else:
        html = content

    message.attach(MIMEText(html, "html"))
    if attach_content is not None:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attach_content)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment; filename= {0}".format(attach_filename),
        )
        message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message.as_string())

