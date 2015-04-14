#-------------------------------------------------------------------------------
# Name:        mailmodule
# Purpose:
#
# Author:      chemutt
#
# Created:     08/04/2015
# Copyright:
# Licence:
#-------------------------------------------------------------------------------

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import Encoders
import os

gmail_user = ""
gmail_pwd = ""
def mail(to, subject, text, attach):
 msg = MIMEMultipart()
 msg['From'] = gmail_user
 msg['To'] = to
 msg['Subject'] = subject
 msg.attach(MIMEText(text))
 part = MIMEBase('application', 'octet-stream')
 part.set_payload(open(attach, 'rb').read())
 Encoders.encode_base64(part)
 part.add_header('Content-Disposition',
 'attachment; filename="%s"' % os.path.basename(attach))
 msg.attach(part)
 mailServer = smtplib.SMTP("smtp.gmail.com", 587)
 mailServer.ehlo()
 mailServer.starttls()
 mailServer.ehlo()
 mailServer.login(gmail_user, gmail_pwd)
 mailServer.sendmail(gmail_user, to, msg.as_string())
 mailServer.close()


def main():
    pass

if __name__ == '__main__':
    main()




    mail(to, subject, text, attach)
