from enum import Enum
import os
from dotenv import load_dotenv

class STAGE(Enum):
    TEST = "TEST"
    DEV = "DEV"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"

class Environments:
    load_dotenv()
    print(os.environ.get('STAGE'))
    stage: STAGE = STAGE(os.environ.get('STAGE', '').upper())
    region: str = os.environ.get("AWS_REGION", "sa-east-1")
    user_pool_id: str = os.environ.get("USER_POOL_ID", "")
    user_pool_arn: str = os.environ.get("USER_POOL_ARN", "")
    app_client_id: str = os.environ.get("APP_CLIENT_ID", "")
    bucket_name: str = os.environ.get("BUCKET_NAME", "")
    dynamo_table_name: str = os.environ.get("DYNAMO_TABLE_NAME", "")
    dynamo_partition_key: str = os.environ.get("DYNAMO_PARTITION_KEY", "")
    dynamo_sort_key: str = os.environ.get("DYNAMO_SORT_KEY", "")
    dynamo_gsi_partition_key: str = os.environ.get("DYNAMO_GSI_PARTITION_KEY", "")