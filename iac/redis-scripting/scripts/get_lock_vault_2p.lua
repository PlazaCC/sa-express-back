local VAULT_1_KEY = KEYS[1];
local VAULT_2_KEY = KEYS[2];

local VAULT_1_LOCKED = redis.call("HGET", VAULT_1_KEY, "locked");

if (type(VAULT_1_LOCKED) == "boolean")
then
    return "MISS";
end;

if (VAULT_1_LOCKED == "1") then return "LOCKED" end;

local VAULT_2_LOCKED = redis.call("HGET", VAULT_2_KEY, "locked");

if (type(VAULT_2_LOCKED) == "boolean")
then
    return "MISS";
end;

if (VAULT_2_LOCKED == "1") then return "LOCKED" end;

redis.call("HSET", VAULT_1_KEY, "locked", "1");
redis.call("HSET", VAULT_2_KEY, "locked", "1");

local RESULT = {};

RESULT[1] = redis.call("HGETALL", VAULT_1_KEY);
RESULT[2] = redis.call("HGETALL", VAULT_2_KEY);

return RESULT;