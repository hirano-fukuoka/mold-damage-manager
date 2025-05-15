import streamlit as st
from excel_parser import parse_excel
from ocr_engine import parse_pdf
from db import init_db, insert_report, search_reports, get_stats, get_all_reports
from report_generator import export_to_excel

st.set_page_config(page_title="モールド損傷管理", layout="wide")
st.title("🛠️ モールド損傷レポート管理システム（Streamlit版）")

init_db()

tab1, tab2, tab3, tab4 = st.tabs(["📤 レポート登録", "🔍 データ検索", "📊 ダッシュボード", "📄 レポート出力"])

with tab1:
    uploaded_file = st.file_uploader("ExcelまたはPDFファイルをアップロード", type=["xlsx", "pdf"])
    if uploaded_file:
        reports = []
        if uploaded_file.name.endswith(".xlsx"):
            reports = parse_excel(uploaded_file)
        else:
            report = parse_pdf(uploaded_file)
            if report:
                reports.append(report)

        for r in reports:
            insert_report(r)
        st.success(f"✅ {len(reports)} 件 登録完了")
        st.json(reports)

with tab2:
    keyword = st.text_input("キーワード検索（損傷・処置内容）")
    if st.button("検索"):
        df = search_reports(keyword)
        st.dataframe(df)

with tab3:
    st.subheader("📈 処置統計")
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
        st.download_button("レポートをダウンロード", data=excel_bytes, file_name="damage_report.xlsx")
