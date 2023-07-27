import pandas as pd
import streamlit as st
import os
import base64
from io import BytesIO


st.set_page_config(layout="wide")

@st.cache_data()
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("image.jpg")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

# Web App Title
st.markdown('''
# **Venn_mini**
''')

st.subheader("Upload your files")


# Function to create dataframes for all uploaded files
def create_dataframes(uploaded_files):
    dataframes = []
    for input_file in uploaded_files:
        # Check if file already exists
        if any(df.name == input_file.name for df in dataframes):
            st.warning(f"{input_file.name} already exists. Please choose a different file name.")
        else:
            # Load the dataframe from the input file
            df = pd.read_excel(input_file)
            
            # Do something with the dataframe
            st.success(f"{input_file.name} uploaded successfully!")
            
            # Use file name as dataframe name
            df.name = input_file.name
            
            dataframes.append(df)
    return dataframes
# Function to select a single column from all dataframes
def select_column_from_dataframes(dataframes, column_name):
    selected_columns = {}
    for df in dataframes:
        if column_name in df.columns:
            selected_columns[df.name] = df[column_name]
        else:
            st.warning(f"Column '{column_name}' not found in '{df.name}' dataframe.")
    return selected_columns

# Function to download dataframes as a single Excel file
def download_selected_columns_as_excel(selected_columns):
    # Create a Pandas Excel writer using BytesIO to save the file in memory
    output_file = BytesIO()
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        for name, column_data in selected_columns.items():
            column_data.to_excel(writer, sheet_name=name, index=False)
    output_file.seek(0)
    return output_file
# Main Streamlit app code
uploaded_files = st.file_uploader(
    label="hi",
    type="xlsx",
    label_visibility="collapsed",
    accept_multiple_files=True
)
st.write("User Can input up-to 6 files but the file should be in the format of sample input")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1dVtTVpuDgVLeVv4lgvoYH8zMc5Y5AfaQ/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1K0HRInvjFL2_aiK9jRoKTa8Dq43kfFtx/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")

if uploaded_files is not None:
    # Call the create_dataframes function to create dataframes for all uploaded files
    dataframes = create_dataframes(uploaded_files)
    st.write(f"Created {len(dataframes)} dataframes from uploaded files:")
    
    # Get the column name from the user (you can modify this part based on how the user provides the column name)
    column_name = st.text_input("Enter the column name to select:")
    
    if column_name:
            # Call the select_column_from_dataframes function to select the desired column from all dataframes
            selected_columns = select_column_from_dataframes(dataframes, column_name)
            
            if selected_columns:
                st.write("Selected columns:")
                for name, column_data in selected_columns.items():
                    st.write(f"DataFrame: {name}")
                    st.write(column_data)
                
                # Add a download button to download the selected columns as a single Excel file
                download_button = st.button("Download Selected Columns as Excel")
                if download_button:
                    output_file = download_selected_columns_as_excel(selected_columns)
                    st.download_button(
                        label="Click here to download",
                        data=output_file,
                        file_name="selected_columns.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.warning(f"No data found for column '{column_name}'.")
