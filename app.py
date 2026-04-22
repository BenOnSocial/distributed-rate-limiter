import time
from risk_engine import RedisRateLimiter


def main():
    rate_limiter = RedisRateLimiter()

    for i in range(7):
        allowed = rate_limiter.is_allowed(ip_address="192.168.1.1", timestamp=time.time_ns())
        print(f"Request {i+1}: {'Allowed' if allowed else 'Blocked'}")

if __name__ == '__main__':
    main()
