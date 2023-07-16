import pandas_datareader as pdr
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_analysts_info
from currency_converter import CurrencyConverter

# Converts SEK to EUR
c = CurrencyConverter()
ROUND_TO_BILLIONS = 0.000001


# Helper functions for the main notebook
# Calculate the intrinsic value of a stock based on earnings per share (EPS),
# five-year growth rate, and current yield of AAA corporate bonds.
def intrinsic_value(eps, five_years_growth_rate, current_yield_of_aaa_corporate_bonds):
    if eps and five_years_growth_rate and current_yield_of_aaa_corporate_bonds:
        v = eps * (7 + (1.0 * five_years_growth_rate)) * 4.4
        return v / current_yield_of_aaa_corporate_bonds
    return "N/A"


# Calculate the safety margin of a stock based on its intrinsic value and current price.
def margin_of_safety(instrincic_value, current_price):
    return current_price / instrincic_value


# Calculate the acceptable buy price based on the safety margin and a difference factor.
def acceptable_buy_price(margin_of_safety, intrinsic_val):
    print("margin_of_safety", margin_of_safety)
    return margin_of_safety * intrinsic_val


# Determine whether to buy or sell a stock based on the acceptable buy price and current price.
def buy_or_sell(acceptable_buy_price, current_price):
    print("acceptable buy price", acceptable_buy_price, current_price)
    if acceptable_buy_price > current_price:
        return "Buy"
    elif acceptable_buy_price == current_price:
        return "Hold"
    else:
        return "Sell"


def five_year_growth_estimate(ticker):
    growth_estimates = get_analysts_info(ticker)["Growth Estimates"]
    return growth_estimates.loc[4, ticker]


# Retrieve data for a stock from Yahoo Finance.
def get_data(ticker):
    next_5_years_growth_rate = five_year_growth_estimate(ticker)
    aaa_df = pdr.get_data_fred("AAA")
    current_yield = aaa_df.iloc[-1][0]

    output = {
        "Growth Rate": float(next_5_years_growth_rate.rstrip("%"))
        if isinstance(next_5_years_growth_rate, str)
        else next_5_years_growth_rate,
        "Current Yield": float(current_yield),
    }
    return output


def process_stock_data(
    stock_info, wanted_values, rounded_values, convert_to_euros, symbol
):
    data = get_data(symbol)
    current_yield = data["Current Yield"]
    five_year_growth_rate = data["Growth Rate"]
    print(five_year_growth_rate)
    eps = stock_info.get("trailingEps")
    print("eps", eps)
    intrinsic_val = intrinsic_value(eps, current_yield, five_year_growth_rate)
    print("intrinsic_val", intrinsic_val)
    current_price = stock_info.get("previousClose")
    print("current_price", current_price)

    SAFETY_MARGIN = 0.65
    print("safety_margin", SAFETY_MARGIN)
    buy_price = acceptable_buy_price(SAFETY_MARGIN, intrinsic_val)
    print("buy_price", buy_price)
    buy_sell = buy_or_sell(buy_price, current_price)
    d = {}
    for k, v in stock_info.items():
        if k in wanted_values:
            if k in rounded_values:
                v *= ROUND_TO_BILLIONS
            elif k in convert_to_euros and stock_info.get("currency") == "SEK":
                v = round(c.convert(v, "SEK", "EUR"), 1) * ROUND_TO_BILLIONS
            elif k == "enterpriseValue":
                v *= ROUND_TO_BILLIONS
            d[k] = [v]
    # Custom columns
    d["symbol"] = [symbol]
    d["Five year growth"] = [five_year_growth_rate]
    d["Intrinsic value"] = [intrinsic_val]
    d["safety margin"] = [SAFETY_MARGIN]
    d["Acceptable buying price"] = [buy_price]
    d["Buy/Sell"] = [buy_sell]
    return d
