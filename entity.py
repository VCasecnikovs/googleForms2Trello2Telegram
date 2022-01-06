from dataclasses import dataclass
import datetime


@dataclass
class Order:
    index: int
    timestamp: datetime.datetime
    date: str
    time: str
    contact: str
    platform: str
    additional_info: str
    has_stilistic: bool
    stilistic_players_amount: str
    stilistic_description: str
