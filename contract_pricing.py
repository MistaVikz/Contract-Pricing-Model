from utils.io import *
from utils.calc import *

DB_PATH = "data/risk_model.db"

def main():
    df_merge = load_data(DB_PATH)

    # Calculate the yearly firm ER and ROFR to buyer
    for i in range(1, 11):
        df_merge[f'firmERYr{i}'] = df_merge[f'offYr{i}'] * (1 - df_merge['totalShortfall'])
        df_merge[f'ROFRtoBuyerYr{i}'] = df_merge[f'offYr{i}'] - df_merge[f'firmERYr{i}']

    # Calculate Discount on Corporate Contracts
    df_merge['DiscCorpContract'] = df_merge['risklessRate'] + df_merge['spreadAAA'] + df_merge['adjFactor']

    # Something wrong with query
    print(df_merge[['risklessRate', 'spreadAAA', 'adjFactor', 'DiscCorpContract']])
    

if __name__ == "__main__":
    main()
