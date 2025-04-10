import sqlite3
import pandas as pd

q_load_data = '''SELECT ConPri.*, ConPriAssumptions.*, Project.pID AS simulationName, Project.offYr1, Project.offYr2, Project.offYr3,
    Project.offYr4, Project.offYr5, Project.offYr6, Project.offYr7, Project.offYr8, Project.offYr9, ProjectDescription.cLength, 
    Project.offYr10, Project.ovRating, Project.ovSPRating, Project.totalShortfall FROM Conpri
    LEFT JOIN ConPriAssumptions ON ConPri.aChoice = ConPriAssumptions.aID
    LEFT JOIN Project ON ConPri.prunID = Project.ID
    LEFT JOIN ProjectDescription ON Project.pID = ProjectDescription.pID;'''
q_load_spread = '''SELECT * FROM ConPriSpread;'''

def load_data(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    
    # Load and clean required Contract Pricing data
    df_conpri = pd.read_sql_query(q_load_data, conn)
    df_conpri = df_conpri.drop(columns=['OvRating','prunID','aChoice','aID', 'ovSPRating', 'dateEntered', 'isCurrent'], axis=1, errors='ignore')

    # Load and clean required Contract Pricing Spread data
    df_spread = pd.read_sql_query(q_load_spread, conn)
    
    conn.close()

    return df_conpri, df_spread