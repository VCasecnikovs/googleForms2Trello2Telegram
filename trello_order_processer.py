from trello import TrelloClient
from entity import Order


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
        '''
        labels = [
            self.stilistic_label if order.has_stilistic else self.without_stilistic_label]

        self.todo_list.add_card(name, desc=description, labels=labels)
