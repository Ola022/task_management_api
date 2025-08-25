from fastapi import FastAPI
from db import models
from db.database import engine
from routers import meetings, metrics, tasks, user, project
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(metrics.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(tasks.router)
app.include_router(meetings.router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return "Hello world"

models.Base.metadata.create_all(engine)

origins = ["https://taskmanagementwebapps.netlify.app", "http://localhost:4200" ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Railway assigns PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
