import streamlit as st
from db import init_db, insert_report, search_reports, get_stats, get_all_reports
from report_generator import export_to_excel

st.set_page_config(page_title="連続鋳造モールド損傷管理", layout="wide")
st.title("🛠️ 連続鋳造モールド損傷レポート管理システム")

init_db()

tab1, tab2, tab3, tab4 = st.tabs(["✍️ レポート手入力", "🔍 データ検索", "📊 ダッシュボード", "📄 レポート出力"])

with tab1:
    st.subheader("損傷報告の入力")

    usage = st.number_input("使用回数", min_value=0, step=1)
    part = st.selectbox("損傷部位", ["型枠左側", "型枠右側", "抜きピン", "中央スライド", "上面コーナー", "その他"])
    damage = st.text_input("損傷内容（例：ひび割れ、摩耗、変形、欠け）")
    action = st.selectbox("処置内容", ["コーティング変更", "肉盛り溶接", "部品交換", "研磨", "形状修正", "その他"])
    result = st.selectbox("結果", ["成功", "失敗", "経過観察"])

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

with tab2:
    keyword = st.text_input("🔍 キーワード検索（損傷内容・処置内容など）")
    if st.button("検索"):
        df = search_reports(keyword)
        st.dataframe(df)

with tab3:
    st.subheader("📈 統計ダッシュボード")
    stats = get_stats()
    st.metric("登録件数", stats["total"])
    st.metric("成功数", stats["success"])
    st.metric("成功率", f"{stats['rate']}%")

    import plotly.express as px
    if stats["by_action"] is not None:
        fig = px.bar(stats["by_action"], x='action', y='count', title="処置別件数")
        st.plotly_chart(fig)

with tab4:
    if st.button("📥 Excelレポート生成"):
        df = get_all_reports()
        excel_bytes = export_to_excel(df)
        st.download_button("レポートをダウンロード", data=excel_bytes, file_name="mold_damage_report.xlsx")
