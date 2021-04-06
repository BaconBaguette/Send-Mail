import email, smtplib, ssl, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

orderno = sys.argv[1]

smtp_server = "smtp.office365.com"
port = 587

sender = "ctstesting4jack@outlook.com"
password = "Test4cts123"
reciever = "jturner@clearthinkingsoftware.co.uk"

# base64 encoded image
company_logo = "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"

message = MIMEMultipart("alternative")
message["Subject"] = "Python Emailing Test"
message["From"] = sender
message["To"] = reciever

html = f"""\
<html>
  <body>
    <p>Thank you for your order, {orderno}!<br>
      Please leave us a review on <a href="https://uk.trustpilot.com/review/glassandstainlessuk.co.uk">TrustPilot</a><br><br>
      <img src="data:image/png;base64,{company_logo}" alt="Glass + Stainless"/>
    </p>
  </body>
</html>
"""

# This will be used in place of the HTML if it can't be rendered for any reason
text = """
Thank you for your order!
Please leave us a review on TrustPilot - https://uk.trustpilot.com/review/glassandstainlessuk.co.uk

Glass + Stainless"""

part1 = MIMEText(text, "text")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

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