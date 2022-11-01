import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
from api.routes import routers

origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# call routes (API endpoints)
app.include_router(routers.route)

# connect to database
load_dotenv()
db_connection = os.getenv("ATLAS_URI")
db_name = os.getenv("DB_NAME")

# open connection to database server
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(db_connection)
    app.database = app.mongodb_client[db_name]
    print("Connected to the MongoDB database!")

# # close connection to database server
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)