from src.shared.wallet.utils import now_timestamp

from src.shared.wallet.tx_results.sign import TXSignResult

class TXPushResult:
    error: str
    timestamp: str
    sign_result: TXSignResult | None

    @staticmethod
    def successful(sign_result: TXSignResult | None = None) -> 'TXPushResult':
        return TXPushResult(
            error='',
            timestamp=now_timestamp(),
            sign_result=sign_result
        )

    @staticmethod
    def failed(error: str) -> 'TXPushResult':
        return TXPushResult(error=error, timestamp=now_timestamp())
    
    @staticmethod
    def locked() -> 'TXPushResult':
        return TXPushResult.failed('Locked')
    
    def __init__(self, error: str, timestamp: int, sign_result: TXSignResult | None = None):
        self.error = error
        self.timestamp = timestamp
        self.sign_result = sign_result

    def to_dict(self):
        result = {
            'error': self.error,
            'timestamp': str(self.timestamp)
        }

        if self.sign_result is not None:
            result['sign_result'] = self.sign_result.to_dict()

        return result

    def with_error(self):
        if self.error != '':
            return True
        
        if self.sign_result is not None and self.sign_result.with_error():
            return True

        return False
    
    def without_error(self):
        return not self.with_error()