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

    print(df_conpri)    

    
if __name__ == "__main__":
    main()
