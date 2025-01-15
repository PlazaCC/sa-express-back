from src.shared.wallet.utils import now_timestamp

class TXLogs:
    error: str
    timestamp: str
    data: dict | None

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXLogs':
        return TXLogs(
            error=data['error'],
            timestamp=data['timestamp'],
            data=data['data'] if 'data' in data else None,
        )
    
    @staticmethod
    def successful(data: dict | None = None) -> 'TXLogs':
        return TXLogs(
            error='',
            timestamp=now_timestamp(),
            data=data
        )

    @staticmethod
    def failed(error: str) -> 'TXLogs':
        return TXLogs(error=error, timestamp=now_timestamp())
    
    def __init__(self, error: str, timestamp: str, data: dict | None = None):
        self.error = error
        self.timestamp = timestamp
        self.data = data

    def to_tx_snapshot(self) -> dict:
        result = {
            'error': self.error,
            'timestamp': self.timestamp,
        }

        if self.data is not None:
            result['data'] = self.data

        return result
    
    def with_error(self) -> bool:
        return self.error != ''