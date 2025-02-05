import os

from src.shared.wallet.enums.paygate import PAYGATE
from src.shared.wallet.decimal import Decimal
from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.wrappers.paygate import IWalletPayGate

class WalletPayGateMock(IWalletPayGate):
    name: PAYGATE = PAYGATE.MOCK

    @staticmethod
    def get_paygate_ref_header(tx_id: str, nonce: str):
        webhook_token = os.environ.get('PAYGATE_WEBHOOK_TOKEN')

        return f'WTK={webhook_token}&TX={tx_id}&NC={nonce}'

    def __init__(self):
        self.pending_payments = []
        self.auth_token = ''

    ### OVERRIDE METHODS ###

    ### PIX ###
    async def post_pix_deposit(self, tx_id: str, nonce: str, amount: Decimal, \
        ref_id: str) -> dict:
        webhook_ref_header = WalletPayGateMock.get_paygate_ref_header(tx_id, nonce)

        self.pending_payments.append(webhook_ref_header)

        req_payload =  {
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
                'url': 'https://postman-echo.com/post?test=1',
                'customHeaderName': 'X-Webhook-Reference',
                'customHeaderValue': webhook_ref_header
            }
        }
    
        return {
            'statusCode': 'Done',
            'data': {
                'transaction': {
                    'id': 'f6431a0f-970a-4be9-9c6d-f444f729adc3',
                    'orderId': ref_id,
                    'date': '2023-10-27T01:58:14.573Z',
                    'state': 'Registered',
                    'amount': str(amount)
                },
                'payment': {
                    'qrCode': '76616684937466847221br.gov.bcb.pix2564qrcode.sandbox.paybrokers.solutions/QR/cob/504920436013785957047772193456164644706748877985089166204308PayBrokers Cobrança e Serviço em Tecnologia Ltda78445932284303602542***BA5BD701',
                    'qrCodeLocation': 'https://api.sandbox.paybrokers.solutions/v1/system/qrcodeviewer/f6431a0f-970a-4be9-9c6d-f444f729adc3'
                }
            }
        }
    
    async def post_pix_withdrawal(self, tx_id: str, nonce: str, amount: Decimal, pix_key: PIXKey, \
        ref_id: str) -> dict:
        webhook_ref_header = WalletPayGateMock.get_paygate_ref_header(tx_id, nonce)

        self.pending_payments.append(webhook_ref_header)

        req_payload = {
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
                'url': 'https://postman-echo.com/post?test=1',
                'customHeaderName': 'X-Webhook-Reference',
                'customHeaderValue': webhook_ref_header
            }
        }
        
        return {
            'statusCode': 'Done',
            'data': {
                'transaction': {
                    'id': 'f6431a0f-970a-4be9-9c6d-f444f729adc3',
                    'orderId': tx_id,
                    'date': '2023-10-27T01:58:14.573Z',
                    'state': 'Created',
                    'amount': str(amount)
                }
            }
        }