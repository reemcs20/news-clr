import telegram_send
from telegram_send import telegram


def SendToChannel(message):
    """:argument: message: a text of the news
       :rtype: None
       A method that sends news to Telegram Bot
    """
    try:
        telegram_send.send(parse_mode=telegram.ParseMode.MARKDOWN, messages=[message])
    except BaseException as e:
        print(e)
