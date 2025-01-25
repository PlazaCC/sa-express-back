import json
import requests

from src.shared.wallet.decimal import Decimal
from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.wrappers.paygate import IWalletPayGate

class Paybrokers(IWalletPayGate):
    def __init__(self):
        self.base_url = 'https://api.sandbox.paybrokers.solutions/v1/partners-int/accounts'
        self.auth_token = 'placeholder'
        self.webhook_token = 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2YTZjYjY2NC03NzI4LTR'
    
    ### PIX ###
    async def post_pix_deposit(self, paygate_ref: str, amount: Decimal) -> dict:
        payload =  {
            'payment': {
                'value': {
                    'original': str(amount)
                }
            },
            'transaction': {
                'orderId': paygate_ref,
                'orderDescription': 'SA-Deposit'
            },
            'webhook': {
                'url': 'https://postman-echo.com/post?test=1',
                'customHeaderName': 'PaygateAuth',
                'customHeaderValue': f'WTK={self.webhook_token}&{paygate_ref}'
            }
        }

        url = f'{self.base_url}/pix/cashin'

        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Bearer {self.auth_token}'
        }

        response = requests.post(url, json=payload, headers=headers, timeout=3)

        try:
            return json.loads(response.text)
        except:
            return { 'error': { 'message': 'Paybrokers request failed' } }
    
    async def post_pix_withdrawal(self, paygate_ref: str, amount: Decimal, pix_key: PIXKey) -> dict:
        payload = {
            'payment': {
                'key': {
                    'type': pix_key.to_paygate_type(),
                    'value': pix_key.value
                },
                'value': str(amount)
            },
            'transaction': {
                'orderId': paygate_ref,
                'orderDescription': 'SA-Withdrawal'
            },
            'webhook': {
                'url': 'https://postman-echo.com/post?test=1',
                'customHeaderName': 'PaygateAuth',
                'customHeaderValue': f'WTK={self.webhook_token}&{paygate_ref}'
            }
        }

        url = f'{self.base_url}/pix/cashout'

        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Bearer {self.auth_token}'
        }

        response = requests.post(url, json=payload, headers=headers, timeout=3)

        try:
            return json.loads(response.text)
        except:
            return { 'error': { 'message': 'Paybrokers request failed' } }