import boto3

class SQS():
    def __init__(self):
        self.sqs = boto3.client('sqs')

    def list_queue(self):
        response = self.sqs.list_queues()

    def create_queue(self):
        response = self.sqs.create_queue(
            QueueName='SQS_QUEUE_NAME',
            Attributes={
                'DelaySeconds': '60',
                'MessageRetentionPeriod': '86400'
            }
        )

        print(response['QueueUrl'])

    def del_queue(self):
        self.sqs.delete_queue(QueueUrl='SQS_QUEUE_URL')

    #Messages
    def SendMessage(self):
        queue_url = 'https://sqs.us-west-2.amazonaws.com/777964820277/test'

        # Send message to SQS queue
        response = self.sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={

            },
            MessageBody=(
                'Information about current NY Times fiction bestseller for '
                'week of 12/11/2016.'
            )
        )

        print(response['MessageId'])

    def ReceiveMessage(self):
        queue_url = 'https://sqs.us-west-2.amazonaws.com/777964820277/test'

        # Receive message from SQS queue
        response = self.sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )
        print(response)

        messages = response['Messages']
        receipt_handles = []
        for message in messages:
            receipt_handles.append(message['ReceiptHandle'])

        for receipt_handle in receipt_handles:
        # Delete received message from queue
            self.sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )

        for message in messages:
            print('Received and deleted message: %s' % message)