import streamlit as st
import pandas as pd
import numpy as np

# Define a Streamlit app
st.title("Blog_IT")

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

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
