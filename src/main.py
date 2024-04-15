from fastapi import FastAPI
from fastapi.responses import JSONResponse
from config.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware
from auth.controller.route import router as auth_router
from users.controller.routes import router as guest_router, user_router

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)


# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())


@app.get('/')
def health_check():
    return JSONResponse(content={"message": "Ok"})
