from fastapi import FastAPI
from db import models
from db.database import engine
from routers import meetings, tasks, user
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(user.router)
app.include_router(tasks.router)
app.include_router(meetings.router)

@app.get("/")
def root():
    return "Hello world"

models.Base.metadata.create_all(engine)

origins = ["http://localhost:4800", "http://localhost:4200" ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
