import random
from datetime import datetime

from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.vault_type_num import VAULT_TYPE
from src.shared.domain.enums.user_status_enum import USER_STATUS

from src.shared.domain.entities.user import User
from src.shared.domain.entities.vault import Vault
from src.shared.domain.entities.tx import TX

from src.shared.wallet.models.pix import PIXKey
from src.shared.wallet.wrappers.repository import RepositoryWrapper

class RepositoryMock(RepositoryWrapper):
    def __init__(self):
        self.users = []
        self.vaults = []
        self.transactions = []

    ### DEBUG-ONLY METHODS ###
    async def get_user_by_user_id(self, user_id: int) -> tuple[str | None, User | None]:
        rep_user = next((u for u in self.users if u['user_id'] == user_id), None)

        return (None, User.from_dict_static(rep_user)) if rep_user is not None else (None, None)
    
    def _generate_users(self, config: dict) -> list[User]:
        num_users = config['num_users'] if 'num_users' in config else 1

        role_list = config['role'] if 'role' in config else ([ r.value for r in ROLE ])
        user_status_list = config['user_status'] if 'user_status' in config else ([ s.value for s in USER_STATUS ])

        now = datetime.now()

        users = []

        for i in range(num_users):
            name = 'user-mock-' + str(i)

            role = random.choice(role_list)
            user_status = random.choice(user_status_list)

            user = User.from_dict_static({
                "user_id": i,
                "name": name,
                "email": i,
                "role": role,
                "user_status": user_status,
                "created_at": str(now.timestamp()),
                "updated_at": str(now.timestamp()),
                "email_verified": True,
                "enabled": True
            })

            users.append(user.to_dict())

        return users

    def generate_users(self, config: dict) -> list[User]:
        users = self._generate_users(config)

        if 'append' in config:
            self.users += users
        else:
            self.users = users

        return self.users

    def get_all_users(self) -> list[User]:
        return ([ User.from_dict_static(u) for u in self.users ])
    
    def get_all_user_vaults(self) -> list[Vault]:
        return ([ Vault.from_dict_static(v) for v in self.vaults if v['type'] == VAULT_TYPE.USER.value ])

    def get_random_user(self) -> User:
        return User.from_dict_static(random.choice(self.users))
    
    def get_random_vault(self) -> Vault:
        user = self.get_random_user()

        rep_vault = next((v for v in self.vaults if v['user_id'] == user.user_id), None)

        return Vault.from_dict_static(rep_vault) if rep_vault is not None else None
    
    async def set_vault_pix_by_user_id(self, user_id: int, pix_key: PIXKey) -> str | None:
        (_, rep_vault) = await self.get_vault_by_user_id(user_id)

        if rep_vault is None:
            return None
        
        rep_vault.pix_key = pix_key

        return await self.set_vault(rep_vault)
    
    ### OVERRIDE METHODS ###
    async def set_vault(self, vault: Vault) -> str | None:
        (get_error, rep_vault) = await self.get_vault_by_user_id(vault.user_id)

        if get_error is not None:
            return get_error

        if rep_vault is not None:
            rep_vault_key = rep_vault.to_identity_key()

            self.vaults = [ v for v in self.vaults if Vault.from_dict_static(v).to_identity_key() != rep_vault_key ]

        self.vaults.append(vault.to_dict())

        return None
    
    async def get_vault_by_user_id(self, user_id: int) -> tuple[str | None, Vault | None]:
        rep_vault = next((v for v in self.vaults if 'user_id' in v and v['user_id'] == user_id), None)

        return (None, Vault.from_dict_static(rep_vault)) if rep_vault is not None else (None, None)

    async def get_vault_by_server_ref(self, server_ref: str) -> tuple[str | None, Vault | None]:
        rep_vault = next((v for v in self.vaults if 'server_ref' in v and v['server_ref'] == server_ref), None)

        return (None, Vault.from_dict_static(rep_vault)) if rep_vault is not None else (None, None)
    
    async def set_transaction(self, tx: TX) -> str | None:
        rep_tx = next((t for t in self.transactions if t['tx_id'] == tx.tx_id), None)
        
        if rep_tx is not None:
            self.transactions = [ t for t in self.transactions if t['tx_id'] != tx.tx_id ]

        self.transactions.append(tx.to_dict())

        return None
    
    async def get_transaction(self, tx_id: str) -> tuple[str | None, TX | None]:
        rep_tx = next((t for t in self.transactions if t['tx_id'] == tx_id), None)

        return (None, TX.from_dict_static(rep_tx)) if rep_tx is not None else (None, None)