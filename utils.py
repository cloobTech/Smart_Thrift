# Description: Utility functions

import bcrypt
from uuid import uuid4

def hash_password(password: str) -> bytes:
    """ hash password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def generate_uuid() -> str:
    """Generate a new uuid string"""
    return str(uuid4())