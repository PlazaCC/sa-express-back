class TXLogs:
    is_error: bool
    message: str
    timestamp: str

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXLogs':
        return TXLogs(
            is_error=data['is_error'],
            message=data['message'],
            timestamp=data['timestamp']
        )
    
    def __init__(self, is_error: bool, message: str, timestamp: str):
        self.is_error = is_error
        self.message = message
        self.timestamp = timestamp

    def to_tx_snapshot(self) -> dict:
        return {
            'is_error': self.is_error,
            'message': self.message,
            'timestamp': self.timestamp
        }