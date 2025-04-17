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

def calculate_prepay_pod_avg_cost(df_conpri, split):
    df_conpri['TotalValueOfContract'] = sum(
        df_conpri[f'firmERYr{i}'] * df_conpri[f'PODPriceYr{i}'] for i in range(1, 11)
    )
    
    # Calculate total prepay values for first and second splits
    df_conpri[f'TotalPrepayValue{split}'] = df_conpri['TotalValueOfContract'] * (df_conpri['firstSplit'] / 100)
    
    # Initialize cumulative prepay amount
    df_conpri[f'CumulativePrepayAmount{split}'] = 0

    for i in range(10):
        year = i + 1
        prepay_col = f'PrepayVol{split}Yr{year}'
        pod_vol_col = f'PODVol{split}Yr{year}'
        pod_payment_col = f'PODPayment{split}Yr{year}'
        avg_cost_col = f'AvgCostTon{split}Yr{year}'
        prepay_payment_col = f'PrepayPayment{split}Yr{year}'

        # Calculate remaining prepay
        df_conpri['PrepayRemaining'] = df_conpri[f'TotalPrepayValue{split}'] - df_conpri[f'CumulativePrepayAmount{split}']

        # Prepay logic
        df_conpri[prepay_col] = df_conpri.apply(
            lambda x: x[f'firmERYr{year}'] if x['PrepayRemaining'] > 0 else 0,
            axis=1
        )
        df_conpri[pod_vol_col] = df_conpri.apply(
            lambda x: 0 if x['PrepayRemaining'] > 0 else x[f'firmERYr{year}'],
            axis=1
        )
        df_conpri[prepay_payment_col] = df_conpri[prepay_col] * df_conpri[f'prepayPriceYr{year}']
        df_conpri[pod_payment_col] = df_conpri[pod_vol_col] * df_conpri[f'PODPriceYr{year}']

        # Calculate temporary payment
        df_conpri['TempPayment'] = df_conpri[prepay_col] * df_conpri[f'prepayPriceYr{year}']

        # Update cumulative prepay amount
        df_conpri[f'CumulativePrepayAmount{split}'] += df_conpri['TempPayment']

        # Handle case where prepay is exhausted
        df_conpri.loc[df_conpri['PrepayRemaining'] <= 0, pod_payment_col] = (
            df_conpri['PrepayRemaining'] * -1
        )
        df_conpri.loc[df_conpri['PrepayRemaining'] <= 0, pod_vol_col] = (
            df_conpri[pod_payment_col] / df_conpri[f'PODPriceYr{year}']
        )
        df_conpri.loc[df_conpri['PrepayRemaining'] <= 0, prepay_col] = (
            df_conpri['PrepayRemaining'] / df_conpri[f'prepayPriceYr{year}']
        )
        df_conpri.loc[df_conpri['PrepayRemaining'] <= 0, prepay_payment_col] = df_conpri['PrepayRemaining']

        # Calculate average cost per tonne
        df_conpri[avg_cost_col] = df_conpri.apply(
            lambda x: (x[prepay_payment_col] + x[pod_payment_col]) / x[f'firmERYr{year}']
            if x[f'firmERYr{year}'] > 0 else 0,
            axis=1
        )

    # Drop temporary columns
    df_conpri.drop(columns=['PrepayRemaining', 'TempPayment'], inplace=True)

    return df_conpri