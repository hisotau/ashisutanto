from aiogram.fsm.state import State, StatesGroup


class ChatState(StatesGroup):
    wait_content_message = State()
    admin_answer = State()


if __name__ == "__main__":
    pass
