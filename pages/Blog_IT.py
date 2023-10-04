import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

# Define a Streamlit app
st.title("Blog IT")
st.header("Upload a file")
# Upload Excel file
uploaded_file = st.file_uploader(type=["xlsx"],label_visibility="collapsed",key="blog_it")

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

    # Save the processed data to an Excel file
    st.download_button(
        label="Download Processed Data",
        data=data1.to_excel(index=False, header=True),
        file_name="out.xlsx",
        key="processed-data",
    )
