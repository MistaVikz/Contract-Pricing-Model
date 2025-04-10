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

    print(df_conpri.columns)
    print(df_spread)

if __name__ == "__main__":
    main()
