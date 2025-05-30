from aiogram import Router, Bot
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.configuration.config_service import ConfigService
from bot.router.keyboards import answer_user
from bot.state.chat_states import ChatState

router = Router()


@router.message(ChatState.wait_content_message)
async def wait_msg(message: Message, bot: Bot, state: FSMContext):
    admin_id = ConfigService("config").get_section_value("admin_id")
    await bot.send_message(
        chat_id=admin_id,
        text=f"Вы получили сообщение от пользователя {message.from_user.username}:",
        reply_markup=await answer_user(message.from_user.id),
    )
    await bot.forward_message(
        chat_id=ConfigService("config").get_section_value("admin_id"),
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )
    await message.answer(
        text=ConfigService("messages").get_section_value("successful_send")
    )
    await state.clear()


@router.message(ChatState.admin_answer)
async def admin_answer(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(
        chat_id=data["user_id"],
        text=f"Вам ответил администратор\n\n {message.text} \n\nНажмите на кнопку ниже чтобы ответить",
        reply_markup=await answer_user(
            ConfigService("config").get_section_value("admin_id")
        ),
    )
    await message.answer("Вы успешно ответили пользователю.")
    await state.clear()


@router.message(StateFilter(None))
async def unknown_command(message: Message):
    await message.answer(
        text=ConfigService("messages").get_section_value("unknown_command"),
        parse_mode=ParseMode.MARKDOWN,
    )


if __name__ == "__main__":
    pass
