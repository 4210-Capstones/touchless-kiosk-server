import os
import secrets

import configuration


def generate_jwt_key_file_if_not_exist() -> str:
    if not os.path.isfile(configuration.jwt_key_path):
        os.makedirs(os.path.dirname(configuration.jwt_key_path), exist_ok=True)
        with open(configuration.jwt_key_path, 'x') as f:
            jwt_key = secrets.token_hex(20)
            f.write(jwt_key)
            return jwt_key
    else:
        with open(configuration.jwt_key_path, 'r') as f:
            return f.read()
