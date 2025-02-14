from src.shared.wallet.utils import now_timestamp

from src.shared.wallet.tx_results.commit import TXCommitResult

class TXPopResult:
    error: str
    timestamp: int
    commit_result: TXCommitResult | None

    @staticmethod
    def successful(commit_result: TXCommitResult | None = None) -> 'TXPopResult':
        return TXPopResult(
            error='',
            timestamp=now_timestamp(),
            commit_result=commit_result
        )

    @staticmethod
    def failed(error: str) -> 'TXPopResult':
        return TXPopResult(error=error, timestamp=now_timestamp())
    
    @staticmethod
    def locked() -> 'TXPopResult':
        return TXPopResult.failed('Locked')
    
    def __init__(self, error: str, timestamp: int, commit_result: TXCommitResult | None = None):
        self.error = error
        self.timestamp = timestamp
        self.commit_result = commit_result
    
    def to_dict(self):
        result = {
            'error': self.error,
            'timestamp': self.timestamp
        }

        if self.commit_result is not None:
            result['commit_result'] = self.commit_result.to_dict()

        return result

    def with_error(self):
        if self.error != '':
            return True
        
        if self.commit_result is not None and self.commit_result.with_error():
            return True

        return False
    
    def without_error(self):
        return not self.with_error()