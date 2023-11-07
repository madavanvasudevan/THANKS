import base64
import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

st.title("↑&↓Gene_Plot")
        
st.subheader("Upload a file")

# Define a function that creates a download link for a DataFrame
def download_excel(data):
            excel_file = BytesIO()
            data.to_excel(excel_file,index=True)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
            return href
# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed",key="UP&DOWN")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1dZbmL27Wg6dWfYmpKFJDFqHg6EkNb4yA/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1I3HsN0pvUrluHKl20TDry6TCA5tRA_oj/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
if file is not None:
    try:
        df = pd.read_excel(file)

        # Check if the columns exist in the DataFrame
        if 'GENE_NAME' in df.columns and 'logFC' in df.columns:
            # Select columns by name "gene" and "logfc"
            data = df[['GENE_NAME', 'logFC']].T
            st.write(data)
        else:
            st.write("The 'GENE_NAME' and 'logFC' columns are not present in the DataFrame.")
        # Create a download button
        st.markdown(download_excel(data), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
