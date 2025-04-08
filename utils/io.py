import sqlite3
import pandas as pd

q_load_data = '''SELECT ConPri.*, ConPriAssumptions.*, Project.pID AS simulationName, Project.offYr1, Project.offYr2, Project.offYr3,
    Project.offYr4, Project.offYr5, Project.offYr6, Project.offYr7, Project.offYr8, Project.offYr9, 
    Project.offYr10, Project.ovRating FROM Conpri
    LEFT JOIN ConPriAssumptions ON ConPri.aChoice = ConPriAssumptions.aID
    LEFT JOIN Project ON ConPri.prunID = Project.ID;'''

def load_data(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    
    df = pd.read_sql_query(q_load_data, conn)
    df = df.drop(columns=['prunID','aChoice','aID'], axis=1, errors='ignore')

    conn.close()

    return df