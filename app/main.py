import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import database, metadata
from app.controllers.auth import auth_router
from app.controllers.users import user_router
from app.controllers.chats import chat_router

# from app1.database import database, metadata
# from app1.users.router import auth_router, user_router
# from app1.chats.router import chat_router

# from load_local_milvus import load_pickled_dump

version = "0.1.0"

app = FastAPI(
    title="Project ChatDPT",
    description="POC Project for ChatGPT Bot for Data Privacy Concerns",
    version=version,
    contact={
        "name": "Project ChatDPT",
        "url": "https://gitlab.mynt.xyz/data-analytics/project-abogadobot/issues"
    },
)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(chat_router, prefix="/chats", tags=["chats"])

@app.get("/version")
def get_version():
    return version

if __name__ == "__main__":
    

    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.on_event("startup")
async def startup():
    await database.connect()
    # await load_pickled_dump()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()