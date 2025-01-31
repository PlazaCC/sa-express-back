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