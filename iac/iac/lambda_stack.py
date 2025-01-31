from aws_cdk import (
    aws_lambda as lambda_,
    Duration
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, CognitoUserPoolsAuthorizer


class LambdaStack(Construct):
    functions_that_need_cognito_permissions = []
    functions_that_need_dynamo_permissions = []

    def create_lambda_api_gateway_integration(self, module_name: str, method: str, api_resource: Resource,
                                              environment_variables: dict = {"STAGE": "TEST"}, authorizer=None):

        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/routes/{module_name}"),
            handler=f"{module_name}.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer],
            memory_size=512,
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        api_resource.add_resource(module_name.replace("_", "-")).add_method(method, integration=LambdaIntegration(function), authorizer=authorizer)

        return function

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict,
                 authorizer: CognitoUserPoolsAuthorizer) -> None:
        super().__init__(scope, "SAExpress_Lambda")

        self.lambda_layer = lambda_.LayerVersion(self, "SAExpress_Layer",
                                                 code=lambda_.Code.from_asset("./lambda_layer_out_temp"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9]
                                                 )

        self.adm_update_user = self.create_lambda_api_gateway_integration(
            module_name="adm_update_user",
            method="PUT",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )
        
        self.create_deal = self.create_lambda_api_gateway_integration(
            module_name="create_deal",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.create_entity = self.create_lambda_api_gateway_integration(
            module_name="create_entity",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.create_user = self.create_lambda_api_gateway_integration(
            module_name="create_user",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_entities = self.create_lambda_api_gateway_integration(
            module_name="get_all_entities",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_users = self.create_lambda_api_gateway_integration(
            module_name="get_all_users",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_entity = self.create_lambda_api_gateway_integration(
            module_name="get_entity",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_entity_actives_deals = self.create_lambda_api_gateway_integration(
            module_name="get_entity_actives_deals",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_deal_status = self.create_lambda_api_gateway_integration(
            module_name="update_deal_status",
            method="PUT",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_entity = self.create_lambda_api_gateway_integration(
            module_name="update_entity",            
            method="PUT",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.functions_that_need_cognito_permissions = [
            self.adm_update_user,
            self.create_user,
            self.get_all_users
        ]

        self.functions_that_need_dynamo_permissions = [
            self.create_deal,
            self.create_entity,
            self.get_all_entities,
            self.get_entity,
            self.get_entity_actives_deals,
            self.update_deal_status,
            self.update_entity
        ]