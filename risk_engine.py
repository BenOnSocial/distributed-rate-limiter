import redis


ATOMIC_IS_ALLOWED_SCRIPT = """
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

-- 1. Remove timestamps older than the window
redis.call('ZREMRANGEBYSCORE', key, 0, now - window)

-- 2. Count current requests
local count = redis.call('ZCARD', key)

if count < limit then
    -- 3. Add current request and set expiry to auto-clean memory
    redis.call('ZADD', key, now, now)
    redis.call('EXPIRE', key, window)
    return 1 -- Allowed
else
    return 0 -- Blocked
end
"""


class RedisRateLimiter(object):
    def __init__(self, host="redis", port=6379):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)
        self._ip_address_limit: int = 5
        self._ttl_window_seconds: int = 60 * 1000000000

        self.script = self.r.register_script(ATOMIC_IS_ALLOWED_SCRIPT)

    def is_allowed(self, ip_address: str, timestamp: int) -> bool:
        return self.script(keys=[f"rate_limit:{ip_address}"], args=[timestamp, self._ttl_window_seconds, self._ip_address_limit]) == 1
