from passlib.context import CryptContext


pwd_cxt = CryptContext(schemes='bcrypt', deprecated='auto')

class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
    
    def verify(hashed_password, plain_passwords):
        return pwd_cxt.verify(plain_passwords, hashed_password)