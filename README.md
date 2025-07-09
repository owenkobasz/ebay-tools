# 🛠️ eBay Tools

Tools to make life easier as an eBay seller.  
Currently everything is written in Python and can be run locally or on Streamlit.  
Plan migrate them to a unified webpage with Flash/Django down the line.

🌐 First Web App, eBay Profit Tool: [ebay-profit-tool.streamlit.app](https://ebay-profit-tool.streamlit.app/)

---

## eBay Profit Tool Features

- Upload your eBay CSV or Excel export
- Edit item and shipping costs per order
- Get a summary of:
  - Revenue
  - Item costs
  - Shipping material costs
  - Returns
  - Net profit
- Export to:
  - Excel (.xlsx) with full data and added columns
  - PDF summary with date range

---

## Local Setup (via Docker)

1. Clone this repo:

git clone https://github.com/owenkobasz/ebay-tools.git
cd ebay-tools

2. Build the Docker image:

docker build -t ebay-profit-tool .

3. Run the container:

docker run -p 8501:8501 ebay-profit-tool

4. Open your browser and visit:

http://localhost:8501
