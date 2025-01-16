from src.shared.wallet.utils import now_timestamp

class TXSignResult:
    error: str
    timestamp: str
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
    
    def __init__(self, error: str, timestamp: str, data: dict | None = None):
        self.error = error
        self.timestamp = timestamp
        self.data = data

    def to_dict(self):
        return {
            'error': self.error,
            'timestamp': self.timestamp,
            'data': self.data
        }

    def with_error(self):
        return self.error != ''
    
    def without_error(self):
        return self.error == ''