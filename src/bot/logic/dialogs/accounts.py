"""Accounts dialog file"""
from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Column, Select, Row, SwitchTo, ListGroup, Checkbox, Radio, Next, \
    Back
from aiogram_dialog.widgets.text import Const, Format

from src.bot.logic.handlers.accounts import input_phone_number_handler, input_phone_code_handler, \
    account_delete_handler, turn_account_handler, account_confirm_delete_handler
from src.bot.structures.bool_format import BoolFormat
from src.bot.structures.funcs import open_account_option
from src.bot.structures.getters import get_accounts_data, get_account_phone_number
from src.bot.structures.states import AccountsStatesGroup
from src.bot.structures.text import ButtonText as btn_txt, CaptureText as cpt_txt


lst_win = Window(
    Const(cpt_txt.ACCOUNTS_MENU),
    ListGroup(
        Checkbox(
            Format("✓ {item.phone_number}"),
            Format("  {item.phone_number}"),
            id="acc_check",
        ),
        Row(
            Button(
                BoolFormat(
                    "{item.is_ready}",
                    on_text=btn_txt.TURNED_ON,
                    off_text=btn_txt.TURNED_OFF,
                ),
                id="acc_ready",
                on_click=turn_account_handler,
            ),
            Button(
                Const(btn_txt.DELETE),
                id='acc_delete',
                on_click=account_confirm_delete_handler,
            ),
            when=open_account_option,
        ),
        id="lg",
        item_id_getter=lambda acc: acc.id,
        items=F["accounts"],
    ),
    Row(
        Next(Const(btn_txt.ACCOUNTS_NEW)),
        Cancel(Const(btn_txt.BACK)),
    ),
    state=AccountsStatesGroup.lst,
    getter=get_accounts_data,
)

input_phone_number_win = Window(
    Const(cpt_txt.ACCOUNTS_PHONE_INPUT),
    MessageInput(
        content_types=[ContentType.TEXT],
        func=input_phone_number_handler,
    ),
    Back(Const(btn_txt.BACK)),
    state=AccountsStatesGroup.input_phone_number,
)

input_code_win = Window(
    Const(cpt_txt.ACCOUNTS_CODE_INPUT),
    MessageInput(
        content_types=[ContentType.TEXT],
        func=input_phone_code_handler,
    ),
    Back(Const(btn_txt.BACK)),
    state=AccountsStatesGroup.input_code,
)

confirm_delete_win = Window(
    Format(cpt_txt.ACCOUNTS_CONFIRM_DELETE),
    Row(
        Button(
            Const(btn_txt.CONFIRM),
            id='acc_confirm_delete',
            on_click=account_delete_handler,
        ),
        SwitchTo(
            Const(btn_txt.REJECT),
            id='reject_delete',
            state=AccountsStatesGroup.lst,
        ),
    ),
    getter=get_account_phone_number,
    state=AccountsStatesGroup.delete,
)


dialog = Dialog(
    lst_win,
    input_phone_number_win,
    input_code_win,
    confirm_delete_win,
)
