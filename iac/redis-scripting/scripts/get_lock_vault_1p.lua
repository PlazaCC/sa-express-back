local VAULT_KEY = KEYS[1];

local VAULT_LOCKED = redis.call("HGET", VAULT_KEY, "locked");

if (type(VAULT_LOCKED) == "boolean")
then
    return "MISS";
end;

if (VAULT_LOCKED == "1") then return "LOCKED" end;

redis.call("HSET", VAULT_KEY, "locked", "1");

return redis.call("HGETALL", VAULT_KEY);