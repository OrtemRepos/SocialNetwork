import uvicorn
import web
from fastapi import FastAPI

app = FastAPI()

app.include_router(web.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
