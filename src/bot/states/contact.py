from aiogram.fsm.state import StatesGroup, State


class ContactState(StatesGroup):
    waiting_contact = State()

class CaseState(StatesGroup):
    waiting = State()
