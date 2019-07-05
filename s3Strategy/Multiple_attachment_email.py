import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import s3

class EmailSend():
    def __init__(self):
        self.client = boto3.client('ses')

    def send(self):
        SENDER = "shambir@tripwire.com"
        RECIPIENT = "shambir@tripwire.com"
        AWS_REGION = "eu-west-1"
        SUBJECT = "Customer service contact info"
        ATTACHMENT = "abc.pdf"
        ATTACHMENT = ATTACHMENT.split(',')

        BODY_HTML = """\
          <html>
          <head></head>
          <body>
          <h1>Hello!</h1>
          <p>Please see the attached file for a list of customers to contact.</p>
          </body>
          </html>
          """

        CHARSET = "utf-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name=AWS_REGION)

        # Create a multipart/mixed parent container.
        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = SUBJECT
        msg['From'] = SENDER
        msg['To'] = RECIPIENT

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')

        # Encode the text and HTML content and set the character encoding. This step is
        # necessary if you're sending a message with characters outside the ASCII range.

        htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
        msg.attach(msg_body)
        # Add the text and HTML parts to the child container.

        # Add the attachment to the parent container.
        msg_body.attach(htmlpart)
        for attachments in ATTACHMENT:
            att = MIMEApplication(open(attachments, 'rb').read())
            att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachments))
            msg.attach(att)
        try:
            # Provide the contents of the email.
            response = client.send_raw_email(
                Source=SENDER,
                Destinations=[
                    RECIPIENT
                ],
                RawMessage={
                    'Data': msg.as_string(),
                },

            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response)
        else:
            print("Email sent! Message ID:"),
            print(response)
