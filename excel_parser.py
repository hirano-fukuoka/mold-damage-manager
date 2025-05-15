import pandas as pd

def parse_excel(file):
    df = pd.read_excel(file)
    reports = []
    for _, row in df.iterrows():
        reports.append({
            "usage": int(row[0]),
            "part": str(row[1]),
            "damage": str(row[2]),
            "action": str(row[3]),
            "result": str(row[4])
        })
    return reports
