import pandas as pd

def parse_excel(file):
    df = pd.read_excel(file)

    # ヘッダー行を自動スキップする場合
    if df.columns[0] != "使用回数":
        df.columns = ["使用回数", "損傷部位", "損傷内容", "処置内容", "結果"]

    reports = []

    for _, row in df.iterrows():
        try:
            reports.append({
                "usage": int(row[0]),
                "part": str(row[1]),
                "damage": str(row[2]),
                "action": str(row[3]),
                "result": str(row[4])
            })
        except Exception:
            # 空白や不正行をスキップ
            continue

    return reports
