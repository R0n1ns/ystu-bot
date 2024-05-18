import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_address, subject, message, from_address, password):
    # Настройка параметров SMTP-сервера
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Установка соединения с SMTP-сервером и начало шифрованной сессии
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Авторизация на SMTP-сервере
        server.login(from_address, password)

        # Отправка письма
        server.sendmail(from_address, to_address, msg.as_string())

        # Закрытие соединения с сервером
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")


# Пример использования функции
to_address = "recipient@example.com"
subject = "Test Email"
message = "This is a test email sent from Python."
from_address = "your_email@gmail.com"
password = "your_password"

send_email(to_address, subject, message, from_address, password)

import imaplib
import email
from email.header import decode_header
import webbrowser
import os

def check_inbox(email_user, email_pass):
    # Логин и соединение с сервером
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)

    # Выбор почтового ящика, "inbox" - это стандартный входящий ящик
    mail.select("inbox")

    # Поиск всех писем в папке "inbox"
    status, messages = mail.search(None, "ALL")

    # Получение списка номеров писем
    mail_ids = messages[0].split()

    # Перебор последних 5 писем
    for i in range(min(5, len(mail_ids))):
        # Получение письма по ID
        status, msg_data = mail.fetch(mail_ids[-(i+1)], "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Парсинг письма
                msg = email.message_from_bytes(response_part[1])
                # Декодирование заголовка
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")
                print(f"Subject: {subject}")
                print(f"From: {from_}")

                # Если письмо содержит текст или HTML
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if "attachment" not in content_disposition:
                            # Получение содержимого письма
                            body = part.get_payload(decode=True).decode()
                            if content_type == "text/plain":
                                print("Body:", body)
                        else:
                            # Обработка вложений
                            filename = part.get_filename()
                            if filename:
                                filepath = os.path.join("/path/to/save/attachments", filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                else:
                    # Обработка писем без вложений
                    body = msg.get_payload(decode=True).decode()
                    print("Body:", body)
    # Закрытие соединения
    mail.logout()

# Пример использования функции
email_user = "your_email@gmail.com"
email_pass = "your_password"

check_inbox(email_user, email_pass)
