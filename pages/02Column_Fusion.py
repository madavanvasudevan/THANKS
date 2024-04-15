import pandas as pd
import streamlit as st
import base64
from io import BytesIO

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

st.title("Column Fusion")
    
st.subheader("Upload a file")

# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["txt","xlsx","csv"], label_visibility="collapsed",key="Fusion")

st.write("[Sample-Input](https://drive.google.com/file/d/16MiqpKw0Fm9j38fWf3TIH2elr3nlE2aP/view?usp=sharing)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1i473hOKzOAW6XICDAImjEIGN8XZ8b8u3/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
   
if file is not None:
    file_format = file.name.split('.')[-1]  # Get the file format
    
    if file_format == "txt":
     df = pd.read_csv(file, delimiter='\t')
    elif file_format == "csv":
     df = pd.read_csv(file, delimiter=',')
    elif file_format == "xlsx":
     df = pd.read_excel(file)
    else:
      st.error("Unsupported file format. Please upload a CSV or Excel file.")
      st.stop()

    # Check for duplicate values in the first column
    duplicate_values = df[df.columns[0]].duplicated()
    if not duplicate_values.any():
        st.error("Error: The first column does not contain duplicate values.")
        st.stop()  
        
    delimiter = st.text_input("Enter the delimiter to split values (e.g., ';'): ")
    # Check if delimiter is non-alphanumeric
    if delimiter and delimiter.isalnum():
        st.error("Error: The delimiter must be a non-alphanumeric character.")
        st.stop()

    delimiter = delimiter if delimiter else '\t'  # Use default delimiter '\t' if not provided

        
    # Get the number of rows in the new DataFrame
    all_rows = df.shape[0]

    # Display the number of rows in the Streamlit app
    st.write("Number of rows: ", all_rows)

    # Convert columns to string type if not already
    df = df.astype(str)

    # Group by the first column and concatenate values in all other columns using the delimiter
    new_data = df.groupby(df.columns[0], as_index=False).agg({col: delimiter.join for col in df.columns[1:]})

    # Display the resulting DataFrame
    st.write(new_data)

    # Get the number of rows in the new DataFrame
    new_rows = new_data.shape[0]

    # Display the number of rows in the Streamlit app
    st.write("Number of rows: ", new_rows)
    
     # Check if new_rows is equal to new_row
    if all_rows == new_rows:
        st.error("Error: Number of rows in the resulting DataFrame is equal to the original number of rows.")
    
    # Create a download button
    def download_excel(df):
        excel_file = BytesIO()
        new_data.to_excel(excel_file, index=False)
        excel_file.seek(0)
        b64 = base64.b64encode(excel_file.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
        return href

    st.markdown(download_excel(new_data), unsafe_allow_html=True)
