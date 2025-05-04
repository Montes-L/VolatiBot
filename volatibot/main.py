import os
import time
from variation_checker import VariationChecker

# Récupère les tickets
tickers_env = os.getenv("TICKERS")
tickers = [ticker.strip().upper() for ticker in tickers_env.split(",") if ticker.strip()]
# Récupère le seuil d'alerte
levels_env = os.getenv("ALERT_LEVELS", "5,10,15")
levels = [float(level.strip()) for level in levels_env.split(",") if level.strip()]
interval = int(os.getenv("CHECK_INTERVAL", "600"))  # default is 10 minutes

checker = VariationChecker(tickers=tickers, levels=levels)

while True:
    print("New verification of stock market variations...")
    checker.check_open_prepost_market()
    print(f"Pause {interval} seconds before next check.\n")
    time.sleep(interval)

