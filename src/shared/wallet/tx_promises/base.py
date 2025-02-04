class TXBasePromise:
    def __init__(self):
        pass

    def to_dict(self) -> dict:
        pass

    def is_resolved(self) -> bool:
        pass

    async def call(self) -> str | None:
        pass

    async def resolve(self) -> str | None:
        pass