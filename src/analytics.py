"""MarketPulse analytics: pure functions for comparison (TD07)."""


def index_by_date(prices):
    return {row["date"]: row for row in prices}
    


def align_series(instrument_prices, benchmark_prices):
    inst_by_date = index_by_date(instrument_prices)
    bench_by_date = index_by_date(benchmark_prices)
    common_dates = sorted(set(inst_by_date.keys()) & set(bench_by_date.keys()))
    aligned_instrument = [inst_by_date[d] for d in common_dates]
    aligned_benchmark = [bench_by_date[d] for d in common_dates]
    return aligned_instrument, aligned_benchmark


def calculate_period_return(prices):
    if not prices:
        raise ValueError("Price series cannot be empty.")
    first_close = float(prices[0]["close"])
    if first_close == 0.0:
        raise ValueError("First close cannot be zero.")
    last_close = float(prices[-1]["close"])
    return ((last_close / first_close) - 1.0) * 100.0


def calculate_base_100(prices):
    if not prices:
        raise ValueError("Price series cannot be empty.")
    first_close = float(prices[0]["close"])
    if first_close == 0.0:
        raise ValueError("First close cannot be zero.")
    return [
        {
            "date": row["date"],
            "ticker": row["ticker"],
            "value": (float(row["close"]) / first_close) * 100.0,
        }
        for row in prices
    ]

def calculate_relative_performance(instrument_return, benchmark_return):
    return instrument_return - benchmark_return