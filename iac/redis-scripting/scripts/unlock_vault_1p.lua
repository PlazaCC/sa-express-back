local VAULT_KEY = KEYS[1];

local VAULT_EXISTS = redis.call("EXISTS", VAULT_KEY);

if (VAULT_EXISTS == 1)
then
    redis.call("HSET", VAULT_KEY, "locked", "0");
end;

return nil;