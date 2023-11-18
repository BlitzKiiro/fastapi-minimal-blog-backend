from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os

from db.database import engine, Base
from routes import blog, user

Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(prefix="/api/user", router=user.UserRouter, tags=['user'])

app.include_router(prefix="/api/blog", router=blog.BlogRouter, tags=['blog'])

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=os.getenv("PORT"))
