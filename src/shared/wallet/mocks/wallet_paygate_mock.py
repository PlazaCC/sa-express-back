from src.shared.wallet.decimal import Decimal
from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.wrappers.paygate import IWalletPayGate

class WalletPayGateMock(IWalletPayGate):
    def __init__(self):
        self.pending_payments = []
        self.webhook_token = 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2YTZjYjY2NC03NzI4LTR'

    ### OVERRIDE METHODS ###
    
    ### PIX ###
    async def post_pix_deposit(self, paygate_ref: str, amount: Decimal) -> dict:
        self.pending_payments.append(paygate_ref)

        req_payload =  {
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
    
        return {
            'statusCode': 'Done',
            'data': {
                'transaction': {
                    'id': '9947b80a-8107-4264-938d-56a7f43593f5',
                    'orderId': paygate_ref,
                    'date': '2023-10-27T01:58:14.573Z',
                    'state': 'Registered',
                    'amount': str(amount)
                },
                'payment': {
                    'qrCode': '76616684937466847221br.gov.bcb.pix2564qrcode.sandbox.paybrokers.solutions/QR/cob/504920436013785957047772193456164644706748877985089166204308PayBrokers Cobrança e Serviço em Tecnologia Ltda78445932284303602542***BA5BD701',
                    'qrCodeLocation': 'https://api.sandbox.paybrokers.solutions/v1/system/qrcodeviewer/9947b80a-8107-4264-938d-56a7f43593f5'
                }
            }
        }
    
    async def post_pix_withdrawal(self, paygate_ref: str, amount: Decimal, pix_key: PIXKey) -> dict:
        self.pending_payments.append(paygate_ref)

        req_payload = {
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

        return {
            'statusCode': 'Done',
            'data': {
                'transaction': {
                    'id': '9947b80a-8107-4264-938d-56a7f43593f6',
                    'orderId': paygate_ref,
                    'date': '2023-10-27T01:58:14.573Z',
                    'state': 'Created',
                    'amount': str(amount)
                }
            }
        }