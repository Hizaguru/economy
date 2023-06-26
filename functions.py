import pandas_datareader as pdr
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_analysts_info


# Helper functions for the main notebook


# Calculate the intrinsic value of a stock based on earnings per share (EPS),
# five-year growth rate, and current yield of AAA corporate bonds.
def intrinsic_value(eps, five_years_growth_rate, current_yield_of_aaa_corporate_bonds):
    if eps and five_years_growth_rate and current_yield_of_aaa_corporate_bonds:
        v = eps * (7 + (1.0 * five_years_growth_rate)) * 4.4
        return v / current_yield_of_aaa_corporate_bonds
    return "N/A"


# Calculate the safety margin of a stock based on its intrinsic value and current price.
def safety_margin(instrincic_value, current_price):
    return current_price / instrincic_value


# Calculate the acceptable buy price based on the safety margin and a difference factor.
def acceptable_buy_price(margin_of_safety, difference):
    return margin_of_safety * difference


# Determine whether to buy or sell a stock based on the acceptable buy price and current price.
def buy_or_sell(acceptable_buy_price, current_price):
    if acceptable_buy_price > current_price:
        return "buy"
    else:
        return "sell"


# Retrieve data for a stock, including current price, EPS, growth rate,
# current yield, P/E ratio, multiplier, and margin.
def get_data(ticker, ng_pe, multiplier, margin):
    quote = si.get_quote_table(ticker)
    current_price = quote["Quote Price"]
    eps = quote["EPS (TTM)"]
    growth_df = get_analysts_info(ticker)["Growth Estimates"]
    growth_rate = growth_df.iloc[4][1]
    growth_rate = str(growth_rate).rstrip("%") if isinstance(growth_rate, str) else ""
    aaa_df = pdr.get_data_fred("AAA")
    current_yield = aaa_df.iloc[-1][0]

    if ng_pe is None:
        ng_pe = 0.0

    output = {
        "Current Price": float(current_price),
        "Eps": float(eps),
        "Growth Rate": float(growth_rate) if growth_rate else "",
        "Current Yield": float(current_yield),
        "P/E": float(ng_pe),
        "Multiplier": float(multiplier),
        "Margin": float(margin),
    }
    return output
