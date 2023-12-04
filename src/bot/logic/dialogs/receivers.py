"""Receivers dialog file"""
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, SwitchTo, Row, Back
from aiogram_dialog.widgets.text import Const, Format

from src.bot.logic.handlers.receivers import input_receivers_file, cancel_receivers_file, confirm_receivers_file
from src.bot.structures.getters import get_receivers_list
from src.bot.structures.states import ReceiversStatesGroup
from src.bot.structures.text import ButtonText as btn_txt
from src.bot.structures.text import CapturesText as cpt_txt

menu_win = Window(
    Const(cpt_txt.RECEIVERS_MENU),
    Row(
        SwitchTo(
            Const(btn_txt.RECEIVERS_FILE),
            id='file',
            state=ReceiversStatesGroup.from_file,
        ),
        SwitchTo(
            Const(btn_txt.RECEIVERS_GROUP),
            id='group',
            state=ReceiversStatesGroup.from_group,
        ),
    ),
    SwitchTo(
        Const(btn_txt.RECEIVERS_GEO),
        id='geo',
        state=ReceiversStatesGroup.from_geo,
    ),
    Cancel(Const(btn_txt.BACK)),
    state=ReceiversStatesGroup.menu,
)

from_file_win = Window(
    Const(cpt_txt.RECEIVERS_FILE_INPUT),
    MessageInput(
        content_types=[ContentType.DOCUMENT],
        func=input_receivers_file,
    ),
    Back(Const(btn_txt.BACK)),
    state=ReceiversStatesGroup.from_file,
)

confirm_from_file_win = Window(
    Format(cpt_txt.RECEIVERS_FILE_CONFIRM),
    Row(
        Button(
            Const(btn_txt.NEXT),
            id='rec_file_confirm',
            on_click=confirm_receivers_file,
        ),
        Button(
            Const(btn_txt.BACK),
            id='rec_file_cancel',
            on_click=cancel_receivers_file,
        ),
    ),
    state=ReceiversStatesGroup.confirm_from_file,
    getter=get_receivers_list,
)

dialog = Dialog(
    menu_win,
    from_file_win,
    confirm_from_file_win,
)
