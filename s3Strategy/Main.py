import sqs
import s3
import Email

ress3 = s3.storage().upload_file('demo1','sanket7783')
resqueu = sqs.SQS().SendMessage()
rec = sqs.SQS().ReceiveMessage()
resEmail = Email.EmailSend().send()