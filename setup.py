import secrets

def create_random_secret_key():
    return secrets.token_hex(16)


if __name__ in "__main__":
    print(create_random_secret_key())