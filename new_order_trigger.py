import datetime
from typing import List
import gspread

from repository import JSON_Repository
from utils import parse_str2datetime, get
from processer import Processer
from entity import Order


class GoogleSheetsOrderTrigger():
    def __init__(self, repository: JSON_Repository, processers: List[Processer], service_account, table_name, header_shift=1):
        self.repository = repository
        self.header_shift = header_shift
        self.processers = processers

        gc = gspread.service_account(service_account)
        sh = gc.open(table_name)
        self.forms_worksheet = sh.get_worksheet(0)

    def get_all_unprocessed_orders_indexes(self, last_processed_order_timestamp: datetime.datetime):
        order_timestamps = self.forms_worksheet.col_values(1)[
            self.header_shift:]
        newest_order = last_processed_order_timestamp

        orders_indexes = []
        for order_index, ts in enumerate(order_timestamps):
            order_dt = parse_str2datetime(ts)
            if order_dt > last_processed_order_timestamp:
                # last one is because enumerate starts with 0, but rows in google sheets starts with one
                orders_indexes.append(order_index + self.header_shift + 1)
                if order_dt > newest_order:
                    newest_order = order_dt

        return orders_indexes, newest_order

    def get_unprocessed_orders(self, unpocessed_orders_indexes):
        orders = []
        for index in unpocessed_orders_indexes:
            order_row = self.forms_worksheet.row_values(index)
            order = Order(
                index=index,
                timestamp=parse_str2datetime(get(order_row, 0)),
                date=get(order_row, 1),
                time=get(order_row, 2),
                contact=get(order_row, 3),
                platform=get(order_row, 4),
                additional_info=get(order_row, 6),
                has_stilistic=get(order_row, 7) == "Да",
                stilistic_players_amount=get(order_row, 8),
                stilistic_description=get(order_row, 5)
            )
            orders.append(order)
        return orders

    def process_orders(self, orders: List[Order]):
        for order in orders:
            for processer in self.processers:
                processer.process(order)

    def run(self):
        last_processed_order_timestamp = self.repository.get_last_processed_order_timestamp()

        unpocessed_orders_indexes, newest_order = self.get_all_unprocessed_orders_indexes(
            last_processed_order_timestamp)
        orders = self.get_unprocessed_orders(unpocessed_orders_indexes)

        self.process_orders(orders)

        self.repository.save_newest_processed_order(newest_order)
