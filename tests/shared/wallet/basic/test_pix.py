import pytest

from src.shared.wallet.enums.pix import PIX_KEY_TYPE
from src.shared.wallet.models.pix import PIXKey

class Test_PIX:
    ### TEST METHODS ###
    # @pytest.mark.skip(reason='')
    def test_validate_cpf(self):
        cpf = '85223578970'

        valid = PIXKey.validate(PIX_KEY_TYPE.CPF, cpf)
        
        assert valid