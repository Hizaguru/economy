def intrinsic_value(eps, five_years_growth_rate, current_yield_of_aaa_corporate_bonds):
    v = (eps * (8.5 + (2.0*five_years_growth_rate)) * 4.4 )
    print(v/current_yield_of_aaa_corporate_bonds)
    return v/current_yield_of_aaa_corporate_bonds
print(intrinsic_value(5.11, 17.93, 2.57))

def safety_margin(instrincic_value, current_price):
    return current_price/instrincic_value
print(safety_margin(intrinsic_value(5.11, 17.93, 2.57), 145.86))