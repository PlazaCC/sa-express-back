from typing import Any
from collections.abc import Callable

from src.shared.wallet.utils import now_timestamp

class TXLogs:
    error: str
    timestamp: int
    data: dict | None
    resolved: bool

    populate_sign_data: Callable[[], tuple[str, Any]] | None = None

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXLogs':
        return TXLogs(
            error=data['error'],
            timestamp=data['timestamp'],
            data=data['data'] if 'data' in data else None,
            resolved=data['resolved']
        )
    
    @staticmethod
    def successful(data: dict | None = None, resolved: bool = False) -> 'TXLogs':
        return TXLogs(
            error='',
            timestamp=now_timestamp(),
            data=data,
            resolved=resolved
        )

    @staticmethod
    def failed(error: str) -> 'TXLogs':
        return TXLogs(
            error=error, 
            timestamp=now_timestamp()
        )
    
    def __init__(self, error: str, timestamp: int, \
        data: dict | None = None, resolved: bool = False):
        self.error = error
        self.timestamp = timestamp
        self.data = data
        self.resolved = resolved

    def to_tx_snapshot(self) -> dict:
        result = {
            'error': self.error,
            'timestamp': str(self.timestamp),
            'resolved': self.resolved
        }

        if self.data is not None:
            result['data'] = self.data

        return result
    
    def with_error(self) -> bool:
        return self.error != ''
    
    def without_error(self) -> bool:
        return self.error == ''