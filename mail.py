import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailClient:
    def __init__(self, smtp_server, imap_server, email_address, password):
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.email_address = email_address
        self.password = password

    def send_email(self, recipients, subject, message):
        """Отправка письма."""
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address, recipients, msg.as_string())

    def receive_email(self, folder="inbox", header=None):
        """Получение писем из указанной папки."""
        with imaplib.IMAP4_SSL(self.imap_server) as mail:
            mail.login(self.email_address, self.password)
            mail.select(folder)
            criterion = f'(HEADER Subject "{header}")' if header else 'ALL'
            result, data = mail.uid('search', None, criterion)
            if not data[0]:
                raise ValueError("No emails found with the specified header")

            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)
            return email_message


if __name__ == "__main__":
    # Инициализация клиента
    client = EmailClient(
        smtp_server="smtp.gmail.com",
        imap_server="imap.gmail.com",
        email_address="login@gmail.com",
        password="qwerty"
    )

    # Отправка письма
    client.send_email(
        recipients=["vasya@email.com", "petya@email.com"],
        subject="Subject",
        message="Message"
    )

    # Получение письма
    try:
        email_message = client.receive_email(header="Subject")
        print("Получено письмо:", email_message)
    except ValueError as e:
        print(e)
