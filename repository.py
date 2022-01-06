import datetime
from os import path
import json
from utils import parse_str2datetime


class JSON_Repository():
    def __init__(self, json_file, default_timezone, time_format):
        self.json_file = json_file
        self.default_timezone = default_timezone
        self.time_format = time_format

    def get_last_processed_order_timestamp(self):
        if not path.exists(self.json_file):
            return datetime.datetime(1900, 1, 1).replace(tzinfo=self.default_timezone)
        with open(self.json_file) as f:
            prev_run_info = json.load(f)
            return parse_str2datetime(prev_run_info["last_update_time"])

    def save_newest_processed_order(self, dt: datetime.datetime):
        with open(self.json_file, "w") as f:
            json.dump({"last_update_time": dt.strftime(self.time_format)}, f)
