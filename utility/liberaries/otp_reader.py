# python
"""
OTP reader utilities for mobile test automation.

Provides:
- read_otp_from_redis(...): poll Redis for a key/value and extract OTP using regex
- read_otp_from_mail(...): poll an IMAP mailbox and extract OTP from the latest matching message
- parse_otp_from_text(text, otp_regex): utility to extract OTP using regex

Notes:
- Depends on `redis` (redis-py), `imapclient`, and `pyzmail36` packages. These are listed in requirements.txt.
- Email servers and Appium test environments may require app-specific parsing rules; pass a custom `otp_regex` if needed.
"""
from __future__ import annotations

import os
import re
import time
import logging
from typing import Optional


logger = logging.getLogger(__name__)


def parse_otp_from_text(text: str, otp_regex: str = r"(\d{4,8})") -> Optional[str]:
    """
    Extract the first matching OTP from `text` using `otp_regex`.
    Returns the OTP string or None if not found.
    """
    if not text:
        return None
    m = re.search(otp_regex, text)
    if m:
        return m.group(1)
    return None


def _safe_decode_redis_val(val) -> str:
    """Helper to safely decode redis bytes/bytearray to string."""
    try:
        return val.decode("utf-8") if isinstance(val, (bytes, bytearray)) else str(val)
    except Exception:
        return str(val)
"""
try:
        print("\n[Step 6/8] Fetching OTP from Redis...")
        
        redis_client = redis.StrictRedis(
            host='replica.stage-redis-cache.8l2ixg.aps1.cache.amazonaws.com',
            port=6379,
            username='bashisht-kumar',
            password='BashishtKumar21@2025',
            ssl=True,
            decode_responses=True
        )
        
        email_key = 'APP-AUTH-2-USER-WATCH-OTP-email-bashishtg22@gmail.com'
        otp = redis_client.get(email_key)
        
        assert otp, f"OTP not found in Redis for key: {email_key}"
        print(f"✅ OTP fetched from Redis: {otp}")
        
    except Exception as e:
        print(f"❌ Failed to get OTP from Redis: {str(e)[:150]}")
        raise"""

def read_otp_from_redis(
    redis_client=None,
    redis_url: Optional[str] = None,
    key: Optional[str] = None,
    key_pattern: Optional[str] = None,
    timeout: int = 30,
    poll_interval: float = 1.0,
    otp_regex: str = r"(\d{4,8})",
    delete_after_read: bool = False,
) -> Optional[str]:
    """
    Poll Redis for a key or keys and extract an OTP.

    Args:
      redis_client: optional pre-created redis.Redis instance. If omitted, `redis_url` will be used to create one.
      redis_url: redis connection URL (e.g. redis://localhost:6379/0). If None, reads REDIS_URL from env.
      key: exact key to poll (preferred). If provided, the function GETs the key.
      key_pattern: pattern for matching keys (e.g. "otp:*"). If `key` is None, the function will SCAN for matching keys.
      timeout: total seconds to poll before giving up.
      poll_interval: seconds between polls.
      otp_regex: regex to extract OTP from the value.
      delete_after_read: delete the key after reading it (best-effort).

    Returns the OTP string if found, otherwise None.
    """
    try:
        import redis
    except Exception as e:  # pragma: no cover - import-time error
        raise RuntimeError("redis package is required for read_otp_from_redis: install redis") from e

    if redis_client is None:
        url =  os.getenv("REDIS_URL") or redis_url
        if not url:
            raise ValueError("redis_client or redis_url (or REDIS_URL env) must be provided")
        redis_client = redis.StrictRedis(
            host=url,
            port= int(os.getenv("REDIS_PORT", 6379)),
            username= os.getenv("REDIS_USER_NAME") or 'kuldeep.sachan',
            password= os.getenv("REDIS_PASSWORD") or 'K^1d33pXn0!$32025',
            ssl=True,
            decode_responses=True
        )
    end = time.time() + float(timeout)
    last_error = None
    #  kuldeep_sachan
    #  K^1d33pXn0!$32025
    # "redis://:K^1d33pXn0!$32025@replica.stage-redis-cache.8l2ixg.aps1.cache.amazonaws.com:6379/0?decode_responses=True"
    while time.time() < end:
        try:
            if key:
                val = redis_client.get(key)
                if val:
                    # redis returns bytes -> decode
                    text = _safe_decode_redis_val(val)
                    otp = parse_otp_from_text(text, otp_regex)
                    if otp:
                        if delete_after_read:
                            try:
                                redis_client.delete(key)
                            except Exception:
                                logger.debug("Failed to delete redis key %s after read", key, exc_info=True)
                        return otp
                else:
                    logger.debug("Key '%s' not found in Redis. Retrying...", key)
        except Exception as e:
            last_error = e
            logger.debug("Error polling redis for OTP: %s", e, exc_info=True)

        time.sleep(poll_interval)

    # timed out
    if last_error:
        logger.debug("read_otp_from_redis last error: %s", last_error)
    return None


def read_otp_by_email(
    email: str,
    redis_client=None,
    redis_url: Optional[str] = None,
    timeout: int = 30,
    poll_interval: float = 1.0,
    otp_regex: str = r"(\d{4,8})",
    delete_after_read: bool = False,
) -> Optional[str]:
    """
    Fetch OTP from Redis for a specific email using the key pattern:
    APP-AUTH-2-USER-LUNA-OTP-email-{email}
    """
    key = f"APP-AUTH-2-USER-LUNA-OTP-email-{email.strip()}"
    logger.info("Attempting to read OTP from Redis with key: %s", key)
    return read_otp_from_redis(
        redis_client=redis_client,
        redis_url=redis_url,
        key=key,
        timeout=timeout,
        poll_interval=poll_interval,
        otp_regex=otp_regex,
        delete_after_read=delete_after_read,
    )


def read_otp_by_mobile(
    mobile: str,
    redis_client=None,
    redis_url: Optional[str] = None,
    timeout: int = 30,
    poll_interval: float = 1.0,
    otp_regex: str = r"(\d{4,8})",
    delete_after_read: bool = False,
) -> Optional[str]:
    """
    Fetch OTP from Redis for a specific mobile number using the key pattern:
    APP-AUTH-2-USER-LUNA-OTP-mobile-{mobile}
    """
    key = f"APP-AUTH-2-USER-LUNA-OTP-mobile-{mobile}"
    return read_otp_from_redis(
        redis_client=redis_client,
        redis_url=redis_url,
        key=key,
        timeout=timeout,
        poll_interval=poll_interval,
        otp_regex=otp_regex,
        delete_after_read=delete_after_read,
    )


