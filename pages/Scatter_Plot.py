import base64
import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

st.title("Scatter_Plot")
        
st.subheader("Upload a file")

# Define a function that creates a download link for a DataFrame
def download_excel(data):
            excel_file = BytesIO()
            data.to_excel(excel_file, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
            return href
# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed",key="Scatter")
st.write('Users can use this app to plot scatter, m6a scatter,quadrant scatter, upset_r')
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1OcfdHNd2rQHpu93b0dkh21rEfcIqGoej/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1lj463Ev7cV0MQ9qC9-tla8y2xULSwj2k/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
if file is not None:
    try:
        df = pd.read_excel(file)
        # Get user input for selecting a specific column
        column_options = list(df.columns)
        selected_column = st.selectbox("Select the Gene_column", column_options)
        
        n = st.number_input("Enter a number of columns need to download", min_value=1, max_value=len(df.columns)//2, step=1, value=3)
        selected_columns = list(range(2, (2*n)+2, 2))
        
        d = df.iloc[:, selected_columns]
        
        # Get user input for selecting specific columns from DataFrame d
        selected_d_columns = st.multiselect("Select columns to filter:", d.columns)
        
        # Create the final DataFrame data by combining the selected gene column with the chosen columns from d
        data = df[[selected_column] + selected_d_columns]
        
        st.write(data)
        # Create a download button
        st.markdown(download_excel(data), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

