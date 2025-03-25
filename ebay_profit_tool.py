# ebay_profit_tool.py

import pandas as pd
import streamlit as st
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

selected_columns = [
    'Order creation date',
    'Item ID',
    'Item title',
    'Item price',
    'Quantity',
    'Gross amount',
    'Discount',
    'Order earnings'
]

st.title("eBay Profit Tool")

uploaded_file = st.file_uploader("Upload your eBay CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = df[selected_columns].copy()

    df["Item Cost"] = 0.0
    df["Shipping Material Cost"] = 0.0

    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("Calculate Summary"):
        item_total = edited_df["Item Cost"].sum()
        shipping_total = edited_df["Shipping Material Cost"].sum()
        revenue_total = edited_df["Order earnings"].sum()
        total_costs = item_total + shipping_total
        net_profit = revenue_total - total_costs

        st.subheader("Summary Statistics")
        st.markdown(f"- **Total Revenue**: ${revenue_total:.2f}")
        st.markdown(f"- **Total Item Costs**: ${item_total:.2f}")
        st.markdown(f"- **Total Shipping Material Costs**: ${shipping_total:.2f}")
        st.markdown(f"- **Combined Costs**: ${total_costs:.2f}")
        st.markdown(f"- **Net Profit**: ${net_profit:.2f}")

        # Excel export
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            edited_df.to_excel(writer, index=False, sheet_name='eBay Data')
        st.download_button("Download Excel", output.getvalue(), file_name="ebay_data.xlsx")

        # PDF export
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="eBay Summary Report", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Total Revenue: ${revenue_total:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Item Costs: ${item_total:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Shipping Costs: ${shipping_total:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Costs: ${total_costs:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Net Profit: ${net_profit:.2f}", ln=True)

        pdf_output = BytesIO()
        pdf.output(pdf_output)
        st.download_button("Download PDF", pdf_output.getvalue(), file_name="summary_report.pdf")



