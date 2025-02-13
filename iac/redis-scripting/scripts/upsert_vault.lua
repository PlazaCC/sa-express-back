local VAULT_KEY = KEYS[1];
local BALANCE = KEYS[2];
local BALANCE_LOCKED = KEYS[3];
local USER_ID = KEYS[4];
local PIX_KEY_TYPE = KEYS[5];
local PIX_KEY_VALUE = KEYS[6];

local VAULT_EXISTS = redis.call("EXISTS", VAULT_KEY);

if (VAULT_EXISTS == 1)
then
    local locked = redis.call("HGET", VAULT_KEY, "locked");

    redis.call("HSET", VAULT_KEY, "locked", locked, "balance", BALANCE, "balance_locked", BALANCE_LOCKED, "user_id", USER_ID, "pix_key_type", PIX_KEY_TYPE, "pix_key_value", PIX_KEY_VALUE); 
    return nil;
end;

redis.call("HSET", VAULT_KEY, "locked", "0", "balance", BALANCE, "balance_locked", BALANCE_LOCKED, "user_id", USER_ID, "pix_key_type", PIX_KEY_TYPE, "pix_key_value", PIX_KEY_VALUE);

return nil;