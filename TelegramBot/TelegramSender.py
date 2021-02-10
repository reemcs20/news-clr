import telegram_send
from telegram_send import telegram


def SendToChannel(message):
    try:
        telegram_send.send(parse_mode=telegram.ParseMode.MARKDOWN, messages=[message])
    except BaseException as e:
        print(e)
