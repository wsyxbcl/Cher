import smtplib
import os
from email.message import EmailMessage

def mail(mail_from, mail_to, subject, content):
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    msg = EmailMessage()
    msg.set_content(content)

    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = mail_to

    server = smtplib.SMTP_SSL("smtp.googlemail.com", 465)
    server.login(MAIL_USERNAME, MAIL_PASSWORD)
    server.sendmail(mail_from, mail_to, msg.as_string())
    server.quit()

if __name__ == '__main__':
    subject = 'TEST'
    content = 'Hello world, this is Cher.'
    mail_from = 'wsyxbcl@gmail.com'
    with open('mail_list.txt') as fp:
        mail_list = [line.rstrip() for line in fp]
    for mail_to in mail_list:
        mail(mail_from, mail_to, subject, content)
 
