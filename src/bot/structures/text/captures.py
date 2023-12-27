""" Captures text file """


class CaptureText:

    # Menu
    MAIN_MENU = """Главное меню"""

    # Mailing
    MAILING_NO_ACCOUNTS = """Ни один аккаунт не включен"""
    MAILING_CHOOSE_MESSAGE = """Выберите сообщение для рассылки:"""
    FINAL_INFO = """<b>Время расылки составит {time}\n\nКоличество получателей: {receivers_count}\n
В рассылке участвуют аккаунты:</b>\n\n{accounts}"""
    FINAL_INFO_UPDATE = """Данные обновлены:"""
    MAILING_RUNNING = """Рассылка выполняется..."""

    # Accounts
    ACCOUNTS_MENU = """Меню аккаунтов"""
    ACCOUNTS_PHONE_INPUT = """Введите номер телефона в формате <b>+7**********</b>:"""
    ACCOUNTS_EXISTS = """Аккаунт с данным номером уже подключен"""
    ACCOUNTS_CODE_INPUT = """Введите проверочный код:"""
    ACCOUNTS_PHONE_INCORRECT_INPUT = """Данный номер имеет неверный формат. Попробуйте снова"""
    ACCOUNTS_PHONE_INPUT_FLOOD = """Произведено слишком много попыток аутентификации на данный номер\n
Попробуйте другой номер или повторите попытку через {} сек"""
    ACCOUNTS_CODE_INCORRECT_INPUT = """Введенный код был неверным. Попробуйте снова"""
    ACCOUNTS_CODE_EXPIRED_INPUT = """Введенный код устарел, либо вы пытаетесь добавить аккаунт, который используете в данный момент\n
Попробуйте снова"""
    ACCOUNTS_CONFIRM_DELETE = """Вы точно хотите удалить аккаунт в номером {phone_number}?"""
    ACCOUNTS_DELETED_ON_AUTH = """Аккаунт <b>{first_name} {phone_number}</b> был вынужденно удален из-за потери доступа"""

    # Messages
    MESSAGES_MENU = """Меню сообщений"""
    MESSAGES_LIST = """Список сообщений"""
    MESSAGE_TITLE_INPUT = """Введите заголовок нового сообщения:"""
    MESSAGE_TITLE_INPUT_UNIQUE = """Сообщение с данным заголовком уже существует"""
    MESSAGE_TEXT_INPUT = """Введите текст нового сообщения:"""
    MESSAGE_MEDIA_INPUT = """Отправьте изображение/видео нового сообщение, либо пропустите этот шаг:"""
    MESSAGE_INCORRECT_INPUT = """Сообщение должно быть исключительно текстовым"""
    MESSAGE_ADD_CONFIRM = """Уверены, что хотите добавить такое сообщение?\n\n<b>{title}</b>\n\n{message}"""
    MESSAGE_DELETE_CONFIRM = """Уверены, что хотите удалить сообщение "{message.title}"?"""

    # Receivers
    RECEIVERS_MENU = """Выберите способ получение адресатов"""
    RECEIVERS_FILE_INPUT = """Отправьте файл с расширением <b>.txt</b>\nФайл должен содержать номера телефонов и/или username-ы"""
    RECEIVERS_FILE_CONFIRM = """<b>Проверьте содержимое файла:</b>\n\n{receivers}\n..."""
    RECEIVERS_CHAT_INPUT = """Отправьте <b>username</b> группы\nСписок пользователей группы должен быть доступен каждому"""
    RECEIVERS_CHAT_NO_MEMBERS = """Из данной группы не удалось получить ни одного пользователя\nПопробуйте другую группу"""
    RECEIVERS_CHAT_ERROR = """Группа с таким именем не найдена\nПопробуйте ввести другое имя группы"""
    RECEIVERS_GEO_INPUT = """Отправьте геолокацию, откуда хотите собрать получателей"""
    RECEIVERS_GEO_NO_USERS = """В данной локации не удалось найти пользователей\nПопробуйте прислать другую локацию"""
