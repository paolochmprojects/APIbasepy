from fastapi import FastAPI
from api.routes.index import router

app = FastAPI(
    title="APPBase for devs",
    summary="Api base for mongodb",
    description="API base developed with FastAPI and MongoDB",
    version="0.0.1",
)


app.include_router(router=router)