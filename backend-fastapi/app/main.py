from fastapi import FastAPI

from app.modules.accounts.router import router as accounts_router

app = FastAPI(title="My Project")

app.include_router(accounts_router)
