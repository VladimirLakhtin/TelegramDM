"""Main dialog file"""
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Next, Start
from aiogram_dialog.widgets.text import Const

from src.bot.structures.states import MenuStatesGroup, AccountsStatesGroup, ParamsStatesGroup
from src.bot.structures.text import ButtonText as btn_txt
from src.bot.structures.text import CapturesText as cpt_txt


dialog = Dialog(
    Window(
        Const(cpt_txt.MAIN_MENU),
        Row(
            Start(Const(btn_txt.ACCOUNTS), id="accounts", state=AccountsStatesGroup.lst),
            Start(Const(btn_txt.PARAMS), id="params", state=ParamsStatesGroup.menu),
        ),
        Next(Const(btn_txt.START), id="mailing"),
        state=MenuStatesGroup.menu,
    )
)
