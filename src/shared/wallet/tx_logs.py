
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
        # return TXTransferInstructionResult(success=False, timestamp=now_timestamp(), error=error)
        pass
    
    def __init__(self, is_error: bool, timestamp: str, data: dict | None = None):
        self.is_error = is_error
        self.timestamp = timestamp
        self.data = data

    def to_tx_snapshot(self) -> dict:
        result = {
            'is_error': self.is_error,
            'timestamp': self.timestamp,
        }

        if self.data is not None:
            result['data'] = self.data

        return result