from fastapi import HTTPException, Depends
from app.config import settings
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

def verify_token(credentials=Depends(security)):
    sec_key = settings.SECRET_KEY
    enc_algo = settings.ALGORITHM
    token = credentials.credentials
    
    # print(f"Secret Key: {sec_key}, Algorithm: {enc_algo}, Token: {token}")
    
    try:
        return jwt.decode(token, sec_key, [enc_algo])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token Expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid Token')
    

if __name__ == "__main__":
    from fastapi.security import HTTPAuthorizationCredentials
    
    tkn = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTb21lLXRlc3QtdXNlci0xMjM0NSIsInJvbGUiOiJBZG1pbl9UZXN0IiwiZXhwIjo4ODE1ODAyMjI4N30.EKD2bGCZ4KzaVrxjtf2wWE9XYIzbS_V-VKGPQIHsuyY"
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=tkn)
    x = verify_token(credentials=creds)
    print(x)