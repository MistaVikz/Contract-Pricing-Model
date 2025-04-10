from utils.io import *
from utils.calc import *

DB_PATH = "data/risk_model.db"

def main():
    df_merge = load_data(DB_PATH)

    print(df_merge)
    print(df_merge.info())


if __name__ == "__main__":
    main()
