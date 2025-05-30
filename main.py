import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.utils.token import TokenValidationError

from bot.configuration.config_service import ConfigService
from bot.middleware.check_block import CheckBlock
from bot.router import commands, messages, callbacks

logging.basicConfig(level=logging.INFO)
config = ConfigService("config")


def dispatcher_configuration():
    dp = Dispatcher()
    dp.include_routers(commands.router, callbacks.router, messages.router)
    dp.callback_query.outer_middleware(CheckBlock())
    dp.message.outer_middleware(CheckBlock())
    asyncio.run(bot_start(dp))


async def bot_start(dp: Dispatcher):
    try:
        bot = Bot(token=config.get_section_value("bot_token"))
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        await bot_stop(dp)
    except TokenValidationError:
        logging.error("Вы ввели некорректный токен\n")
        config.set_section_value("bot_token", None)


async def bot_stop(dp: Dispatcher):
    await dp.stop_polling()


if __name__ == "__main__":
    dispatcher_configuration()
