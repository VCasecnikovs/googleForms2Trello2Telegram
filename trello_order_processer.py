from trello import TrelloClient
from entity import Order
from utils import parse_str2datetime
import pytz


class TrelloOrderProcesser():
    def __init__(self, api_public, api_secret, board_id, list_id, with_stilistic_label_id, without_stilistic_label_id) -> None:
        self.trello_client = TrelloClient(
            api_key=api_public,
            api_secret=api_secret
        )

        self.stilistic_label = self.trello_client.get_label(
            with_stilistic_label_id, board_id)
        self.without_stilistic_label = self.trello_client.get_label(
            without_stilistic_label_id, board_id)
        self.todo_list = self.trello_client.get_list(list_id)

    def create_payment_template(self, order: Order):
        return f'''      
    Здравствуйте,
    Мы получили и подтвердили ваш заказ:
    Дата и время игры: {order.date} {order.time}
    Ведущий: !!!Ввести ведущего
    Платформа проведения: {order.platform}

    {"Стилистика: " + order.stilistic_description if order.has_stilistic else ""}

    Если все выше перечисленные аспекты игры соответствуют вашему заказу, и вы ничего не хотите изменить, то оплатите игру и пошлите подтверждение об оплате. Как только средства поступят к нам на счёт, вам будет отправлено сообщение о получении оплаты, и ведущий начнёт подготовку к игре.

    Сумма для оплаты: {1195 if order.has_stilistic else 495} рублей

    Реквизиты для оплаты:
    4082 0810 5044 3000 2543
    БИК номер банка:044525593


    С уважением,
    команда разработчиков Shelter.
'''

    def process(self, order: Order):
        name = f"{order.index}. {order.contact} {'со стилистикой' if order.has_stilistic  else 'без стилистики'}"

        stilictic_info = ""
        if order.has_stilistic:
            stilictic_info = f'''Игра со стилистикой🧙‍♂️:
                🔢Количество игроков: {order.stilistic_players_amount}
                🎞️Стилистика: {order.stilistic_description}
            '''

        description = f'''Описание заказа📄:

📅Дата проведения: {order.date}
⏲️Время проведения: {order.time}
🧑‍🦲Контакт: {order.contact}
🤙Платформа: {order.platform}

{stilictic_info}

Дополнительная информация: {order.additional_info}
Время заказа по Риге: {order.timestamp}

        
ШАБЛОНЧИК (ВАЖНО ВВЕСТИ ВЕДУЩЕГО И ЖЕЛАТЕЛЬНО ОПИСАТЬ СВОИМИ СЛОВАМИ СТИЛИСТИКУ!!!):
{self.create_payment_template(order)}       
        '''
        labels = [
            self.stilistic_label if order.has_stilistic else self.without_stilistic_label]

        iso_format_date = parse_str2datetime(
            f"{order.date} {order.time}", default_timezone=pytz.timezone("Europe/Moscow")).isoformat()

        self.todo_list.add_card(name, desc=description,
                                labels=labels, due=iso_format_date)
