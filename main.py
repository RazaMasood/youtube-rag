import uvicorn
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from api import (
    rag_api,
    transcript_api
)

app = FastAPI(title="YouTube Chatbot", version="1.0.0")

# Handle CORS protection
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type"],
)


app.include_router(transcript_api.router)
app.include_router(rag_api.router)


@app.get("/")
def get():
    return {"msg": "Welcome to YouTube Chatbot API"}

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="localhost", port=8010, reload=True, workers=4)
    except KeyboardInterrupt:
        print("Server stopped by user.")