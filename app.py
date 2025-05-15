import streamlit as st
from db import init_db, insert_report, search_reports, get_stats, get_all_reports
from report_generator import export_to_excel
from datetime import datetime
import plotly.express as px
import os

st.set_page_config(page_title="連続鋳造モールド損傷管理", layout="wide")
st.title("🛠️ 連続鋳造モールド損傷レポート管理（拡張版）")

init_db()
os.makedirs("uploaded_images", exist_ok=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "✍️ レポート手入力",
    "🔍 データ検索",
    "📊 ダッシュボード",
    "📄 レポート出力"
])

with tab1:
    st.subheader("損傷報告の入力（連続鋳造モールド）")

    today = datetime.now().strftime("%Y-%m-%d")
    st.markdown(f"🗓️ 入力日：**{today}**（自動記録）")

    # 1段目：担当者名、モールド番号、材種
    col1, col2, col3 = st.columns(3)
    with col1:
        user = st.text_input("👤 担当者名", max_chars=30)
    with col2:
        mold_id = st.text_input("🔢 モールド番号")
    with col3:
        material = st.selectbox("鋳造材種", ["炭素鋼", "ステンレス", "特殊鋼", "その他"])

    # 2段目：使用回数、損傷部位、損傷内容
    col4, col5, col6 = st.columns(3)
    with col4:
        usage = st.number_input("使用回数", min_value=0, step=1)
    with col5:
        part = st.selectbox("損傷部位", [
            "銅板表面", "コーナーブロック", "水管部", "突起部", "支持ピン", "バックプレート", "その他"
        ])
    with col6:
        damage = st.selectbox("損傷内容", [
            "摩耗", "割れ", "剥離", "溶損", "目詰まり", "変形", "腐食", "熱疲労クラック"
        ])

    # 3段目：処置内容、結果、画像アップロード
    col7, col8, col9 = st.columns(3)
    with col7:
        action = st.selectbox("処置内容", [
            "グラインダー補修", "肉盛り溶接", "部品交換", "耐熱コーティング", "穴あけ清掃", "表面再加工", "その他"
        ])
    with col8:
        result = st.selectbox("結果", ["成功", "失敗", "再発", "経過観察"])
    with col9:
        image_file = st.file_uploader("📷 損傷写真（任意）", type=["png", "jpg", "jpeg"])

    # 登録ボタン（中央寄せ）
    st.markdown("---")
    if st.button("✅ 登録する", use_container_width=True):
        image_path = ""
        if image_file:
            image_path = os.path.join("uploaded_images", image_file.name)
            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())

        report = {
            "date": today,
            "user": user,
            "mold_id": mold_id,
            "material": material,
            "usage": usage,
            "part": part,
            "damage": damage,
            "action": action,
            "result": result,
            "image_path": image_path
        }
        insert_report(report)
        st.success("✅ レポートが登録されました。")


with tab2:
    keyword = st.text_input("🔍 キーワード検索（損傷内容・処置内容など）")
    if st.button("検索"):
        df = search_reports(keyword)
        if df.empty:
            st.warning("該当するデータがありませんでした。")
        else:
            st.dataframe(df)

with tab3:
    stats = get_stats()
    st.metric("登録件数", stats["total"])
    st.metric("成功数", stats["success"])
    st.metric("成功率", f"{stats['rate']}%")
    if stats["by_action"] is not None and not stats["by_action"].empty:
        fig = px.bar(stats["by_action"], x='action', y='count', title="処置別 登録件数")
        st.plotly_chart(fig)

with tab4:
    if st.button("📥 Excelレポート生成"):
        df = get_all_reports()
        if df.empty:
            st.warning("データがありません。")
        else:
            excel_bytes = export_to_excel(df)
            st.download_button(
                label="レポートをダウンロード",
                data=excel_bytes,
                file_name="mold_damage_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
