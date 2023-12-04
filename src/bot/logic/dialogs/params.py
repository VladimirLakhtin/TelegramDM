"""Params dialog file"""
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Cancel, Start, Row
from aiogram_dialog.widgets.text import Const

from src.bot.structures.states import MessagesStatesGroup, ReceiversStatesGroup, ParamsStatesGroup
from src.bot.structures.text import ButtonText as btn_txt
from src.bot.structures.text import CapturesText as cpt_txt


dialog = Dialog(
    Window(
        Const(cpt_txt.PARAMS_MENU),
        Row(
            Start(Const(btn_txt.MESSAGES), id="messages", state=MessagesStatesGroup.lst),
            Start(Const(btn_txt.RECEIVERS), id="receivers", state=ReceiversStatesGroup.menu),
        ),
        Cancel(Const(btn_txt.BACK)),
        state=ParamsStatesGroup.menu,
    )
)
