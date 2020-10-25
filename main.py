from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import yaml

from db import models
from db.db import engine
from api.api import api_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SwiftServe", docs_url='/')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.openapi_schema = yaml.load(open('swagger.yaml').read())
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
