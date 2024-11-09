import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import datetime

class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password, from_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.server = None

    def connect(self):
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.server.login(self.smtp_user, self.smtp_password)
            print('Connected to SMTP server')
        except Exception as e:
            print(f'Failed to connect to SMTP server: {e}')

    def disconnect(self):
        if self.server:
            self.server.quit()
            print('Disconnected from SMTP server')

    def send_email(self, to_email, subject, body):
        if not self.server:
            print('Not connected to SMTP server')
            return

        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        try:
            self.server.sendmail(self.from_email, to_email, msg.as_string())
            print(f'Email sent to {to_email}')
        except Exception as e:
            print(f'Failed to send email: {e}')

    @staticmethod
    def render_template(template_str, context):
        env = Environment()
        template = env.from_string(template_str)
        return template.render(context)

    @staticmethod
    def render_template_from_file(template_name, context):
        file_loader = FileSystemLoader('./email_templates')
        env = Environment(loader=file_loader)
        template = env.get_template(template_name)
        return template.render(context)


smtp_server = "smtp.mail.ru"
smtp_port = 587
smtp_user = "dudlif.pl@mail.ru"
smtp_password = "Cwwf0U0a2U61mhXXGyB8"
from_email = "dudlif.pl@mail.ru"

email_sender = EmailSender(smtp_server, smtp_port, smtp_user, smtp_password, from_email)
email_sender.connect()

