from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Format


class BoolFormat(Format):
    """ Changes the text depending on the item boolean parameter """
    def __init__(self, text: str, on_text: str,
                 off_text: str, when: WhenCondition = None):
        super().__init__(text=text, when=when)
        self.text = text
        self.on_text = on_text
        self.off_text = off_text

    async def _render_text(
            self, data: Dict, manager: DialogManager,
    ) -> str:
        result = await super()._render_text(data, manager)
        if result == 'True':
            return self.on_text
        elif result == 'False':
            return self.off_text
        else:
            return result
