local VAULT_1_LOCK_KEY = KEYS[2];
local VAULT_2_LOCK_KEY = KEYS[4];

local VAULT_1_LOCK_RESULT = redis.call("EXISTS", VAULT_1_LOCK_KEY);

if (VAULT_1_LOCK_RESULT == 1) then return "LOCKED" end;

local VAULT_2_LOCK_RESULT = redis.call("EXISTS", VAULT_2_LOCK_KEY);

if (VAULT_2_LOCK_RESULT == 1) then return "LOCKED" end;

local VAULT_1_KEY = KEYS[1];
local VAULT_1_DATA = redis.call("JSON.GET", VAULT_1_KEY, "$");

if (not VAULT_1_DATA) then return "MISS" end;

local VAULT_2_KEY = KEYS[3];
local VAULT_2_DATA = redis.call("JSON.GET", VAULT_2_KEY, "$");

if (not VAULT_2_DATA) then return "MISS" end;

redis.call("SET", VAULT_1_LOCK_KEY, "1", "NX", "EX", "5");
redis.call("SET", VAULT_2_LOCK_KEY, "1", "NX", "EX", "5");

local RESULT = {};

RESULT[1] = VAULT_1_DATA;
RESULT[2] = VAULT_2_DATA;

return RESULT;



