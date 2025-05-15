st.subheader("損傷報告の入力（連続鋳造モールド）")

usage = st.number_input("使用回数", min_value=0, step=1)

part = st.selectbox("損傷部位", [
    "銅板表面",
    "コーナーブロック",
    "水管部",
    "突起部",
    "支持ピン",
    "バックプレート",
    "その他"
])

damage = st.selectbox("損傷内容", [
    "摩耗",
    "割れ",
    "剥離",
    "溶損",
    "目詰まり",
    "変形",
    "腐食",
    "熱疲労クラック"
])

action = st.selectbox("処置内容", [
    "グラインダー補修",
    "肉盛り溶接",
    "部品交換",
    "耐熱コーティング",
    "穴あけ清掃",
    "表面再加工",
    "その他"
])

result = st.selectbox("結果", [
    "成功",
    "失敗",
    "再発",
    "経過観察"
])

if st.button("✅ 登録する"):
    report = {
        "usage": usage,
        "part": part,
        "damage": damage,
        "action": action,
        "result": result
    }
    insert_report(report)
    st.success("損傷データを登録しました。")
