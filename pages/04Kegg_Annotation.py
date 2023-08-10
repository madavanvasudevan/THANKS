import re
import pandas as pd
import streamlit as st
import base64
from io import BytesIO

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

# Title and file uploader
st.title("KEGG Annotation")
st.subheader("Upload a file")
file3 = st.file_uploader(label="Select a file", type=["txt"], label_visibility="collapsed",key="Kegg")
st.write("[Sample-Input](https://drive.google.com/file/d/14jzsr3Xl6Ekfim1EtWGW5fTDDStSoAvv/view?usp=share_link)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1cUAqGNQXzRswIsrQ5EeyRc68mVQrWJUb/edit?usp=share_link&ouid=103232618408666892680&rtpof=true&sd=true)")

if file3 is not None:
    # Read the uploaded file into a DataFrame
    df = pd.read_csv(file3, header=None,delimiter='None')
    
    # Create an input field for the "map" data
    map_data = st.text_input("Enter map data (e.g., map123): ")
    if map_data:
        # Escape special characters in the user input
        escaped_map_data = re.escape(map_data)

        # Extract the "map" data from the first column and create a new column
        df['Map'] = df.iloc[:, 0].str.extract('(' + escaped_map_data + r'\d+ .+?)(?=\s*\()(?!.*:)')
        df['Map'].fillna(method='ffill', inplace=True)

        # Create a boolean mask based on regex pattern match in first column
        mask = df.iloc[:, 0].str.extract('(' + escaped_map_data + r'\d+ .+)').notna().squeeze()

        # Use boolean mask to select rows to be deleted and drop them
        df.drop(df[mask].index, inplace=True)

        # Drop rows with missing values in the 'Map' column
        df.dropna(subset=[0], inplace=True)

        # Create a function to download the processed data as an Excel file
        def download_excel(data):
            excel_file = BytesIO()
            df.to_excel(excel_file, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
            return href

        # Display the download button for the Excel file
        st.markdown(download_excel(df), unsafe_allow_html=True)

        # Display the processed data in a table
        st.subheader("Data Processing with Streamlit")
        st.write("Processed Data:")
        st.dataframe(df)
