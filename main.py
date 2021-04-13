
import smtplib, ssl, sys
from os import environ
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

## Script is called in the format - "main.exe {invno} {acc_email} [{job_email}]"

load_dotenv()

orderno = sys.argv[1]
acc_email = sys.argv[2]
try:
  job_email = sys.argv[3]
except:
  job_email = ''

smtp_server = environ.get("SMTP_SERVER")
port = environ.get("SMTP_PORT")

if job_email != '':
  reciever = job_email
else:
  reciever = acc_email

sender = environ.get("OUTLOOK_ADDRESS")
password = environ.get("OUTLOOK_KEY")

# base64 encoded image
company_logo_b64 = environ.get("COMPANY_LOGO_B64")
company_logo_link = environ.get("COMPANY_LOGO_LINK")
company_trustpilot_link = environ.get("COMPANY_TRUSTPILOT_LINK")
company_name = environ.get("COMPANY_NAME")

message = MIMEMultipart("alternative")
message["Subject"] = f"Invoice Confirmation - {orderno}"
message["From"] = sender
message["To"] = reciever

html_gmail = f"""\
<html>
  <body>
    <p>Thank you for your order, {orderno}!<br>
      Please leave us a review on <a href="{company_trustpilot_link}">TrustPilot</a><br><br>
      <img src="{company_logo_link}" alt="{company_name}" title="Logo"/>
    </p>
  </body>
</html>
"""

html_other = f"""\
<html>
  <body>
    <p>Thank you for your order, {orderno}!<br>
      Please leave us a review on <a href="{company_trustpilot_link}">TrustPilot</a><br><br>
      <img src="data:image/png;base64,{company_logo_b64}" alt="{company_name}" title="Logo"/>
    </p>
  </body>
</html>
"""

# This will be used in place of the HTML if it can't be rendered for any reason
text = f"""\
Thank you for your order, {orderno}!
Please leave us a review on TrustPilot - {company_trustpilot_link}

{company_name}"""

part1 = MIMEText(text, "text")
part2 = MIMEText(html_other, "html")
part3 = MIMEText(html_gmail, "html")

message.attach(part1)
message.attach(part2)
message.attach(part3)

context = ssl.create_default_context()
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender, password)
    server.sendmail(sender, reciever, message.as_string())
except Exception as e:
    print(e)
finally:
    server.quit()