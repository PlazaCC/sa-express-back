from src.shared.wallet.utils import now_timestamp

class TXCommitResult:
    error: str
    timestamp: str

    @staticmethod
    def successful() -> 'TXCommitResult':
        return TXCommitResult(
            error='',
            timestamp=now_timestamp()
        )

    @staticmethod
    def failed(error: str) -> 'TXCommitResult':
        return TXCommitResult(error=error, timestamp=now_timestamp())
    
    def __init__(self, error: str, timestamp: str):
        self.error = error
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'error': self.error,
            'timestamp': self.timestamp
        }

    def with_error(self):
        return self.error != ''
    
    def without_error(self):
        return self.error == ''