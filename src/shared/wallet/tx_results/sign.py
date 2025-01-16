from src.shared.wallet.utils import now_timestamp

class TXSignResult:
    error: str
    timestamp: str

    @staticmethod
    def successful() -> 'TXSignResult':
        return TXSignResult(
            error='',
            timestamp=now_timestamp()
        )

    @staticmethod
    def failed(error: str) -> 'TXSignResult':
        return TXSignResult(error=error, timestamp=now_timestamp())
    
    def __init__(self, error: str, timestamp: str):
        self.error = error
        self.timestamp = timestamp