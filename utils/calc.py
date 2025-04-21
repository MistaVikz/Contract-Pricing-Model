import numpy_financial as npf
import pandas as pd

def calc_top_bottom_discount_rate(df_spread, spreadChoice, ovRating, cLength, discCorpContract, is_Top):   
    """
    Calculate the top or bottom discount rate for a corporate contract.

    Args:
        df_spread (pd.DataFrame): DataFrame containing spread data.
        spreadChoice (str): The spread type (e.g., 'AAA', 'BBB').
        ovRating (str): The overall rating of the contract (e.g., 'A', 'B', 'C').
        cLength (int): The contract length in years.
        discCorpContract (float): The discount on the corporate contract.
        is_Top (bool): Whether to calculate the top discount rate (True) or bottom discount rate (False).

    Returns:
        float: The calculated discount rate.
    """
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
    """
    Calculate the RA (Risk Adjustment) price for a contract.

    Args:
        discount_rate (float): The discount rate for the contract.
        techFuncPrice (float): The technical function price.
        cLength (int): The contract length in years.

    Returns:
        float: The calculated RA price.
    """
    ratio = npf.pv(discount_rate / 100, cLength, 0 , 100) * -1
    return round((ratio * techFuncPrice) / 100, 2)

def calculate_prepay_pod_avg_cost(df_conpri, split):
    """
    Calculate prepay, POD (Point of Delivery), and average cost per ton for a contract.

    Args:
        df_conpri (pd.DataFrame): DataFrame containing contract pricing data.
        split (int): The percentage split for prepay (e.g., 30 or 50).

    Returns:
        pd.DataFrame: The updated DataFrame with calculated columns for prepay, POD, and average cost.
    """
    # Dictionary to store new columns
    new_columns = {f'PrepayVol{split}Yr{year}': [] for year in range(1, 11)}
    new_columns.update({f'PODVol{split}Yr{year}': [] for year in range(1, 11)})
    new_columns.update({f'PODPayment{split}Yr{year}': [] for year in range(1, 11)})
    new_columns.update({f'AvgCostTon{split}Yr{year}': [] for year in range(1, 11)})
    new_columns.update({f'PrepayPayment{split}Yr{year}': [] for year in range(1, 11)})

    # Helper function to calculate prepay and POD values for each row
    def calculate_row(row):
        total_value_of_contract = sum(
            row[f'firmERYr{i}'] * row[f'PODPriceYr{i}'] for i in range(1, int(row['cLength']) + 1)
        )
        total_prepay_value = total_value_of_contract * (split / 100)
        cumulative_prepay_amount = 0
        row_results = {key: 0 for key in new_columns.keys()}  # Initialize all columns for this row with default values

        for year in range(1, int(row['cLength']) + 1):
            prepay_col = f'PrepayVol{split}Yr{year}'
            pod_vol_col = f'PODVol{split}Yr{year}'
            pod_payment_col = f'PODPayment{split}Yr{year}'
            avg_cost_col = f'AvgCostTon{split}Yr{year}'
            prepay_payment_col = f'PrepayPayment{split}Yr{year}'

            if total_prepay_value - cumulative_prepay_amount > 0:
                # Prepay logic
                prepay_remaining = total_prepay_value - cumulative_prepay_amount
                row_results[prepay_col] = row[f'firmERYr{year}']
                row_results[pod_vol_col] = 0
                row_results[pod_payment_col] = 0
                temp_payment = row_results[prepay_col] * row[f'prepayPriceYr{year}']
                row_results[prepay_payment_col] = temp_payment
                cumulative_prepay_amount += temp_payment

                if total_prepay_value - cumulative_prepay_amount <= 0:
                    # Handle case where prepay is exhausted
                    row_results[pod_payment_col] = (total_prepay_value - cumulative_prepay_amount) * -1
                    row_results[pod_vol_col] = row_results[pod_payment_col] / row[f'PODPriceYr{year}']
                    row_results[prepay_col] = prepay_remaining / row[f'prepayPriceYr{year}']
                    row_results[prepay_payment_col] = prepay_remaining
                    temp_payment = row_results[prepay_payment_col] + row_results[pod_payment_col]
                    row_results[avg_cost_col] = (
                        temp_payment / row[f'firmERYr{year}']
                        if row[f'firmERYr{year}'] > 0 else 0
                    )
            else:
                # POD logic
                row_results[prepay_col] = 0
                row_results[pod_vol_col] = row[f'firmERYr{year}']
                row_results[pod_payment_col] = row_results[pod_vol_col] * row[f'PODPriceYr{year}']
                temp_payment = row_results[pod_payment_col]
                row_results[avg_cost_col] = (
                    temp_payment / row[f'firmERYr{year}']
                    if row[f'firmERYr{year}'] > 0 else 0
                )

        return row_results

    # Calculate all rows
    row_results = df_conpri.apply(calculate_row, axis=1)

    # Combine all row results into the new_columns dictionary
    for col in new_columns.keys():
        new_columns[col] = row_results.apply(lambda x: x[col]).tolist()

    # Add all new columns to the DataFrame at once
    new_columns_df = pd.DataFrame(new_columns, index=df_conpri.index)
    df_conpri = pd.concat([df_conpri, new_columns_df], axis=1)

    return df_conpri

def calc_cash_flow(rofrToBuyer, year, cLength, podPrice, podPayment, salesPrice, firmEr, fee, prePayAndOption = None):
    """
    Calculate the cash flow for a specific year of a contract.

    Args:
        rofrToBuyer (float): The ROFR (Right of First Refusal) volume to the buyer.
        year (int): The year for which to calculate cash flow.
        cLength (int): The contract length in years.
        podPrice (float): The POD (Point of Delivery) price.
        podPayment (float): The POD payment.
        salesPrice (float): The sales price.
        firmEr (float): The firm energy requirement.
        fee (float): The fee for the year.
        prePayAndOption (float, optional): The prepay and option cost (if applicable).

    Returns:
        float: The calculated cash flow for the year.
    """
    if(year > cLength):
        return None
    elif(year == cLength):
        rofrCost = rofrToBuyer * podPrice
        rofrSales = rofrToBuyer * salesPrice
        revenue = round((firmEr * salesPrice) + rofrSales, 2)
        cost = round(podPayment + rofrCost + fee, 2)
    elif(year < 4):
        revenue = round(firmEr * salesPrice, 2)
        cost = round(prePayAndOption + podPayment + fee, 2)
    else:
        revenue = round(firmEr * salesPrice, 2)
        cost = round(podPayment + fee, 2)
    return (cost * -1) + revenue

def calc_irr(cashYr1, cashYr2, cashYr3, cashYr4, cashYr5, cashYr6, cashYr7, cashYr8, cashYr9, cashYr10, simulationName, split):
    """
    Calculate the IRR (Internal Rate of Return) for a contract.

    Args:
        cashYr1, ..., cashYr10 (float): Cash flows for years 1 through 10.
        simulationName (str): The name of the simulation.
        split (int): The percentage split for prepay (e.g., 30 or 50).

    Returns:
        float: The calculated IRR, or None if it cannot be calculated.
    """
    cashFlows = [cashYr1, cashYr2, cashYr3, cashYr4, cashYr5, cashYr6, cashYr7, cashYr8, cashYr9, cashYr10]
    cashFlowsNotNull = [x for x in cashFlows if not pd.isnull(x)]
        
    if len(cashFlowsNotNull) == 0:
        return None
    elif len(cashFlowsNotNull) == 1:
        return cashFlowsNotNull[0] * 100
    irr = round(npf.irr(cashFlowsNotNull) * 100, 2)
    
    if pd.isnull(irr):
        print(f'IRR {split} could not be calculated for {simulationName}. Check cash flows.')
    return irr


