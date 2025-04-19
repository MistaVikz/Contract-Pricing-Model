from utils.io import *
from utils.calc import *

DB_PATH = "data/risk_model.db"

FIRST_SPLIT = 30
SECOND_SPLIT = 50

def main():
    df_conpri, df_spread = load_data(DB_PATH)

    # Calculate the yearly firm ER and ROFR to buyer
    for i in range(1, 11):
        df_conpri[f'firmERYr{i}'] = df_conpri[f'offYr{i}'] * (1 - df_conpri['totalShortfall'])
        df_conpri[f'ROFRtoBuyerYr{i}'] = df_conpri[f'offYr{i}'] - df_conpri[f'firmERYr{i}']

    # Calculate Discount on Corporate Contracts
    df_conpri['DiscCorpContract'] = df_conpri['risklessRate'] + df_conpri['spreadAAA'] + df_conpri['adjFactor']

    # Calculate top and bottom discount rates
    df_conpri['TopDiscRate'] = df_conpri.apply(lambda x: calc_top_bottom_discount_rate(df_spread, x['spreadChoice'], x['ovRating'], x['cLength'], x['DiscCorpContract'], True), axis=1)
    df_conpri['BottomDiscRate'] = df_conpri.apply(lambda x: calc_top_bottom_discount_rate(df_spread, x['spreadChoice'], x['ovRating'], x['cLength'], x['DiscCorpContract'], False), axis=1)

    # Calculate top and bottom RA prices
    df_conpri['TopRAPrice'] = df_conpri.apply(lambda x: calc_ra_price(x['TopDiscRate'], x['techFundPrice'], x['cLength']), axis=1)
    df_conpri['BottomRAPrice'] = df_conpri.apply(lambda x: calc_ra_price(x['BottomDiscRate'], x['techFundPrice'], x['cLength']), axis=1)

    # Total Prepay/POD/Average Costs
    df_conpri = calculate_prepay_pod_avg_cost(df_conpri, FIRST_SPLIT)
    df_conpri = calculate_prepay_pod_avg_cost(df_conpri, SECOND_SPLIT)

    # Calculate Option Years
    for i in range(1, 5):
        df_conpri[f'CashFlow{FIRST_SPLIT}Yr{i}'] = df_conpri.apply(lambda x: calc_cash_flow(x[f'ROFRtoBuyerYr{i}'], i, x['cLength'], x[f'PODPriceYr{i}'], x[f'PODPayment{FIRST_SPLIT}Yr{i}'], x[f'SalesPriceYr{i}'], x[f'firmERYr{i}'], x[f'feeYr{i}'], x[f'prepayAndOptionYr{1}'], ), axis=1)
        df_conpri[f'CashFlow{SECOND_SPLIT}Yr{i}'] = df_conpri.apply(lambda x: calc_cash_flow(x[f'ROFRtoBuyerYr{i}'], i, x['cLength'], x[f'PODPriceYr{i}'], x[f'PODPayment{SECOND_SPLIT}Yr{i}'], x[f'SalesPriceYr{i}'], x[f'firmERYr{i}'], x[f'feeYr{i}'], x[f'prepayAndOptionYr{1}'], ), axis=1)

    print(df_conpri)
    print(df_conpri.columns)    

    # Remember to FIX warnings with lambda functions and DOUBLE CHECK prepar/pod/avg costs function
    # Remember to DROP Unnecessary Columns and SPLIT Columns (They are now hardcoded)
    
if __name__ == "__main__":
    main()
