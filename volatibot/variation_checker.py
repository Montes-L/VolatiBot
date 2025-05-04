from datetime import datetime
import yfinance as yf
from notifier import NotificationManager
from discord_alert import send_discord_alert
import pytz


class VariationChecker:
    def __init__(self, tickers: list[str], levels: list[int] = [5, 10, 15]):
        self.tickers = tickers
        self.levels = levels
        self.notifier = NotificationManager()

    def get_closing_data(self, ticker: str, period: str ="2d", interval: str="1d", iloc: float=-2):
        historique = yf.download(ticker, period=period, interval=interval, progress=False)
        last_row = historique.iloc[iloc]
        return last_row["Close"].item(), last_row.name.isoformat()

    def get_latest_price(self, ticker: str, prepost_market: bool):
        intraday = yf.download(ticker, period="1d", interval="1m", prepost=prepost_market, progress=False)
        return intraday["Close"].iloc[-1].item()

    def calc_variation_percent(self, old_price: float, new_price: float) -> float:
        return ((new_price - old_price) / old_price) * 100
    
    def conditioner(self, ticker, variation: float, old_value: float, new_value: float, closing_timestamp, context: str, extra_condition: bool= True):
        for level in self.levels:
            condition_variation = abs(variation) >= level
            condition_notified = not self.notifier.has_been_notified(ticker, closing_timestamp, level, context=context)
            should_notify = condition_variation and condition_notified and extra_condition

            print(f"Checking the {ticker} ticket for a variation of {level}%:")
            print(f"   ➤ Variation of {variation:.2f}% >= {level} ? {'✅' if condition_variation else '❌'}")
            print(f"   ➤ Already notified ? {'✅ No' if condition_notified else '❌ Yes'}")
            print(f"   ➤ Extra Condition ? {'✅ Yes' if extra_condition else '❌ No'}" if context !="openMarket" else "   ➤ No extra condition")

            if should_notify:
                emoji = "🟢" if variation > 0 else "🔴"
                send_discord_alert(
                    message=f"{emoji} {ticker} affiche une variation de {variation:.2f}% en {context} 🕒 ({old_value:.2f} ➡️ {new_value:.2f})"
                )
                self.notifier.add_notification(ticker, closing_timestamp, level, context=context)
            
            else:
                print(f"⚠️ Alert ignored for {ticker} ({context}) at {closing_timestamp} at treshold {level}%")

    def check_since_close(self):
        context="openMarket"
        for ticker in self.tickers:
            print(f"Looking for {ticker}...")

            try:
                old_price, closing_timestamp = self.get_closing_data(ticker, iloc=-2)
                new_price = self.get_latest_price(ticker, prepost_market=False)
                variation = self.calc_variation_percent(old_price, new_price)

                print(f"📊 {ticker} ({context}) : variation = {variation:.2f}%")

                self.conditioner(ticker=ticker,
                                 variation=variation,
                                 old_value=old_price,
                                 new_value=new_price,
                                 closing_timestamp=closing_timestamp,
                                 context=context)

            except Exception as e:
                print(f"❌ Error for {ticker} : {e}")

    def check_premarket_postmarket(self):
        for ticker in self.tickers:
            print(f"🌙 Pre/post-market processing for {ticker}...")

            try:
                closing_price, closing_timestamp = self.get_closing_data(ticker, iloc=-1)

                latest_price = self.get_latest_price(ticker, prepost_market=True)
                variation = self.calc_variation_percent(closing_price, latest_price)

                print(f"📊 {ticker} (prepost) : variation = {variation:.2f}%")

                ny_now = datetime.now(pytz.timezone("America/New_York"))
                is_market_closed = not (9 <= ny_now.hour < 16)

                self.conditioner(
                    ticker=ticker,
                    variation=variation,
                    old_value=closing_price,
                    new_value=latest_price,
                    closing_timestamp=closing_timestamp,
                    context="prepost-market",
                    extra_condition=is_market_closed
                )

            except Exception as e:
                print(f"❌ Error for {ticker} in prepost-market : {e}")
    
    def check_open_prepost_market(self):
        self.check_since_close()
        self.check_premarket_postmarket()
