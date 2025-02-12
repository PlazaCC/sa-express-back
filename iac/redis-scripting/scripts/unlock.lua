local VAULT_1_LOCK_KEY = KEYS[1];
local VAULT_2_LOCK_KEY = KEYS[2];

redis.call("DEL", VAULT_1_LOCK_KEY);
redis.call("DEL", VAULT_2_LOCK_KEY);