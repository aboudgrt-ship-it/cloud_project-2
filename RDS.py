


import boto3
from botocore.exceptions import ClientError

class vpWrapper:
    def __init__(self, ec2_client: boto3.client, vpc_id: str):
        self.ec2_client = ec2_client


    @classmethod
    def from_client(cls) -> 'vpWrapper':