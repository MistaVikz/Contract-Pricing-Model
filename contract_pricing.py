from utils.io import *

DB_PATH = "data/risk_model.db"

def main():
    df_conpri = load_data(DB_PATH)

    print(df_conpri)
    print(df_conpri.info())

if __name__ == "__main__":
    main()
