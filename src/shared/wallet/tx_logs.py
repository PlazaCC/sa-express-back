from typing import Any
from collections.abc import Callable

from src.shared.wallet.utils import now_timestamp

class TXLogs:
    key: str
    error: str
    timestamp: str
    data: dict | None
    resolved: bool

    populate_sign_data: Callable[[], tuple[str, Any]] | None = None

    @staticmethod
    def from_tx_snapshot(data: dict) -> 'TXLogs':
        return TXLogs(
            key=data['key'],
            error=data['error'],
            timestamp=data['timestamp'],
            data=data['data'] if 'data' in data else None,
            resolved=data['resolved']
        )
    
    @staticmethod
    def successful(key: str, data: dict | None = None, resolved: bool = False) -> 'TXLogs':
        return TXLogs(
            key=key,
            error='',
            timestamp=now_timestamp(),
            data=data,
            resolved=resolved
        )

    @staticmethod
    def failed(key: str, error: str) -> 'TXLogs':
        return TXLogs(
            key=key,
            error=error, 
            timestamp=now_timestamp()
        )
    
    @staticmethod
    def get_instruction_log_key(instr_index: int) -> str:
        return f'INSTR={instr_index}'
    
    def __init__(self, key: str, error: str, timestamp: str, \
        data: dict | None = None, resolved: bool = False):
        self.key = key
        self.error = error
        self.timestamp = timestamp
        self.data = data
        self.resolved = resolved

    def to_tx_snapshot(self) -> dict:
        result = {
            'key': self.key,
            'error': self.error,
            'timestamp': self.timestamp,
            'resolved': self.resolved
        }

        if self.data is not None:
            result['data'] = self.data

        return result
    
    def with_error(self) -> bool:
        return self.error != ''
    
    def without_error(self) -> bool:
        return self.error == ''