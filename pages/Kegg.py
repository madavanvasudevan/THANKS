import re
import pandas as pd
import streamlit as st
import base64
from io import BytesIO

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# # Check if the user is logged in
# if st.session_state.get('logged_in', False):
#     st.markdown("Welcome to the protected page!")

# Define a function to convert an image file to base64
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Convert image to base64 and set it as the background image
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

# Title and file uploader
st.title("KEGG Annotation")
st.subheader("Upload a file")
file3 = st.file_uploader(label="Select a file", type=["txt"], label_visibility="collapsed")

if file3 is not None:
    # Read the uploaded file into a DataFrame
    df = pd.read_csv(file3, header=None,delimiter='None')
    
    # Create an input field for the "map" data
    map_data = st.text_input("Enter map data (e.g., map123): ")

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
    st.title("Data Processing with Streamlit")
    st.write("Processed Data:")
    st.dataframe(df)

# else:
#     st.markdown("You need to log in to access this page.")
#     # Display a message or redirect the user to the login page
