"""Main dialog file"""
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Row, Start, Button
from aiogram_dialog.widgets.text import Const

from src.bot.logic.handlers.mailing import init_mailing_handler
from src.bot.structures.states import MenuStatesGroup, AccountsStatesGroup, \
    MessagesStatesGroup
from src.bot.structures.text import ButtonText as btn_txt
from src.bot.structures.text import CapturesText as cpt_txt


dialog = Dialog(
    Window(
        Const(cpt_txt.MAIN_MENU),
        Row(
            Start(
                Const(btn_txt.ACCOUNTS),
                id="accounts",
                state=AccountsStatesGroup.lst,
            ),
            Start(
                Const(btn_txt.MESSAGES),
                id="messages",
                state=MessagesStatesGroup.lst
            ),
        ),
        Button(
            Const(btn_txt.START),
            id="mailing",
            on_click=init_mailing_handler,
        ),
        state=MenuStatesGroup.menu,
    )
)
