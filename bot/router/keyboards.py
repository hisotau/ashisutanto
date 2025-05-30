from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.configuration.config_service import ConfigService
from database.service.data_service import DataService


def start_button():
    inline_keyboard = [
        [InlineKeyboardButton(text="Написать админу", callback_data="send_admin_msg")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def answer_user(user_id: int):
    inline_keyboard = [
        [InlineKeyboardButton(text="Ответить", callback_data=f"answer_user_{user_id}")]
    ]
    if user_id != ConfigService("config").get_section_value("admin_id"):
        async with DataService() as db:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=(
                            "Разблокировать"
                            if await db.check_block(user_id=user_id)
                            else "Заблокировать"
                        ),
                        callback_data=f"block_user_{user_id}",
                    )
                ]
            )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


if __name__ == "__main__":
    pass
