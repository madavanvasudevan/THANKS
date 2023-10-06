import streamlit as st
import pandas as pd
import numpy as np
import base64
from io import BytesIO


st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

# Define a function that creates a download link for a DataFrame
def download_excel(result):
            excel_file = BytesIO()
            result.to_excel(excel_file, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Blog_out.xlsx">Download Excel file</a>'
            return href
    
# Define a Streamlit app
st.title("Blog IT")
st.header("Upload a file")
# Upload Excel file
uploaded_file = st.file_uploader(label="hello",type=["xlsx"],label_visibility="collapsed",key="blog_it")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1Oxj9GT3rNhbNm6ZH-Gl-EiYtMfXvbfHn/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/18P2y2jiKqrBaRCZhMyu-uPhkC80USjwk/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
if uploaded_file is not None:
    # Read the Excel file into a DataFrame
    data = pd.read_excel(uploaded_file)
    data1 = data.copy()

    # Data preprocessing
    data1['Term'] = data1['Term'].str.lower()
    data['Term'] = data['Term'].str.title()
    data['Term_Split'] = data['Term'].str.replace(' ', '')
    data = data.assign(Term=data['Term'].str.split()).explode('Term').reset_index(drop=True)
    data['Term'] = data['Term'].str.lower()

    # Group by Term and calculate counts
    df = data.groupby('Term').size().reset_index(name='Count').sort_values(by='Count', ascending=False)
    df['Log_Count'] = np.log2(df['Count'])
    df = df[(df['Count'] != 1) & (df['Term'].str.len() >= 5)]
    df_list = df['Term'].tolist()

    # Create 'Group' column in data1
    data1['Group'] = ['/ '.join([item for item in df_list if item in term]) for term in data1['Term']]

    # Display the processed DataFrame
    st.write(data1)
    # Create a download link
    st.markdown(download_excel(data1), unsafe_allow_html=True)
