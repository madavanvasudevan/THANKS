import base64
import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(layout="wide")

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("image.jpg")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

st.title("Path")
        
st.subheader("Upload a file")
# Define a function that creates a download link for a DataFrame
def download_excel(result):
            excel_file = BytesIO()
            result.to_excel(excel_file, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
            return href

# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed",key="Path")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1zhFzNnTdWLSFsuK_Ya-2LCdJXPEa8nfK/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1R6L4yFUPpN9eEUGdiedMir90YSbVari0/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")

if file is not None:
    try:
        df = pd.read_excel(file)
        
        # Selecting specific columns
        data = df[['TERM', 'Category','Fold Enrichment']]

        # Renaming the columns
        new = {
            'TERM': 'GOterm',
            'Category': 'Subgroup',
            'Fold Enrichment': 'Enrichment score'
        }

        data = data.rename(columns=new)
        
        data['Subgroup'] = data['Subgroup'].replace({
            r'^GOTERM_BP_DIRECT$': 'Biological process',
            r'^GOTERM_CC_DIRECT$': 'Cellular component',
            r'^GOTERM_MF_DIRECT$': 'Molecular function',
        }, regex=True)
        
        st.write(data)

        # Create a download link
        st.markdown(download_excel(data), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
