from fastapi import APIRouter
from api.routes.user import router as user_router

router = APIRouter(prefix="/api")
router.include_router(router=user_router, tags=["user"])
