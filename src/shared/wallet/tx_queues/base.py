from typing import Any

from src.shared.domain.entities.tx import TX

class TXBaseQueue:
    tx_proc: Any

    def __init__(self, tx_proc: Any):
        self.tx_proc = tx_proc

    async def push_tx(self, tx: TX):
        pass

    
