import streamlit as st
from db import init_db, insert_report, search_reports, get_stats, get_all_reports
from report_generator import export_to_excel
import plotly.express as px

st.set_page_config(page_title="連続鋳造モールド損傷管理", layout="wide")
st.title("🛠️ 連続鋳造モールド損傷レポート管理システム")

# データベース初期化
init_db()

# タブUI構成
tab1, tab2, tab3, tab4 = st.tabs([
    "✍️ レポート手入力",
    "🔍 データ検索",
    "📊 ダッシュボード",
    "📄 レポート出力"
])

# --------------------------------------
# 📤 レポート手入力
# --------------------------------------
with tab1:
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

# --------------------------------------
# 🔍 データ検索
# --------------------------------------
with tab2:
    st.subheader("🔍 損傷レポートの検索")
    keyword = st.text_input("検索キーワード（損傷内容・処置内容など）")
    if st.button("検索"):
        df = search_reports(keyword)
        if df.empty:
            st.warning("該当するデータが見つかりませんでした。")
        else:
            st.dataframe(df)

# --------------------------------------
# 📊 ダッシュボード
# --------------------------------------
with tab3:
    st.subheader("📈 統計ダッシュボード")

    stats = get_stats()
    st.metric("登録件数", stats["total"])
    st.metric("成功数", stats["success"])
    st.metric("成功率", f"{stats['rate']}%")

    if stats["by_action"] is not None and not stats["by_action"].empty:
        fig = px.bar(stats["by_action"], x='action', y='count', title="処置別 登録件数")
        st.plotly_chart(fig)

# --------------------------------------
# 📄 レポート出力
# --------------------------------------
with tab4:
    st.subheader("📄 レポート出力（Excel形式）")
    if st.button("📥 Excelレポート生成"):
        df = get_all_reports()
        if df.empty:
            st.warning("レポート出力対象のデータがありません。")
        else:
            excel_bytes = export_to_excel(df)
            st.download_button(
                label="レポートをダウンロード",
                data=excel_bytes,
                file_name="mold_damage_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
