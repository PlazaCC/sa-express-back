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
            timeout=Duration.seconds(15),
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
            # authorizer=authorizer
        )

        self.create_entity = self.create_lambda_api_gateway_integration(
            module_name="create_entity",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.create_profile = self.create_lambda_api_gateway_integration(
            module_name="create_profile",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.create_user = self.create_lambda_api_gateway_integration(
            module_name="create_user",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.deactivate_profile = self.create_lambda_api_gateway_integration(
            module_name="deactivate_profile",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.get_all_entities = self.create_lambda_api_gateway_integration(
            module_name="get_all_entities",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.get_all_users = self.create_lambda_api_gateway_integration(
            module_name="get_all_users",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.get_entity = self.create_lambda_api_gateway_integration(
            module_name="get_entity",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.get_entity_actives_deals = self.create_lambda_api_gateway_integration(
            module_name="get_entity_actives_deals",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.get_my_profile = self.create_lambda_api_gateway_integration(
            module_name="get_my_profile",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.update_deal_status = self.create_lambda_api_gateway_integration(
            module_name="update_deal_status",
            method="PUT",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        self.update_entity = self.create_lambda_api_gateway_integration(
            module_name="update_entity",            
            method="PUT",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            # authorizer=authorizer
        )

        ### WALLET FUNCTIONS ###
        # GET
        self.get_user_vault = self.create_lambda_api_gateway_integration(
            module_name="get_user_vault",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        # TODO: extrair tx_id do query params
        self.get_user_tx = self.create_lambda_api_gateway_integration(
            module_name="get_user_tx",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        # POST
        self.create_vault = self.create_lambda_api_gateway_integration(
            module_name="create_vault",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.set_pix_key = self.create_lambda_api_gateway_integration(
            module_name="set_pix_key",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )
        
        # TODO: implementar get_user_by_email no wallet_repo
        self.transfer = self.create_lambda_api_gateway_integration(
            module_name="transfer",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.deposit = self.create_lambda_api_gateway_integration(
            module_name="deposit",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.withdrawal = self.create_lambda_api_gateway_integration(
            module_name="withdrawal",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.paybrokers_webhook = self.create_lambda_api_gateway_integration(
            module_name="paybrokers_webhook",
            method="POST",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
        )
        ### WALLET FUNCTIONS ###

        self.functions_that_need_cognito_permissions = [
            self.adm_update_user,
            self.create_user,
            self.get_all_users,
            self.deactivate_profile
        ]

        self.functions_that_need_dynamo_permissions = [
            self.create_deal,
            self.create_entity,
            self.get_all_entities,
            self.get_entity,
            self.get_entity_actives_deals,
            self.update_deal_status,
            self.update_entity,
            self.create_profile,
            self.deactivate_profile
        ]

        self.functions_that_need_elasticache_permissions = []

        wallet_functions_with_cognito_dynamo_perms = [
            self.get_user_vault,
            self.get_user_tx,
            self.create_vault,
            self.set_pix_key,
            self.transfer,
            self.deposit,
            self.withdrawal
        ]

        wallet_functions_with_persist_perms = [
            self.transfer,
            self.deposit,
            self.withdrawal,
            self.paybrokers_webhook
        ]

        for fn in wallet_functions_with_cognito_dynamo_perms:
            self.functions_that_need_cognito_permissions.append(fn)
            self.functions_that_need_dynamo_permissions.append(fn)

        for fn in wallet_functions_with_persist_perms:
            if fn not in self.functions_that_need_dynamo_permissions:
                self.functions_that_need_dynamo_permissions.append(fn)

            self.functions_that_need_elasticache_permissions.append(fn)