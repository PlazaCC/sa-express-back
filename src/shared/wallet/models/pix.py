import re

from src.shared.wallet.enums.pix import PIX_KEY_TYPE

class PIXKey:
    type : PIX_KEY_TYPE
    value: str

    @staticmethod
    def from_dict_static(data: dict) -> 'PIXKey':
        return PIXKey(type=PIX_KEY_TYPE[data['type']], value=data['value'])
    
    @staticmethod
    def validate(type: PIX_KEY_TYPE, value: str) -> bool:
        if type == PIX_KEY_TYPE.CPF:
            return PIXKey.validate_cpf(value)
        
        if type == PIX_KEY_TYPE.PHONE:
            return PIXKey.validate_phone(value)
        
        if type == PIX_KEY_TYPE.EMAIL:
            return PIXKey.validate_email(value)
        
        return PIXKey.validate_rng(value)

    @staticmethod
    def validate_cpf(value: str) -> bool:
        if len(value) != 11:
            return False

        digits = re.findall('\\d', value)

        if len(digits) != 11:
            return False
        
        valid = 0

        for digit in digits:
            valid += int(digit)

        if int(digits[0]) == valid / 11:
            return False

        sum = 0
        count = 10

        for i in range(0, len(digits) - 2):
            sum += int(digits[i]) * count
            count -= 1
        
        digit10 = 11 - (sum % 11)
        digit10 = '0' if digit10 >= 10 else str(digit10)

        if digit10 != digits[9]:
            return False
        
        sum = 0
        count = 10

        for i in range(0, len(digits) - 1):
            sum += int(digits[i]) * count
            count -= 1

        digit11 = 11 - (sum % 11)
        digit11 = '0' if digit11 >= 10 else str(digit11)

        if digit11 != digits[10]:
            return False
        
        return True
    
    @staticmethod
    def validate_phone(value: str) -> bool:
        return False
    
    @staticmethod
    def validate_email(value: str) -> bool:
        return False
    
    @staticmethod
    def validate_rng(value: str) -> bool:
        return False
    
    def __init__(self, type: PIX_KEY_TYPE, value: str):
        self.type = type
        self.value = value

    def to_dict(self) -> dict:
        return {
            'type': self.type.value,
            'value': self.value
        }