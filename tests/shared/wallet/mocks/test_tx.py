import random
from datetime import datetime

from src.shared.domain.entities.user import User
from src.shared.wallet.tx_processor import TXProcessor
from src.shared.wallet.vault_processor import VaultProcessor

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS

class Test_TXMock:
    def generate_users(self, config):
        num = config['num'] if 'num' in config else 1

        roleList = config['role'] if 'role' in config else ([ r.value for r in ROLE ])
        userStatusList = config['userStatus'] if 'userStatus' in config else ([ s.value for s in USER_STATUS ])

        now = datetime.now()

        users = []

        for i in range(num):
            name = 'user-mock-' + str(i)

            role = random.choice(roleList)
            userStatus = random.choice(userStatusList)

            user = User.from_dict_static({
                "user_id": i,
                "name": name,
                "email": i,
                "role": role,
                "user_status": userStatus,
                "created_at": str(now.timestamp()),
                "updated_at": str(now.timestamp()),
                "email_verified": True,
                "enabled": True
            })

            users.append(user)

        return users

    def test_vaults(self):
        users = self.generate_users({
            'num': 10,
            'userStatus': [ USER_STATUS.CONFIRMED.value ]
        })
                
        vaultProc = VaultProcessor()

        vaults = []

        for user in users:
            config = {}

            vault = vaultProc.createIfNotExists(user, config)

            vaults.append(vault)

        for vault in vaults:
            print(vault.to_dict())

        assert True

