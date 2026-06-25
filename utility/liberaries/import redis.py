import redis
import os
from dotenv import load_dotenv
load_dotenv()

redis_client = redis.StrictRedis(
        host='replica.stage-redis-cache.8l2ixg.aps1.cache.amazonaws.com',
        port= 6379,
            username= os.getenv("REDIS_USER_NAME") or 'kuldeep.sachan',
            password= os.getenv("REDIS_PASSWORD") or 'K^1d33pXn0!$32025',
        ssl=True,
        decode_responses=True
    )
key1 = 'APP-AUTH-2-USER-LUNA-OTP-email-kuldeep.sachan@nexxbase.com'
otp = redis_client.get(key1)
print(otp)  