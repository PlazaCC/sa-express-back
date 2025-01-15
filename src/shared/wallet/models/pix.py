from src.shared.wallet.enums.pix import PIX_KEY_TYPE

class PIXKey:
    type : PIX_KEY_TYPE
    value: str

    @staticmethod
    def from_dict_static(data: dict) -> 'PIXKey':
        return PIXKey(type=PIX_KEY_TYPE[data['type']], value=data['value'])
    
    def __init__(self, type: PIX_KEY_TYPE, value: str):
        self.type = type
        self.value = value

    def to_dict(self) -> dict:
        return {
            'type': self.type.value,
            'value': self.value
        }