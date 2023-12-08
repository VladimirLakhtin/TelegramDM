class CapturesText:
    MAIN_MENU = """Главное меню"""
    PARAMS_MENU = """Меню параметров"""
    ACCOUNTS_MENU = """Меню аккаунтов"""

    # Mailing
    MAILING_NO_ACCOUNTS = """Ни один аккаунт не включен"""
    MAILING_CHOOSE_MESSAGE = """Выберите сообщение для рассылки:"""
    FINAL_INFO = """<b>Время расылки составит {time}</b>\n\n<b>В рассылке участвуют аккаунты:</b>\n\n{accounts}"""

    # Accounts
    ACCOUNTS_PHONE_INPUT = """Введите номер телефона в формате <b>+7**********</b>:"""
    ACCOUNTS_CODE_INPUT = """Введите проверочный код:"""
    ACCOUNTS_PHONE_INCORRECT_INPUT = """Данный номер имеет неверный формат. Попробуйте снова"""
    ACCOUNTS_PHONE_INPUT_FLOOD = """Произведено слишком много попыток аутентификации на данный номер\n
Попробуйте другой номер или повторите попытку через {} сек"""
    ACCOUNTS_CODE_INCORRECT_INPUT = """Введенный код был неверным. Попробуйте снова"""
    ACCOUNTS_CODE_EXPIRED_INPUT = """Введенный код устарел, либо вы пытаетесь добавить аккаунт, который используете в данный момент\n
Попробуйте снова"""
    ACCOUNTS_CONFIRM_DELETE = """Вы точно хотите удалить аккаунт в номером {phone_number}?"""

    # Messages
    MESSAGES_MENU = """Меню сообщений"""
    MESSAGES_LIST = """Список сообщений"""
    MESSAGE_TITLE_INPUT = """Введите заголовок сообщения:"""
    MESSAGE_TEXT_INPUT = """Введите новое сообщение:"""
    MESSAGE_INCORRECT_INPUT = """Сообщение должно быть исключительно текстовым"""
    MESSAGE_ADD_CONFIRM = """Уверены, что хотите добавить такое сообщение?\n\n<b>{title}</b>\n\n{message}"""
    MESSAGE_DELETE_CONFIRM = """Уверены, что хотите удалить сообщение "{title}"?"""

    # Receivers
    RECEIVERS_MENU = """Выберите способ получение адресатов"""
    RECEIVERS_FILE_INPUT = """Отправьте файл с расширением <b>.txt</b>\nФайл должен содержать номера телефонов и/или username-ы"""
    RECEIVERS_FILE_CONFIRM = """<b>Проверьте содержимое файла:</b>\n\n{receivers}\n..."""
