from fastapi import FastAPI
from fastapi.responses import JSONResponse

from starlette.middleware.authentication import AuthenticationMiddleware

from src.auth.controller.route import router as auth_router
from src.users.controller.routes import router as guest_router, user_router
from src.config.security import JWTAuth

import uvicorn

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)

# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())


@app.get('/')
def health_check():
    return JSONResponse(content={"message": "Ok"})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
