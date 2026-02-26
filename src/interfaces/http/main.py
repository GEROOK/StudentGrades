from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from src.interfaces.http.routes import router
from src.interfaces.sql.db import Database
import os


    
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/studentgrades"
    )
    db_instance = Database(dsn=database_url)
    
    await db_instance.connect()
    await db_instance.create_tables()
    app.extra["db"] = db_instance
    yield

    await db_instance.disconnect()

    
    

     

def get_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app

app = get_app()

print("Startup OK")