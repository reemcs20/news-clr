import telegram_send
from telegram_send import telegram


def SendToChannel(title: str, published_date: str, category: list, link: str) -> None:
    """
    :param title: news heading
    :param published_date: the date of posting the news
    :param category: news category
    :param link: source of link
    :rtype: None
    A method that sends news to Telegram Bot
    """
    try:
        formed_message = "Title: {}\nCategory: {}\nPublished Date: {}\nSource: [Visit]({})".format(title, category,
                                                                                                   published_date, link)
        telegram_send.send(parse_mode=telegram.ParseMode.MARKDOWN, messages=[formed_message])
    except BaseException as e:
        print(e)
