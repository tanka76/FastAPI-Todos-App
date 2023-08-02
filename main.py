from fastapi import FastAPI
import uvicorn
from routes.users import router as user_router

app = FastAPI()


#includes all routers
app.include_router(user_router)





if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080,reload=True)

