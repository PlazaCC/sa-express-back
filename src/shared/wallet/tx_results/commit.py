from src.shared.wallet.utils import now_timestamp

class TXCommitResult:
    error: str
    timestamp: int

    @staticmethod
    def successful() -> 'TXCommitResult':
        return TXCommitResult(
            error='',
            timestamp=now_timestamp()
        )

    @staticmethod
    def failed(error: str) -> 'TXCommitResult':
        return TXCommitResult(error=error, timestamp=now_timestamp())
    
    @staticmethod
    def from_dict_static(data: dict) -> 'TXCommitResult':
        return TXCommitResult(
            error=data['error'],
            timestamp=int(data['timestamp'])
        )

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXCommitResult':
        return TXCommitResult.from_dict_static(data)
    
    def __init__(self, error: str, timestamp: int):
        self.error = error
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'error': self.error,
            'timestamp': str(self.timestamp)
        }
    
    def to_tx_snapshot(self):
        return self.to_dict()

    def with_error(self):
        return self.error != ''
    
    def without_error(self):
        return self.error == ''