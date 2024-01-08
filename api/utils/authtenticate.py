from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from ..models.user import User
from ..database import db
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/user/login",
    description="username must be email and password must be 8-16 characters"
)

userCollection = db.get_collection("users")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = User.verify_token(token)
        user = await userCollection.find_one({"_id": ObjectId(payload["id"])})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid user")
        return User(**user)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
