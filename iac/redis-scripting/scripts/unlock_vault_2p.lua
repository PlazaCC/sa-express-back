local VAULT_1_KEY = KEYS[1];
local VAULT_2_KEY = KEYS[2];

local VAULT_1_EXISTS = redis.call("EXISTS", VAULT_1_KEY);

if (VAULT_1_EXISTS == 1)
then
    redis.call("HSET", VAULT_1_KEY, "locked", "0");
end;

local VAULT_2_EXISTS = redis.call("EXISTS", VAULT_2_KEY);

if (VAULT_2_EXISTS == 1)
then
    redis.call("HSET", VAULT_2_KEY, "locked", "0");
end;

return nil;