import pytest

from src.shared.wallet.enums.pix import PIX_KEY_TYPE
from src.shared.wallet.models.pix import PIXKey

class Test_PIX:
    ### TEST METHODS ###
    # @pytest.mark.skip(reason='')
    def test_validate_cpf(self):
        valid_cpfs = [
            '85223578970',
            '51271235846',
            '18446127407'
        ]

        for cpf in valid_cpfs:
            valid = PIXKey.validate(PIX_KEY_TYPE.CPF, cpf)
            
            assert valid

        invalid_cpfs = [
            '',
            '00000000000',
            '85223578932'
        ]
        
        for cpf in invalid_cpfs:
            valid = PIXKey.validate(PIX_KEY_TYPE.CPF, cpf)
        
            assert not valid

    # @pytest.mark.skip(reason='')
    def test_validate_phone(self):
        valid_phones = [
            '9321099140',
            '6647780706',
            '9626984275',
            '4654602278',
            '35973706977',
            '4946208054',
            '7922367870',
            '1232545080',
            '34996889259',
            '3548502400',
            '53966321651'
        ]

        for phone in valid_phones:
            valid = PIXKey.validate(PIX_KEY_TYPE.PHONE, phone)

            assert valid

        invalid_phones = [
            '',
            '9321099140000',
            '6547780706000',
            '1126984275000',
            '105460227812121',
            '53535973706977132321',
            '554946208054423432',
            '51792236787023232',
            '55123254508011',
            '55349968892592',
            '5035485024003',
            '55539663216511',
            '550000000000',
            'asaoppo1212121031'
        ]

        for phone in invalid_phones:
            valid = PIXKey.validate(PIX_KEY_TYPE.PHONE, phone)

            assert not valid

    # @pytest.mark.skip(reason='')
    def test_validate_email(self):
        valid_emails = [
            'my.ownsite@our-earth.org',
            'bbirth@yahoo.com',
            'rfisher@hotmail.com',
            'ntegrity@aol.com',
            'jdhildeb@comcast.net',
            'library@yahoo.ca',
        ]

        for email in valid_emails:
            valid = PIXKey.validate(PIX_KEY_TYPE.EMAIL, email)

            assert valid

        invalid_emails = [
            '',
            'invalidemail'
        ]

        for email in invalid_emails:
            valid = PIXKey.validate(PIX_KEY_TYPE.EMAIL, email)

            assert not valid

    # @pytest.mark.skip(reason='')
    def test_validate_rng(self):
        valid_rngs = [
            'dcta478j-196l-03fm-t6gh-4298er7845m2'
        ]

        for rng in valid_rngs:
            valid = PIXKey.validate(PIX_KEY_TYPE.RNG, rng)

            assert valid