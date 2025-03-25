import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="eBay Profit Tool", layout="wide")

st.title("eBay Profit Summary Tool")

uploaded_file = st.file_uploader("Upload your eBay order file (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    filetype = uploaded_file.name.lower().split('.')[-1]

    # Load CSV with automatic header row detection
    if filetype == "csv":
        raw_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        lines = raw_text.splitlines()
        header_row = next((i for i, line in enumerate(lines) if line.startswith("Order creation date")), None)

        if header_row is None:
            st.error("Could not locate the header row. Please check the CSV format.")
            st.stop()

        uploaded_file.seek(0)
        try:
            df = pd.read_csv(uploaded_file, skiprows=header_row, quotechar='"', encoding='utf-8', on_bad_lines='skip')
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            st.stop()

    # Load Excel
    elif filetype == "xlsx":
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
            st.stop()
    else:
        st.error("Unsupported file type.")
        st.stop()

    # Keep a copy of the full dataset
    full_df = df.copy()

    # Default columns to preview
    default_preview_columns = [
        'Item title',
        'Item price',
        'Gross amount',
        'Order earnings'
    ]
    valid_preview_defaults = [col for col in default_preview_columns if col in df.columns]

    st.subheader("Choose Columns to Preview/Edit")
    user_selected_columns = st.multiselect(
        "Select columns to include in the preview table:",
        options=list(df.columns),
        default=valid_preview_defaults
    )

    if not user_selected_columns:
        st.warning("Please select at least one column to preview.")
        st.stop()

    # Editable preview table with cost fields
    editable_df = df[user_selected_columns].copy()
    editable_df["Item Cost"] = 0.0
    editable_df["Shipping Material Cost"] = 0.0

    st.subheader("Enter Item and Shipping Costs")
    edited_df = st.data_editor(editable_df, use_container_width=True, num_rows="dynamic")

    if st.button("Calculate Summary and Export"):
        # Merge cost columns into full dataset
        full_df["Item Cost"] = edited_df["Item Cost"]
        full_df["Shipping Material Cost"] = edited_df["Shipping Material Cost"]

        # Ensure numeric columns
        full_df["Item Cost"] = pd.to_numeric(full_df["Item Cost"], errors="coerce").fillna(0)
        full_df["Shipping Material Cost"] = pd.to_numeric(full_df["Shipping Material Cost"], errors="coerce").fillna(0)

        if "Refunds" in full_df.columns:
            full_df["Refunds"] = pd.to_numeric(full_df["Refunds"].replace("--", None), errors="coerce").fillna(0)
        else:
            full_df["Refunds"] = 0.0

        # Format the date range from the Order creation date column
        if "Order creation date" in full_df.columns:
            try:
                full_df["Order creation date"] = pd.to_datetime(full_df["Order creation date"], errors="coerce")
                valid_dates = full_df["Order creation date"].dropna()
                if not valid_dates.empty:
                    start_date = valid_dates.min().strftime("%Y-%m-%d")
                    end_date = valid_dates.max().strftime("%Y-%m-%d")
                    date_range_str = f"{start_date} to {end_date}"
                    human_range_str = f"({valid_dates.min().strftime('%b %d, %Y')} - {valid_dates.max().strftime('%b %d, %Y')})"

                else:
                    date_range_str = "date_range"
                    human_range_str = ""
            except Exception:
                date_range_str = "date_range"
                human_range_str = ""
        else:
            date_range_str = "date_range"
            human_range_str = ""

        # Calculate totals
        item_total = full_df["Item Cost"].sum()
        shipping_total = full_df["Shipping Material Cost"].sum()
        returns_total = full_df["Refunds"].sum()
        returns_total = -returns_total  # convert to neg
        revenue_total = full_df["Order earnings"].sum() if "Order earnings" in full_df.columns else 0
        total_costs = item_total + shipping_total
        net_profit = revenue_total - total_costs

        # Display summary
        st.subheader(f"Summary Statistics {human_range_str}")
        st.markdown(f"- **Total Revenue**: ${revenue_total:,.2f}")
        st.markdown(f"- **Total Item Costs**: ${item_total:,.2f}")
        st.markdown(f"- **Total Shipping Material Costs**: ${shipping_total:,.2f}")
        st.markdown(f"- **Total Returns**: ${returns_total:,.2f}")
        st.markdown(f"- **Total Combined Costs**: ${total_costs:,.2f}")
        st.markdown(f"- **Net Profit**: ${net_profit:,.2f}")

        # Export to Excel
        xlsx_buffer = BytesIO()
        with pd.ExcelWriter(xlsx_buffer, engine='openpyxl') as writer:
            full_df.to_excel(writer, index=False, sheet_name='eBay Orders with Costs')

        excel_filename = f"ebay_orders_{date_range_str}.xlsx"
        st.download_button("Download Excel File", xlsx_buffer.getvalue(), file_name=excel_filename)

        # Export to PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"eBay Profit Summary {human_range_str}", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Total Revenue: ${revenue_total:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Item Costs: ${item_total:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Shipping Costs: ${shipping_total:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Returns: ${returns_total:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Costs: ${total_costs:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Net Profit: ${net_profit:,.2f}", ln=True)

        pdf_buffer = BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin1')
        pdf_buffer.write(pdf_output)

        pdf_filename = f"ebay_profit_summary_{date_range_str}.pdf"
        st.download_button("Download Summary PDF", pdf_buffer.getvalue(), file_name=pdf_filename)

        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; margin-top: 2em;">
                <a href="https://www.buymeacoffee.com/owenkobasz" target="_blank">
                    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="60">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

