import secrets
import string


def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    generated_password = ''.join(secrets.choice(chars) for i in range(length))

    return generated_password