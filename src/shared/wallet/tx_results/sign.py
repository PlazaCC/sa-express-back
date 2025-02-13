from src.shared.wallet.utils import now_timestamp

class TXSignResult:
    error: str
    timestamp: int
    data: dict

    @staticmethod
    def successful(data: dict = {}) -> 'TXSignResult':
        return TXSignResult(
            error='',
            timestamp=now_timestamp(),
            data=data
        )
    
    @staticmethod
    def failed(error: str, data: dict = {}) -> 'TXSignResult':
        return TXSignResult(error=error, timestamp=now_timestamp(), data=data)
    
    @staticmethod
    def from_dict_static(data: dict) -> 'TXSignResult':
        return TXSignResult(
            error=data['error'],
            timestamp=int(data['timestamp']),
            data=data['data']
        )

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXSignResult':
        return TXSignResult.from_dict_static(data)
    
    def __init__(self, error: str, timestamp: int, data: dict | None = None):
        self.error = error
        self.timestamp = timestamp
        self.data = data

    def to_dict(self):
        return {
            'error': self.error,
            'timestamp': str(self.timestamp),
            'data': self.data
        }
    
    def to_tx_snapshot(self):
        return self.to_dict()

    def with_error(self):
        return self.error != ''
    
    def without_error(self):
        return self.error == ''
    
    def clone(self):
        sign_dict = self.to_dict()

        sign_dict['data'] = self.data.copy()

        return TXSignResult.from_dict_static(sign_dict)