
import pandas_datareader as pdr
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_analysts_info
#Helper functions for the main notebook

def intrinsic_value(eps, five_years_growth_rate, current_yield_of_aaa_corporate_bonds):
    v = (eps * (7 + (1.0*five_years_growth_rate)) * 4.4)
    print(v/current_yield_of_aaa_corporate_bonds)
    return v/current_yield_of_aaa_corporate_bonds


def safety_margin(instrincic_value, current_price):
    return current_price/instrincic_value

def acceptable_buy_price(margin_of_safety, difference):
    return margin_of_safety * difference


print(acceptable_buy_price(0.65, safety_margin(
    intrinsic_value(5.11, 17.93, 2.57), 145.86)))


def buy_or_sell(acceptable_buy_price, current_price):
    if acceptable_buy_price > current_price:
        return "buy"
    else:
        return "sell"
    

def get_data(ticker, ng_pe, multiplier, margin):
    quote = si.get_quote_table(ticker)
    print(quote)
    current_price = quote["Quote Price"]
    eps = quote["EPS (TTM)"]
    growth_df = get_analysts_info(ticker)['Growth Estimates']
    growth_rate = growth_df.iloc[4][1] 
    growth_rate = str(growth_rate).rstrip("%") if isinstance(growth_rate, str) else ''
    aaa_df = pdr.get_data_fred('AAA')
    current_yield = aaa_df.iloc[-1][0]

    output = {
        "current_price": float(current_price),
        "eps": float(eps),
        "growth_rate": float(growth_rate) if growth_rate else '',
        "current_yield": float(current_yield),
        "ng_pe": float(ng_pe),
        "multiplier": float(multiplier),
        "margin": float(margin)
    }
    return output
