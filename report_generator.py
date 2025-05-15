import io
import pandas as pd

def export_to_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Reports")
    return buffer.getvalue()
