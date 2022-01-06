import telegram
from entity import Order


class TelegramOrderProcesser():
    def __init__(self, token, chat_id) -> None:
        self.chat_id = chat_id

        self.bot = telegram.Bot(token=token)

    def process(self, order: Order):

        stilictic_info = ""
        if order.has_stilistic:
            stilictic_info = f'''Игра со стилистикой🧙‍♂️:
                🔢Количество игроков: {order.stilistic_players_amount}
                🎞️Стилистика: {order.stilistic_description}
            '''

        message_text = f"""
        👻👻НОВЫЙ ЗАКАЗ👻👻
        
    {order.index}. {order.contact} {'со стилистикой' if order.has_stilistic  else 'без стилистики'}
        
    Описание заказа📄:
    
        📅Дата проведения: {order.date}
        ⏲️Время проведения: {order.time}
        🧑‍🦲Контакт: {order.contact}
        🤙Платформа: {order.platform}

    {stilictic_info}

    Дополнительная информация: {order.additional_info}
    Время заказа по Риге: {order.timestamp}
        
        """
        self.bot.send_message(self.chat_id, message_text)
