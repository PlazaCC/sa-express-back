import boto3

class ElastiCacheDatasource:
    def __init__(self):
        self.client = boto3.client('elasticache')
