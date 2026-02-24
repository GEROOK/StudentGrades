from fastapi import Depends, FastAPI, Request
from typing import TYPE_CHECKING, Annotated
from asyncpg import Connection

if TYPE_CHECKING:
    from src.interfaces.sql.db import Database

def _get_db_from_app(app: FastAPI) -> "Database":
    return app.extra["db"] 

async def get_connection(request: Request) -> Connection:
    app = request.app
    db_instance = _get_db_from_app(app)
    connection = await db_instance.get_connection() 
    try:
        yield connection
    finally:
        await db_instance.release_connection(connection)

ConnectionDep = Annotated[Connection, Depends(get_connection)]


