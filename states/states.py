from aiogram.fsm.state import State, StatesGroup


class FSMPagination(StatesGroup):
    page = State()

class HisStage(StatesGroup):
    book = State()


class LampsPag(StatesGroup):
    page = State()