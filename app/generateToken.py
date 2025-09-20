import jwt
import datetime
from config import settings

def generate_token(argument: str="Some-test-user-12345"):
    sec_key = settings.SECRET_KEY
    enc_algo = settings.ALGORITHM

    expiration = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=999999)
    payload = {
        "sub": argument,
        "role": "Admin_Test",
        "exp": expiration
    }

    token = jwt.encode(payload, sec_key, enc_algo)
    return token


if __name__ == "__main__":
    print(generate_token())
