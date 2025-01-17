from typing import Any

from src.shared.wallet.tx_queues.base import TXBaseQueue

class TXServerSingleQueue(TXBaseQueue):
    tx_proc: Any

    def __init__(self, tx_proc: Any):
        self.tx_proc = tx_proc