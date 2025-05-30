import asyncio

import aiosqlite


class DataService:
    def __init__(self):
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        self.db = await aiosqlite.connect("database/user.sqlite")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.close()

    async def check_user(self, user_id: int):
        async with self.lock:
            async with self.db.execute(
                "SELECT user_id from users WHERE user_id = ?", (user_id,)
            ) as cursor:
                user_id = await cursor.fetchone()
                return user_id

    async def add_user(self, user_id: int):
        async with self.lock:
            await self.db.execute(
                "INSERT INTO users (user_id,blocked) VALUES (?,?)", (user_id, False)
            )
            await self.db.commit()

    async def block_user(self, user_id: int, blocked: bool):
        async with self.lock:
            await self.db.execute(
                "UPDATE users SET blocked = ? WHERE user_id = ?", (blocked, user_id)
            )
            await self.db.commit()

    async def check_block(self, user_id: int):
        async with self.lock:
            async with self.db.execute(
                "SELECT blocked FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                blocked_status = await cursor.fetchone()
                return bool(blocked_status[0])

    async def get_blocked_list(self):
        async with self.db.execute("SELECT * FROM users WHERE blocked = 1") as cursor:
            blocked_list = await cursor.fetchall()
            print(blocked_list)
            return blocked_list


if __name__ == "__main__":
    pass
