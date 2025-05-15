import pandas as pd

def parse_excel(file):
    # ヘッダーを読み込まず、データとしてすべて読み込む
    df_raw = pd.read_excel(file, header=None)

    # 必要な列が5つ以上ない場合は読み込まない
    if df_raw.shape[1] < 5:
        raise ValueError("Excelの列数が不足しています（少なくとも5列必要）")

    reports = []

    for index, row in df_raw.iterrows():
        try:
            usage = int(row[0])
            part = str(row[1])
            damage = str(row[2])
            action = str(row[3])
            result = str(row[4])
            reports.append({
                "usage": usage,
                "part": part,
                "damage": damage,
                "action": action,
                "result": result
            })
        except Exception:
            # ヘッダー行や不正な行はスキップ
            continue

    return reports
