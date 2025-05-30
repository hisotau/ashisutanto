from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

from bot.configuration.config_service import ConfigService
from bot.router.keyboards import start_button
from database.service.data_service import DataService

router = Router()
config = ConfigService("config")
config_message = ConfigService("messages")


@router.message(CommandStart())
async def start_cmd(message: Message):
    user_id = message.from_user.id
    async with DataService() as db:
        if await db.check_user(user_id=user_id) is None:
            await db.add_user(user_id=user_id)
    await message.answer(
        text=config_message.get_section_value("start_message"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=start_button(),
    )


@router.message(Command("unblock"))
async def unblock_user(message: Message, command: CommandObject):
    if not await check_admin(message):
        return
    block_user_id = command.args
    async with DataService() as db:
        if await db.check_user(block_user_id):
            await db.block_user(block_user_id, False)
    await message.answer("Пользователь разблокирован.")


@router.message(Command("block"))
async def block_user(message: Message, command: CommandObject):
    if not await check_admin(message):
        return
    block_user_id = command.args
    async with DataService() as db:
        if await db.check_user(block_user_id):
            await db.block_user(block_user_id, True)
    await message.answer("Пользователь заблокирован.")


@router.message(Command("blocklist"))
async def blocklist_cmd(message: Message):
    if not await check_admin(message):
        return

    content = ""
    async with DataService() as db:
        for user in await db.get_blocked_list():
            content += f"Пользователь: {user[0]} \n"

    await message.answer(f"Список заблокированных пользователей:\n\n{content}")


async def check_admin(message: Message):
    if message.from_user.id != config.get_section_value("admin_id"):
        await message.answer(text=config_message.get_section_value("not_enough_rights"))
        return False
    return True


if __name__ == "__main__":
    pass
