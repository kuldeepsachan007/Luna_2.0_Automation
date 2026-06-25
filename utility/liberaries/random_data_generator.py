# python
from __future__ import annotations
import random
import string
import secrets
import uuid
from datetime import date, timedelta
from typing import Optional


def random_string(length: int = 8, chars: Optional[str] = None) -> str:
    """Return a cryptographically strong random string of given length."""
    if chars is None:
        chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def random_email(domain: Optional[str] = None, username_len: int = 8) -> str:
    """Generate a random email address. If domain is None a random domain is created."""
    if domain is None:
        domain = f"{random_string(6, string.ascii_lowercase)}.com"
    username = random_string(username_len, string.ascii_lowercase + string.digits)
    return f"{username}@{domain}"


def random_name() -> str:
    """Generate a simple random full name (First Last)."""
    first_names = ("Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Jamie", "Drew", "Avery")
    last_names = ("Smith", "Johnson", "Brown", "Taylor", "Anderson", "Lee", "Clark", "Walker", "Wright", "Hill")
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def random_phone(country: str = "us") -> str:
    """
    Generate a simple phone number string.
    - 'us' returns E.164 like +1XXXXXXXXXX
    - otherwise returns a generic numeric string
    """
    if country.lower() == "us":
        # US: +1 followed by 10 digits, ensure first digit of area code not 0/1
        area = str(random.randint(200, 999))
        exch = str(random.randint(200, 999))
        line = f"{random.randint(0, 9999):04d}"
        return f"+1{area}{exch}{line}"
    # generic fallback: 10 digits with optional + prefix
    return f"+{random.randint(1, 99)}{random.randint(10**9, 10**10 - 1)}"


def random_int(minimum: int = 0, maximum: int = 100) -> int:
    """Return a random integer in [minimum, maximum]."""
    return random.randint(minimum, maximum)


def random_date(start_year: int = 1970, end_year: int = 2000) -> date:
    """Return a random date between Jan 1 start_year and Dec 31 end_year."""
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def random_uuid() -> str:
    """Return a random UUID4 string."""
    return str(uuid.uuid4())


def random_password(length: int = 12, require_special: bool = True) -> str:
    """
    Generate a password that includes at least one lowercase, uppercase, digit,
    and optionally a special character. Length must be >=4 (or >=3 if no special).
    """
    if require_special:
        if length < 4:
            raise ValueError("length must be at least 4 when require_special is True")
        lowers = secrets.choice(string.ascii_lowercase)
        uppers = secrets.choice(string.ascii_uppercase)
        digits = secrets.choice(string.digits)
        special = secrets.choice("!@#$%^&*()-_=+[]{};:,.<>?")
        remaining = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?") for _ in range(length - 4))
        pwd = lowers + uppers + digits + special + remaining
    else:
        if length < 3:
            raise ValueError("length must be at least 3 when require_special is False")
        lowers = secrets.choice(string.ascii_lowercase)
        uppers = secrets.choice(string.ascii_uppercase)
        digits = secrets.choice(string.digits)
        remaining = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length - 3))
        pwd = lowers + uppers + digits + remaining

    # shuffle to avoid predictable ordering
    pwd_list = list(pwd)
    random.shuffle(pwd_list)
    return ''.join(pwd_list)
def random_address() -> str:
    """Generate a simple random street address."""
    street_numbers = range(100, 9999)
    street_names = ("Main", "Oak", "Pine", "Maple", "Cedar", "Elm", "Washington", "Lake", "Hill", "Sunset")
    street_types = ("St", "Ave", "Blvd", "Rd", "Ln", "Dr", "Ct", "Pl")
    cities = ("Springfield", "Rivertown", "Lakeside", "Greenville", "Fairview", "Madison", "Georgetown", "Clinton")
    states = ("CA", "NY", "TX", "FL", "IL", "PA", "OH", "MI", "GA", "NC")
    zip_code = f"{random.randint(10000, 99999)}"
    address = f"{random.choice(street_numbers)} {random.choice(street_names)} {random.choice(street_types)}, {random.choice(cities)}, {random.choice(states)} {zip_code}"
    return address

def generate_random_indian_number():
    # Indian mobile numbers usually start with 6, 7, 8, or 9
    first_digit = str(random.choice([6, 7, 8, 9]))
    
    # Generate the remaining 9 digits
    remaining_digits = ''.join(random.choices('0123456789', k=9))
    
    # Combine to form a 10-digit number
    mobile_number = first_digit + remaining_digits
    return mobile_number

 
def generate_random_email():

    # Random username part

    name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 8)))

    number = str(random.randint(10, 999))

    # Common email domains

    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com"]

    domain = random.choice(domains)

    # Construct email

    email = f"{name}{number}@{domain}"

    return email
 

 
