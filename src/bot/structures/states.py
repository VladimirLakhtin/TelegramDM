"""States file"""
from aiogram.fsm.state import State, StatesGroup


class MenuStatesGroup(StatesGroup):
    menu = State()
    mailing = State()


class AccountsStatesGroup(StatesGroup):
    lst = State()
    input_phone_number = State()
    input_code = State()
    incorrect_input_code = State()
    delete = State()


class ParamsStatesGroup(StatesGroup):
    menu = State()


class MessagesStatesGroup(StatesGroup):
    lst = State()
    input_title = State()
    input_text = State()
    add_confirm = State()
    details = State()
    delete = State()
    delete_confirm = State()


class ReceiversStatesGroup(StatesGroup):
    menu = State()
    from_file = State()
    confirm_from_file = State()
    from_group = State()
    from_geo = State()

