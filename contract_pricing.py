from utils.io import *
from utils.calc import *

DB_PATH = "data/risk_model.db"

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

    # Total Prepay Values
    df_conpri['TotalValueOfContract'] = 0
    for i in range(1,11):
        df_conpri['TotalValueOfContract'] += df_conpri[f'firmERYr{i}'] * df_conpri[f'PODPriceYr{i}']    # Drop
    df_conpri['PrepayValueFirstSplit'] = df_conpri['TotalValueOfContract'] * (df_conpri['firstSplit'] / 100)    # Drop
    df_conpri['PrepayValueSecondSplit'] = df_conpri['TotalValueOfContract'] * (df_conpri['secondSplit'] / 100)  # Drop

    # Yearly Costs and Volumes
    df_conpri['CumulativePrepayValueFirstSplit'] = 0    # Drop
    df_conpri['CumulativePrepayValueSecondSplit'] = 0   # Drop

    
    # Remember to drop mid calculation columns

    print(df_conpri)
    print(df_conpri.columns)    

    
if __name__ == "__main__":
    main()
