from aiogram.fsm.state import StatesGroup, State


class AddUserNameState(StatesGroup):
    waiting_username = State()

class DelUserNameState(StatesGroup):
    waiting_username = State()

class CreateNewsLetterState(StatesGroup):
    get_text = State()
    get_photo = State()
    get_kb_text = State()
    get_kb_url = State()
    confirm_state = State()

