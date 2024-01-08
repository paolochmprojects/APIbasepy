from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from logging import getLogger

from ..database import db
from ..models.user import User, UserRegister, UserLogin
from ..utils.authtenticate import get_current_user


logger = getLogger("uvicorn")

router = APIRouter(prefix="/user")


userCollection = db.get_collection("users")


@router.post(path="/register",
             name="Register user",
             response_description="User created",
             response_class=JSONResponse,
             summary="Create user",
             status_code=201
             )
async def register(user: UserRegister):
    user_in_db = await db.users.find_one({"email": user.email})

    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_to_register = User(**user.model_dump())
    user_to_register.hash_password()

    user_to_db = await userCollection.insert_one(user_to_register.model_dump(exclude=["id"]))
    user_in_db = await userCollection.find_one({"_id": user_to_db.inserted_id})

    if not user_in_db:
        raise HTTPException(status_code=400, detail="Error creating user")

    return {
        "detail": "User created successfully",
        "userId": str(user_to_db.inserted_id)
    }


@router.post(path="/login",
             name="Login user",
             status_code=200,
             summary="Login user",
             response_description="User logged",
             response_class=JSONResponse,
             )
async def login(user_data: OAuth2PasswordRequestForm = Depends()):
    try:
        UserLogin(email=user_data.username, password=user_data.password)
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user_in_db = await userCollection.find_one({"email": user_data.username})

    if not user_in_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    user = User(**user_in_db)
    
    if not user.check_password(user_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    user_token = user.get_token()

    return {"access_token": user_token, "token_type": "bearer"}

@router.get(path="/",
            name="Get user",
            status_code=200,
            summary="Get user",
            response_description="User",
            response_class=JSONResponse,
            response_model=User,
            response_model_by_alias=False,
            response_model_exclude=("password")
            )
async def get_user(user: User = Depends(get_current_user)):
    return user