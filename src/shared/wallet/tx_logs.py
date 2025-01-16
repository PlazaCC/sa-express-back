from src.shared.wallet.utils import now_timestamp

class TXLogs:
    key: str
    error: str
    timestamp: str
    data: dict | None

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXLogs':
        return TXLogs(
            key=data['key'],
            error=data['error'],
            timestamp=data['timestamp'],
            data=data['data'] if 'data' in data else None,
        )
    
    @staticmethod
    def successful(key: str, data: dict | None = None) -> 'TXLogs':
        return TXLogs(
            key=key,
            error='',
            timestamp=now_timestamp(),
            data=data
        )

    @staticmethod
    def failed(key: str, error: str) -> 'TXLogs':
        return TXLogs(
            key=key,
            error=error, 
            timestamp=now_timestamp()
        )
    
    def __init__(self, key: str, error: str, timestamp: str, \
        data: dict | None = None):
        self.key = key
        self.error = error
        self.timestamp = timestamp
        self.data = data

    def to_tx_snapshot(self) -> dict:
        result = {
            'key': self.key,
            'error': self.error,
            'timestamp': self.timestamp,
        }

        if self.data is not None:
            result['data'] = self.data

        return result
    
    def with_error(self) -> bool:
        return self.error != ''