from pydantic import (
    BaseModel,
    BeforeValidator, 
    EmailStr, 
    Field, 
    validator, 
    SecretStr,
    ConfigDict)
from typing import Annotated, Optional
from datetime import datetime, timedelta
from bcrypt import hashpw, gensalt, checkpw
from bson import ObjectId
from jwt import encode, decode
import api.settings as settings

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserLogin (BaseModel):
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=16)

class UserRegister (BaseModel):
    name: str
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=16)
    re_password: SecretStr = Field(min_length=8, max_length=16)

    @validator('re_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Password not match')
        return v



class User (BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr
    password: SecretStr
    name: str
    is_active: bool = True
    is_comfirmed: bool = False
    is_superuser: bool = False
    is_staff: bool = False
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ ObjectId: str },
    )
    
    def hash_password(self):
        self.password = hashpw(self.password.get_secret_value().encode(), gensalt()).decode()

    def check_password(self, password):
        return checkpw(password.encode(), self.password.get_secret_value().encode())

    def get_token(self):
        payload = {
            "id": str(self.id),
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_TIME_EXPIRE),
            "iat": datetime.utcnow()
        }
        return encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    
    @staticmethod
    def verify_token(token):
        payload = decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
        