from fastapi import FastAPI
from .routers import contacts
from app.database import engine
from .models import Base

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
