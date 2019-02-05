import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DEFAULT_SMTP = 'smtp.gmail.com'
DEFAULT_IMAP = 'imap.gmail.com'
DEFAULT_PORT = 587


class MailBox:
    def __init__(self, login, password, smtp=DEFAULT_SMTP,
                 imap=DEFAULT_IMAP, smtp_port=DEFAULT_PORT):
        self.login = login
        self.password = password
        self.smtp = smtp
        self.imap = imap
        self.smtp_port = smtp_port

    def send_message(self, subject, recipients, message):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        ms = smtplib.SMTP(self.smtp, self.smtp_port)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(self.login, recipients, msg.as_string())
        ms.quit()

    def receive_messages(self, folder="inbox", header=None):
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(self.login, self.password)
        mail.list()
        mail.select(folder)
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':
    my_email = MailBox('login@gmail.com', 'qwerty')
    my_email.send_message('Subject', ['vasya@email.com', 'petya@email.com'],
                          'Message')
    print(my_email.receive_messages())
