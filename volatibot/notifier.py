import json
import os

class NotificationManager:
    def __init__(self, cache_file="notified.json"):
        self.cache_file = os.path.abspath(cache_file)
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, "w") as f:
                json.dump({}, f)

    def load(self):
        with open(self.cache_file, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.cache_file, "w") as f:
            json.dump(data, f, indent=4)

    def has_been_notified(self, ticker: str, timestamp: str, level: int, context: str = "openMarket") -> bool:
        data = self.load()
        return (
            ticker in data and
            timestamp in data[ticker] and
            context in data[ticker][timestamp] and
            str(level) in data[ticker][timestamp][context]
        )

    def add_notification(self, ticker: str, timestamp: str, level: int, context: str = "openMarket"):
        data = self.load()
        data.setdefault(ticker, {}).setdefault(timestamp, {}).setdefault(context, {})[str(level)] = True
        self.save(data)
