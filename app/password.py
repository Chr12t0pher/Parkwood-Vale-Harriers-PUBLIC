import base64
import hashlib
import os


def hash_password(password):
    """Returns the hashed password and a randomly generated salt.
    :param password: Password inputted by the user.
    :returns: Salt used to hash the password.
    :returns: Hashed password."""
    password = password.encode("utf-8")  # Encode the input correctly.
    salt = base64.b64encode(os.urandom(32))  # Create a random salt.
    hashed_password = hashlib.sha256(salt + password).hexdigest()  # Hash the password.
    return hashed_password, salt


def check_password(password, salt, hashed_password):
    """Hashes the password the user provides and checks it against the stored hash.
    :param password: Password user provides.
    :param salt: Salt stored in users file.
    :param hashed_password: Hashed password stored in users file.
    :returns: True if password provided is correct, else False."""
    password = password.encode("utf-8")  # Encode the input correctly.
    return hashlib.sha256(salt + password).hexdigest() == hashed_password