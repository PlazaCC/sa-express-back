import re

from src.shared.wallet.enums.pix import PIX_KEY_TYPE

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
RNG_REGEX = r'[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}'

class PIXKey:
    type : PIX_KEY_TYPE
    value: str

    @staticmethod
    def from_dict_static(data: dict) -> 'PIXKey':
        return PIXKey(type=PIX_KEY_TYPE[data['type']], value=data['value'])
    
    @staticmethod
    def from_api_gateway(data: dict) -> 'PIXKey':
        return PIXKey.from_dict_static(data)
    
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
        value_length = len(value)

        if value_length != 11:
            return False

        digits = re.findall('\\d', value)

        if len(digits) != value_length:
            return False
        
        valid = 0

        for digit in digits:
            valid += int(digit)

        if int(digits[0]) == valid / 11:
            return False

        sum = 0
        count = 10

        for i in range(0, value_length - 2):
            sum += int(digits[i]) * count
            count -= 1
        
        digit10 = 11 - (sum % 11)
        digit10 = '0' if digit10 >= 10 else str(digit10)

        if digit10 != digits[9]:
            return False
        
        sum = 0
        count = 10

        for i in range(1, value_length - 1):
            sum += int(digits[i]) * count
            count -= 1

        digit11 = 11 - (sum % 11)
        digit11 = '0' if digit11 >= 10 else str(digit11)

        if digit11 != digits[10]:
            return False
        
        return True
    
    @staticmethod
    def validate_phone(value: str) -> bool:
        value_length = len(value)

        if value_length < 10 or value_length > 12:
            return False

        digits = re.findall('\\d', value)

        if len(digits) != value_length:
            return False
        
        sum = 0

        for i in range(2, value_length):
            digit_int = int(digits[i])

            if digit_int < 0:
                return False
            
            sum += digit_int

        if sum == 0:
            return False

        return True
    
    @staticmethod
    def validate_email(value: str) -> bool:
        value_length = len(value)

        if value_length < 10 or value_length > 60:
            return False
        
        return re.match(EMAIL_REGEX, value) is not None
    
    @staticmethod
    def validate_rng(value: str) -> bool:
        value_length = len(value)

        if value_length != 36:
            return False
        
        return re.match(RNG_REGEX, value) is not None
    
    def __init__(self, type: PIX_KEY_TYPE, value: str):
        self.type = type
        self.value = value

    def to_dict(self) -> dict:
        return {
            'type': self.type.value,
            'value': self.value
        }
    
    def valid(self) -> bool:
        return PIXKey.validate(self.type, self.value)
    
    def to_url(self) -> str:
        return ''
    
    def to_qrcode(self) -> str:
        return ''