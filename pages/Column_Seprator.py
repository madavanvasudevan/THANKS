import pandas as pd
import streamlit as st
import base64
from io import BytesIO

st.set_page_config(layout="wide")

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://southburlingtonlibrary.org/assets/image-cache/Teens/genes%20in%20a%20bottle.5d18602e.jpg");
background-size: 120%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: scroll;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:left;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

st.title("Column Separator")

st.subheader("Upload a file")

# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["txt"], label_visibility="collapsed")

if file is not None:
    data = pd.read_csv(file, delimiter='\t', header=None)

    # Validate number of columns
#     if data.shape[1] != 2:
#         st.error("Error: The file must contain exactly 2 columns.")
#         st.stop()

    # Check for duplicate values in the first column
    duplicate_values = data[data.columns[0]].duplicated()
    if duplicate_values.any():
        st.error("Error: The first column contains redundant data.")
        st.stop()

    delimiter = st.text_input("Enter the delimiter to split values (e.g., ';'): ")
    # Check if delimiter is non-alphanumeric
    if delimiter and delimiter.isalnum():
        st.error("Error: The delimiter must be a non-alphanumeric character.")
        st.stop()

    delimiter = delimiter if delimiter else '\t'  # Use default delimiter '\t' if not provided

    # Create a new DataFrame to store the split values
    new_data = pd.DataFrame(columns=data.columns)
        
    # Get the number of rows in the new DataFrame
    all_rows = data.shape[0]

    # Display the number of rows in the Streamlit app
    st.write("Number of rows: ", all_rows)

    # Iterate through each row in the original DataFrame
    column_names = data.columns
    for index, row in data.iterrows():
        # Split values in second column by the specified delimiter
        split_values = row[column_names[1]].split(delimiter)

        # Create a new row for each split value, using column 1 name as identifier
        for value in split_values:
            new_row = row.copy()
            new_row[column_names[1]] = value.strip()
            new_data = new_data.append(new_row, ignore_index=True)

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
    def download_excel(data):
        excel_file = BytesIO()
        new_data.to_excel(excel_file, index=False)
        excel_file.seek(0)
        b64 = base64.b64encode(excel_file.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
        return href

    st.markdown(download_excel(new_data), unsafe_allow_html=True)
