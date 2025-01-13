import os


from aws_cdk import (
    CfnOutput,
    aws_dynamodb,
    RemovalPolicy,
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration

class DynamoStack(Construct):

        def __init__(self, scope: Construct) -> None:
            super().__init__(scope, "SAExpress_Dynamo")

            self.github_ref_name = os.environ.get("GITHUB_REF_NAME")

            REMOVAL_POLICY = RemovalPolicy.RETAIN if 'prod' in self.github_ref_name else RemovalPolicy.DESTROY

            self.dynamo_table = aws_dynamodb.Table(
                self, "SAExpress_Table",
                partition_key=aws_dynamodb.Attribute(
                    name="PK",
                    type=aws_dynamodb.AttributeType.STRING
                ),
                sort_key=aws_dynamodb.Attribute(
                    name="SK",
                    type=aws_dynamodb.AttributeType.STRING
                ),
                point_in_time_recovery=True,
                billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
                removal_policy=REMOVAL_POLICY
            )
                
            self.dynamo_table.add_global_secondary_index(
                partition_key=aws_dynamodb.Attribute(
                    name="GSI-PK",
                    type=aws_dynamodb.AttributeType.STRING
                ),
                index_name="GSI"
            )
            
            CfnOutput(self, 'DynamoSAExpressRemovalPolicy',
                    value=REMOVAL_POLICY.value,
                    export_name=f'SAExpress{self.github_ref_name}DynamoSAExpressRemovalPolicyValue')