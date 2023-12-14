"""States file"""
from aiogram.fsm.state import State, StatesGroup


class MenuStatesGroup(StatesGroup):
    menu = State()


class MailingStatesGroup(StatesGroup):

    # Choose message
    mes_choose_lst = State()
    mes_choose_confirm = State()

    # Choose receivers
    rec_menu = State()
    rec_from_file = State()
    rec_confirm_from_file = State()
    rec_from_chat = State()
    rec_from_geo = State()

    # Main
    final_info = State()
    mailing = State()


class AccountsStatesGroup(StatesGroup):
    lst = State()
    input_phone_number = State()
    input_code = State()
    incorrect_input_code = State()
    delete = State()


class MessagesStatesGroup(StatesGroup):
    lst = State()
    input_title = State()
    input_text = State()
    input_media = State()
    add = State()
    details = State()
    delete = State()

