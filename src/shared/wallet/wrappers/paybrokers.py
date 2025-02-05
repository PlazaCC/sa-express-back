import os
import json
import requests

from src.shared.wallet.enums.paygate import PAYGATE
from src.shared.wallet.decimal import Decimal
from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.wrappers.paygate import IWalletPayGate

class Paybrokers(IWalletPayGate):
    name: PAYGATE = PAYGATE.PAYBROKERS

    @staticmethod
    def get_paygate_ref_header(tx_id: str, nonce: str):
        webhook_token = os.environ.get('PAYGATE_WEBHOOK_TOKEN')

        return f'WTK={webhook_token}&TX={tx_id}&NC={nonce}'
    
    def __init__(self):
        self.base_url = os.environ.get('PAYBROKERS_BASE_URL')
        self.auth_token = os.environ.get('PAYBROKERS_AUTH_TOKEN')
    
    def get_webhook_url(self):
        api_base_url = os.environ.get('API_BASE_URL')

        return f'{api_base_url}/mss-saexpress/paybrokers_webhook'
    
    ### PIX ###
    async def post_pix_deposit(self, tx_id: str, nonce: str, amount: Decimal, \
        ref_id: str) -> dict:
        payload =  {
            'payment': {
                'value': {
                    'original': str(amount)
                }
            },
            'transaction': {
                'orderId': ref_id,
                'orderDescription': 'SA-Deposit'
            },
            'webhook': {
                'url': self.get_webhook_url(),
                'customHeaderName': 'X-Webhook-Reference',
                'customHeaderValue': Paybrokers.get_paygate_ref_header(tx_id, nonce)
            }
        }

        url = f'{self.base_url}/v1/partners-int/accounts/pix/cashin'

        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Bearer {self.auth_token}'
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=3)

            return json.loads(response.text)
        except:
            return { 'error': { 'message': 'Paybrokers request failed' } }
    
    async def post_pix_withdrawal(self, tx_id: str, nonce: str, amount: Decimal, \
        pix_key: PIXKey, ref_id: str) -> dict:
        payload = {
            'payment': {
                'key': {
                    'type': pix_key.to_paygate_type(),
                    'value': pix_key.value
                },
                'value': str(amount)
            },
            'transaction': {
                'orderId': ref_id,
                'orderDescription': 'SA-Withdrawal'
            },
            'webhook': {
                'url': self.get_webhook_url(),
                'customHeaderName': 'X-Webhook-Reference',
                'customHeaderValue': Paybrokers.get_paygate_ref_header(tx_id, nonce)
            }
        }

        url = f'{self.base_url}/v1/partners-int/accounts/pix/cashout'

        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Bearer {self.auth_token}'
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=3)

            return json.loads(response.text)
        except:
            return { 'error': { 'message': 'Paybrokers request failed' } }