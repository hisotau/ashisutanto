from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.configuration.config_service import ConfigService
from bot.router.keyboards import answer_user
from bot.state.chat_states import ChatState
from database.service.data_service import DataService

router = Router()


@router.callback_query(F.data.contains("send_admin_msg"))
async def send_msg(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=ConfigService("messages").get_section_value("send_message_to_admin"),
        reply_markup=None,
    )
    await state.set_state(ChatState().wait_content_message)
    await callback.answer()


@router.callback_query(F.data.startswith("answer_user_"))
async def answer_msg(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split("answer_user_")[1]
    await callback.message.answer("Введите что вы хотите ответить")
    await state.set_state(
        ChatState.admin_answer
        if callback.from_user.id
        == ConfigService("config").get_section_value("admin_id")
        else ChatState.wait_content_message
    )
    await state.update_data(user_id=user_id)
    await callback.answer()


@router.callback_query(F.data.startswith("block_user_"))
async def block_user(callback: CallbackQuery):
    user_id = callback.data.split("block_user_")[1]
    async with DataService() as db:
        await db.block_user(
            user_id=user_id, blocked=False if await db.check_block(user_id) else True
        )
        content = "заблокировали" if await db.check_block(user_id) else "разблокировали"
    await callback.message.edit_reply_markup(
        inline_message_id=callback.inline_message_id,
        reply_markup=await answer_user(user_id=int(user_id)),
    )
    await callback.message.answer(text=f"Вы {content} пользователя: {user_id}")
    await callback.answer()


if __name__ == "__main__":
    pass
