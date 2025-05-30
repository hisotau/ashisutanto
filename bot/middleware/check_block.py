from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.configuration.config_service import ConfigService
from database.service.data_service import DataService


class CheckBlock(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_id = data["event_context"].user_id
        if user_id == ConfigService("config").get_section_value("admin_id"):
            return await handler(event, data)

        async with DataService() as db:
            if await db.check_user(user_id=user_id) is None or not await db.check_block(
                user_id=user_id
            ):
                return await handler(event, data)

        await event.bot.send_message(
            chat_id=user_id,
            text=ConfigService("messages").get_section_value("blocked_message"),
        )
        return


if __name__ == "__main__":
    pass
