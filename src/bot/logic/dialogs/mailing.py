"""Mailing dialog file"""
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Back, Row, Button, Select, Column, Next, Start
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi, Progress
from magic_filter import F

from src.bot.logic.handlers.mailing import choose_message, start_mailing_handler, stop_mailing_handler
from src.bot.logic.handlers.receivers import input_receivers_file, confirm_receivers_file, cancel_receivers, \
    input_receivers_chat, input_receivers_geo
from src.bot.structures.getters import get_messages_data, get_message_data_by_id, get_final_info, get_receivers_list, \
    get_progress_value
from src.bot.structures.states import MailingStatesGroup
from src.bot.structures.text import ButtonText as btn_txt
from src.bot.structures.text import CaptureText as cpt_txt


choose_message_win = Window(
    Const(cpt_txt.MAILING_CHOOSE_MESSAGE),
    Column(
        Select(
            Format('{item.title}'),
            id='mail_mes_choose',
            items=F['messages'],
            item_id_getter=lambda m: m.id,
            on_click=choose_message,
        ),
    ),
    Cancel(Const(btn_txt.BACK)),
    state=MailingStatesGroup.mes_choose_lst,
    getter=get_messages_data,
)

confirm_message_win = Window(
    DynamicMedia(selector='media'),
    Format('<b>{message.title}</b>\n\n{message.text}'),
    Row(
        Next(Const(btn_txt.CONFIRM)),
        Back(Const(btn_txt.BACK)),
    ),
    getter=get_message_data_by_id,
    state=MailingStatesGroup.mes_choose_confirm,
)

receivers_menu_win = Window(
    Const(cpt_txt.RECEIVERS_MENU),
    Row(
        SwitchTo(
            Const(btn_txt.RECEIVERS_FILE),
            id='file',
            state=MailingStatesGroup.rec_from_file,
        ),
        SwitchTo(
            Const(btn_txt.RECEIVERS_CHAT),
            id='chat',
            state=MailingStatesGroup.rec_from_chat,
        ),
    ),
    SwitchTo(
        Const(btn_txt.RECEIVERS_GEO),
        id='geo',
        state=MailingStatesGroup.rec_from_geo,
    ),
    Cancel(Const(btn_txt.BACK)),
    state=MailingStatesGroup.rec_menu,
)

receivers_from_file_win = Window(
    Const(cpt_txt.RECEIVERS_FILE_INPUT),
    MessageInput(
        content_types=[ContentType.DOCUMENT],
        func=input_receivers_file,
    ),
    Back(Const(btn_txt.BACK)),
    state=MailingStatesGroup.rec_from_file,
)

receivers_confirm_from_file_win = Window(
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
            on_click=cancel_receivers,
        ),
    ),
    state=MailingStatesGroup.rec_confirm_from_file,
    getter=get_receivers_list,
)


receivers_from_chat_win = Window(
    Const(cpt_txt.RECEIVERS_CHAT_INPUT),
    MessageInput(
        content_types=[ContentType.TEXT],
        func=input_receivers_chat,
    ),
    SwitchTo(
        Const(btn_txt.BACK),
        id='back_rec_menu_chat',
        state=MailingStatesGroup.rec_menu,
    ),
    state=MailingStatesGroup.rec_from_chat,
)


receivers_from_geo_win = Window(
    Const(cpt_txt.RECEIVERS_GEO_INPUT),
    MessageInput(
        content_types=[ContentType.LOCATION],
        func=input_receivers_geo,
    ),
    SwitchTo(
        Const(btn_txt.BACK),
        id='back_rec_menu_geo',
        state=MailingStatesGroup.rec_menu,
    ),
    state=MailingStatesGroup.rec_from_geo,
)


mailing_info_win = Window(
    Format(cpt_txt.FINAL_INFO),
    Row(
        Button(
            Const(btn_txt.START),
            id='start_mailing',
            on_click=start_mailing_handler,
        ),
        Back(Const(btn_txt.BACK)),
    ),
    Cancel(Const(btn_txt.BACK_MENU)),
    getter=get_final_info,
    state=MailingStatesGroup.final_info,
)

progress_win = Window(
    Multi(
        Const(cpt_txt.MAILING_RUNNING),
        Progress('progress', 10, filled='🟪')
    ),
    Cancel(Const(btn_txt.STOP), on_click=stop_mailing_handler),
    state=MailingStatesGroup.mailing,
    getter=get_progress_value,
)


dialog = Dialog(
    choose_message_win,
    confirm_message_win,
    receivers_menu_win,
    receivers_from_file_win,
    receivers_confirm_from_file_win,
    receivers_from_chat_win,
    receivers_from_geo_win,
    mailing_info_win,
    progress_win,
)
