"""Mailing dialog file"""
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Back, Row, Button, Select, Column
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F

from src.bot.logic.handlers.messages import (
    confirm_create_message, create_message,
    input_message_text, message_details,
    delete_message,
)
from src.bot.structures.getters import get_message_data, get_titles_list, get_message_data_by_id
from src.bot.structures.states import MessagesStatesGroup
from src.bot.structures.text import ButtonText as btn_txt
from src.bot.structures.text import CapturesText as cpt_txt


