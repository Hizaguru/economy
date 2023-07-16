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
def margin_of_safety(instrincic_value, current_price):
    return current_price / instrincic_value


# Calculate the acceptable buy price based on the safety margin and a difference factor.
def acceptable_buy_price(margin_of_safety, difference):
    return margin_of_safety * difference


# Determine whether to buy or sell a stock based on the acceptable buy price and current price.
def buy_or_sell(acceptable_buy_price, current_price):
    if acceptable_buy_price > current_price:
        return "Buy"
    elif acceptable_buy_price == current_price:
        return "Hold"
    else:
        return "Sell"


def five_year_growth_estimate(ticker):
    growth_estimates = get_analysts_info(ticker)["Growth Estimates"]
    return growth_estimates.loc[4, ticker]


# Retrieve data for a stock, including current price, EPS, growth rate,
# current yield, P/E ratio, multiplier, and margin.
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
