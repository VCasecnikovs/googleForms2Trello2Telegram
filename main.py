import pytz

from new_order_trigger import GoogleSheetsOrderTrigger
from repository import JSON_Repository
from trello_order_processer import TrelloOrderProcesser
from telegram_order_processer import TelegramOrderProcesser




if __name__ == "__main__":
    processers = [TrelloOrderProcesser(TRELLO_API_PUBLIC,
                                       TRELLO_API_SECRET,
                                       TRELLO_BOARD_ID,
                                       TRELLO_LIST_ID,
                                       TRELLO_WITH_STILISTIC_LABEL_ID,
                                       TRELLO_WITHOUT_STILISTIC_LABEL_ID),
                  TelegramOrderProcesser(TELEGRAM_TOKEN,
                                         TELEGRAM_CHAT_ID)]

    gsot = GoogleSheetsOrderTrigger(
        JSON_Repository(
            JSON_FILE,
            DEFAULT_TIMEZONE,
            TIME_FORMAT),
        processers,
        SERVICE_ACCOUNT,
        TABLE_NAME,
        HEADER_SHIFT)

    gsot.run()
