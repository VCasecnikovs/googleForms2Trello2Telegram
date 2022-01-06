from typing import Protocol, List
from entity import Order


class Processer(Protocol):
    def process(self, orders: List[Order]):
        ...
