import sqlite3
import pandas as pd

q_load_data = '''SELECT ConPri.*, ConPriAssumptions.*, Project.pID AS simulationName, Project.offYr1, Project.offYr2, Project.offYr3,
    Project.offYr4, Project.offYr5, Project.offYr6, Project.offYr7, Project.offYr8, Project.offYr9, 
    Project.offYr10, Project.ovRating, Project.ovSPRating FROM Conpri
    LEFT JOIN ConPriAssumptions ON ConPri.aChoice = ConPriAssumptions.aID
    LEFT JOIN Project ON ConPri.prunID = Project.ID;'''
q_load_spread = '''SELECT * FROM ConPriSpread;'''

def load_data(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    
    # Load and clean required Contract Pricing data
    df_conpri = pd.read_sql_query(q_load_data, conn)
    df_conpri['spreadID'] = df_conpri['spreadChoice'].astype(str) + '-' + df_conpri['ovRating'].astype(str) + '-' + df_conpri['ovSPRating'].astype(str)
    df_conpri = df_conpri.drop(columns=['spreadChoice','OvRating','prunID','aChoice','aID', 'ovSPRating', 'dateEntered', 'isCurrent'], axis=1, errors='ignore')

    # Load and clean required Contract Pricing Spread data
    df_spread = pd.read_sql_query(q_load_spread, conn)
    df_spread['spreadID'] = df_spread['sType'].astype(str) + '-' + df_spread['rating'].astype(str) + '-' + df_spread['spRating'].astype(str)
    df_spread = df_spread.drop(columns=['sType','rating', 'spRating'], axis=1, errors='ignore')

    # Merge the two dataframes on the spreadID
    df_merge = df_conpri.merge(df_spread, on='spreadID', how='left')

    conn.close()

    return df_merge