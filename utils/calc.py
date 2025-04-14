import numpy_financial as npf

def calc_top_bottom_discount_rate(df_spread, spreadChoice, ovRating, cLength, discCorpContract, is_Top):   
    # Filter df_spread by spreadChoice and ovRating
    df_spread_filtered = df_spread[(df_spread['sType'] == spreadChoice) & (df_spread['rating'] == ovRating)]
    
    # If not C then top/bottom spreads are different
    if ovRating != 'C':
        # Lookup the top and bottom spreads
        if cLength == 1 or cLength == 2 or cLength == 3 or cLength == 5 or cLength == 7 or cLength == 10:
            spread_col = f's{cLength}Yr'
        
            if is_Top:
                spread = df_spread_filtered[spread_col].iloc[0]
            else:
                spread = df_spread_filtered[spread_col].iloc[len(df_spread_filtered) - 1]
            return discCorpContract + (spread / 100)
        # For 8 and 9 year contracts, use the 10 and 7 year spreads respectively
        elif cLength == 8 or cLength == 9:
            spread_plus_col = 's10Yr'
            spread_minus_col = 's7Yr'

            if is_Top:
                spread_plus = df_spread_filtered[spread_plus_col].iloc[0]
                spread_minus = df_spread_filtered[spread_minus_col].iloc[0]
                spread = ((spread_plus + spread_minus) / (10-7)) + spread_minus
            else:
                spread_plus = df_spread_filtered[spread_plus_col].iloc[len(df_spread_filtered) - 1]
                spread_minus = df_spread_filtered[spread_minus_col].iloc[len(df_spread_filtered) - 1]
                spread = ((spread_plus + spread_minus) / (10-7)) + spread_minus
            return discCorpContract + (spread / 100)
        # For all other lengths, use the spread for the next and previous lengths
        else:
            spread_plus_col = f's{cLength + 1}Yr'
            spread_minus_col = f's{cLength - 1}Yr'

            if is_Top:
                spread_plus = df_spread_filtered[spread_plus_col].iloc[0]
                spread_minus = df_spread_filtered[spread_minus_col].iloc[0]
                spread = ((spread_plus + spread_minus) / (cLength + 1 - (cLength - 1))) + spread_minus
            else:
                spread_plus = df_spread_filtered[spread_plus_col].iloc[len(df_spread_filtered) - 1]
                spread_minus = df_spread_filtered[spread_minus_col].iloc[len(df_spread_filtered) - 1]
                spread = ((spread_plus + spread_minus) / (cLength + 1 - (cLength - 1))) + spread_minus
            return discCorpContract + (spread / 100)
    else:
        # For C rating, use the same spread for top and bottom
        if cLength == 1 or cLength == 2 or cLength == 3 or cLength == 5 or cLength == 7 or cLength == 10:
            spread_col = f's{cLength}Yr'
            spread = df_spread_filtered[spread_col].iloc[0]
            return discCorpContract + (spread / 100)
        elif cLength == 8 or cLength == 9:
            spread_plus_col = 's10Yr'
            spread_minus_col = 's7Yr'
            spread_plus = df_spread_filtered[spread_plus_col].iloc[0]
            spread_minus = df_spread_filtered[spread_minus_col].iloc[0]
            spread = ((spread_plus + spread_minus) / (10-7)) + spread_minus
            return discCorpContract + (spread / 100)
        else:
            spread_plus_col = f's{cLength + 1}Yr'
            spread_minus_col = f's{cLength - 1}Yr'
            spread_plus = df_spread_filtered[spread_plus_col].iloc[0]
            spread_minus = df_spread_filtered[spread_minus_col].iloc[0]
            spread = ((spread_plus + spread_minus) / (cLength + 1 - (cLength - 1))) + spread_minus
            return discCorpContract + (spread / 100)            

def calc_ra_price(discount_rate, techFuncPrice, cLength):
    ratio = npf.pv(discount_rate / 100, cLength, 0 , 100) * -1
    return round((ratio * techFuncPrice) / 100, 2)
    