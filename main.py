import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from src.default_route import default_route


load_dotenv()

app = FastAPI()

app.include_router(
    default_route, tags = ["Dummy Login Page"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8002, reload=True)