import pytest

from src.shared.wallet.enums.pix import PIX_KEY_TYPE
from src.shared.wallet.models.pix import PIXKey

class Test_PIX:
    ### TEST METHODS ###
    # @pytest.mark.skip(reason='')
    def test_validate_cpf(self):
        cpf1 = '85223578970'

        valid = PIXKey.validate(PIX_KEY_TYPE.CPF, cpf1)
        
        assert valid

        cpf2 = '00000000000'

        valid = PIXKey.validate(PIX_KEY_TYPE.CPF, cpf2)
        
        assert not valid

    # @pytest.mark.skip(reason='')
    def test_validate_phone(self):
        valid_phones = [
            '559321099140',
            '556647780706',
            '559626984275',
            '554654602278',
            '5535973706977',
            '554946208054',
            '557922367870',
            '551232545080',
            '5534996889259',
            '553548502400',
            '5553966321651',
            '5551983163311'
        ]

        for phone in valid_phones:
            valid = PIXKey.validate(PIX_KEY_TYPE.PHONE, phone)

            assert valid

        invalid_phones = [
            '559321099140000',
            '556547780706000',
            '551126984275000',
            '55105460227812121',
            '53535973706977132321',
            '554946208054423432',
            '51792236787023232',
            '55123254508011',
            '55349968892592',
            '5035485024003',
            '55539663216511',
            '55519831633112',
            '550000000000',
        ]

        for phone in invalid_phones:
            valid = PIXKey.validate(PIX_KEY_TYPE.PHONE, phone)

            assert not valid