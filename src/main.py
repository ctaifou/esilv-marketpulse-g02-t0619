from pathlib import Path
import csv
import json

try:
    from src.analytics import (
        align_series,
        calculate_period_return,
        calculate_base_100,
        calculate_relative_performance,
    )
except ModuleNotFoundError:
    from analytics import (
        align_series,
        calculate_period_return,
        calculate_base_100,
        calculate_relative_performance,
    )
DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
PROVIDER_LABEL = "CSV"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])

def get_first_date(prices):
    return prices[0]["date"]

def get_last_date(prices):
    return prices[-1]["date"]
def display_market_summary(asset, prices, show_currency=True):
    currency_suffix = f" {asset['currency']}" if show_currency else ""
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Market       : {asset['market']}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(f"First close  : {get_first_close(prices):.2f}{currency_suffix}")
    print(f"Last close   : {get_last_close(prices):.2f}{currency_suffix}")



def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    print("=== MarketPulse ===")
    print("Market configuration")
    print(f"Period  : {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print(f"Provider: {PROVIDER_LABEL}")
    print()

    print("Instrument")
    display_market_summary(instrument, instrument_prices, show_currency=True)
    print()

    print("Benchmark")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)


    aligned_instrument, aligned_benchmark = align_series(instrument_prices, benchmark_prices)
    inst_return = calculate_period_return(aligned_instrument)
    bench_return = calculate_period_return(aligned_benchmark)
    rel_perf = calculate_relative_performance(inst_return, bench_return)
    inst_base_100 = calculate_base_100(aligned_instrument)
    bench_base_100 = calculate_base_100(aligned_benchmark)

    print("\nComparison (aligned)")
    print(f"Aligned sessions        : {len(aligned_instrument)}")
    print(f"{instrument['ticker']} period return      : {inst_return:+.2f}%")
    print(f"{benchmark['ticker']} period return     : {bench_return:+.2f}%")
    print(f"Relative performance    : {rel_perf:+.2f} percentage points")

    print("\nBase 100")
    print(f"{instrument['ticker']:<6} : {inst_base_100[0]['value']:.2f} -> {inst_base_100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']:<6} : {bench_base_100[0]['value']:.2f} -> {bench_base_100[-1]['value']:.2f}")
if __name__ == "__main__":
    main()