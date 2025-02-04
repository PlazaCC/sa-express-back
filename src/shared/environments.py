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
    stage: STAGE = STAGE(os.environ.get('STAGE', "TEST"))
    region: str = os.environ.get("AWS_REGION", "sa-east-1")
    user_pool_id: str = os.environ.get("USER_POOL_ID", "")
    user_pool_arn: str = os.environ.get("USER_POOL_ARN", "")
    app_client_id: str = os.environ.get("APP_CLIENT_ID", "")
    bucket_name: str = os.environ.get("BUCKET_NAME", "")
    dynamo_table_name: str = os.environ.get("DYNAMO_TABLE_NAME", "")
    dynamo_partition_key: str = os.environ.get("DYNAMO_PARTITION_KEY", "")
    dynamo_sort_key: str = os.environ.get("DYNAMO_SORT_KEY", "")
    dynamo_gsi_partition_key: str = os.environ.get("DYNAMO_GSI_PARTITION_KEY", "")
    paygate_webhook_token: str = os.environ.get("PAYGATE_WEBHOOK_TOKEN", "MOCK")
    paybrokers_base_url: str = os.environ.get("PAYBROKERS_BASE_URL", "https://api.sandbox.paybrokers.solutions")
    paybrokers_webhook_url: str = os.environ.get("PAYBROKERS_WEBHOOK_BASE_URL", "http://127.0.0.1:3000")
    paybrokers_auth_token: str = os.environ.get("PAYBROKERS_AUTH_TOKEN", "MOCK")
    paybrokers_webhook_key: str = os.environ.get("PAYBROKERS_WEBHOOK_KEY", "bf8867f612a34346a57d4e1c5e98b1ecc53defe3cccc4b7b8ea72dfbcf74a349")
