import os
from aws_cdk import (
    CfnOutput,
    aws_dynamodb,
    RemovalPolicy,
)
from constructs import Construct


class DynamoStack(Construct):

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, "SAExpress_Dynamo")

        github_ref_name = os.environ.get("GITHUB_REF_NAME", "dev")
        removal_policy = RemovalPolicy.RETAIN if 'prod' in github_ref_name else RemovalPolicy.DESTROY

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
            removal_policy=removal_policy
        )

        # GSI: GetProposalsByUser
        self.dynamo_table.add_global_secondary_index(
            partition_key=aws_dynamodb.Attribute(
                name="PROPOSAL#<UserId>",
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="SEND/RECEIVED#TYPE#<ProposalId>#<Status>",
                type=aws_dynamodb.AttributeType.STRING
            ),
            index_name="GetProposalsByUser"
        )

        # GSI: GetDataFromSpecificProposal
        self.dynamo_table.add_global_secondary_index(
            partition_key=aws_dynamodb.Attribute(
                name="PROPOSAL#<ProposalId>",
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="METADATA",
                type=aws_dynamodb.AttributeType.STRING
            ),
            index_name="GetDataFromSpecificProposal"
        )

        # GSI: AdmGetAllUsers
        self.dynamo_table.add_global_secondary_index(
            partition_key=aws_dynamodb.Attribute(
                name="PROFILE",
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="userId#<role>#<email>#<name>#<status>",
                type=aws_dynamodb.AttributeType.STRING
            ),
            index_name="AdmGetAllUsers"
        )

        # GSI: GetAffiliationTopUsersData
        self.dynamo_table.add_global_secondary_index(
            partition_key=aws_dynamodb.Attribute(
                name="DEAL#<DealId>",
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="AFFILIATION#<n° cadastros total>#<n° FTDs total>#<n° CPAs total>#<UserId>",
                type=aws_dynamodb.AttributeType.STRING
            ),
            index_name="GetAffiliationTopUsersData"
        )

        # GSI: GetAllCompetitions
        self.dynamo_table.add_global_secondary_index(
            partition_key=aws_dynamodb.Attribute(
                name="COMPETITION",
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="<CompId>#<Status>#<createdAt>#<endAt>",
                type=aws_dynamodb.AttributeType.STRING
            ),
            index_name="GetAllCompetitions"
        )

        # Saída de configuração da tabela
        CfnOutput(self, 'DynamoTableName',
                  value=self.dynamo_table.table_name,
                  export_name=f"SAExpress{github_ref_name}TableName")

        CfnOutput(self, 'DynamoSAExpressRemovalPolicy',
                  value=removal_policy.value,
                  export_name=f"SAExpress{github_ref_name}DynamoRemovalPolicy")
