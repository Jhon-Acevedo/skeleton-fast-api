# FastAPI Auth

## Instalation

- Create a virtual environment using `python -m venv venv`
- Activate the virtual environment using `source venv/bin/activate` on linux or `venv\Scripts\activate` on windows
- Install the dependencies using `pip install -r requirements.txt`
- Create a `.env` file in the root directory and add the below content: Use `.env-example` as a reference
- Run the app using `uvicorn src.main:app --reload`

## Info

This project contains the code for creating the below four apis

| API Endpoint          | Method | Description                   |
|-----------------------|--------|-------------------------------|
| `/users`              | POST   | Create new user account       | 
| `/auth/login`         | POST   | Create JWT Token              |
| `/auth/refresh-token` | POST   | Refresh JWT Token             | 
| `/users/me`           | POST   | Get Authenticated User Detail |
| `/users/{user_id}`    | GET    | Get user by id                | 

### Additional

- You will learn how to configure mysql in FastAPI
- You will learn how to add connection pooling in SQLAlchemy
- You will learn how to configure and get authenticated user form Request
