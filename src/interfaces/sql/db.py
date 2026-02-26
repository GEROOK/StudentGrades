import asyncpg
from typing import Optional
from builtins import str

CREATE_TABLE_SCRIPTS = """
CREATE TABLE IF NOT EXISTS grades (
    id          BIGSERIAL PRIMARY KEY,
    grade_date  DATE NOT NULL,
    group_number   TEXT NOT NULL,
    student_full_name   TEXT NOT NULL,
    points       SMALLINT NOT NULL CHECK (points BETWEEN 2 AND 5)
);

"""

CREATE_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_grades_student_full_name
    ON grades (student_full_name);
CREATE INDEX IF NOT EXISTS idx_grades_points
    ON grades (points);
"""


class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def get_connection(self) -> asyncpg.Connection:
        if not self.pool:
            raise Exception("database pool is not initialized.")
        return await self.pool.acquire()

    async def release_connection(self, conn: asyncpg.Connection) -> None:
        if not self.pool:
            raise Exception("database pool is not initialized.")
        return await self.pool.release(conn)

    async def create_tables(self):
        async with self.pool.acquire() as conn:
            try:
                await conn.execute(CREATE_TABLE_SCRIPTS)
                await conn.execute(CREATE_INDEXES)
            except asyncpg.DuplicateTableError:
                pass


