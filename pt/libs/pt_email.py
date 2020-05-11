from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
from email.mime.base import MIMEBase
from email import encoders


class PtEmail:
    # https://realpython.com/python-send-email/
    # https://accounts.google.com/DisplayUnlockCaptcha
    # https://myaccount.google.com/lesssecureapps
    smtp_server = None
    smtp_port = None
    smtp_password = None
    smtp_username = None
    from_name = None
    from_email_format = None
    from_email = None

    def __init__(self, smtp_server=None, smtp_port=None, smtp_username=None, smtp_password=None, from_name=None,
                 from_email=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_name = from_name
        self.from_email = from_email

        self.from_email_format = "{from_name} <{from_email}>".format(
            from_name=from_name,
            from_email=from_email
        )

    def send(self, to_email, subject, content, attach_content_str=None, attach_filename="attach_filename.txt", **params):
        message = MIMEMultipart("alternative")
        message["From"] = self.from_email_format
        message["To"] = to_email
        message["Subject"] = subject
        html = content.format(**params)

        message.attach(MIMEText(html, "html"))
        if attach_content_str is not None:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attach_content_str)
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                "attachment; filename= {0}".format(attach_filename),
            )
            message.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.smtp_username, to_email, message.as_string())
