import re
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
background-attachment: local;
}}
[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
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

st.title("kegg annotation")
    
st.subheader("Upload a file")

# Create a file uploader using Streamlit
file3 = st.file_uploader(" ", type=["txt"])

if file3 is not None:
    # Read the uploaded file into a DataFrame
    df = pd.read_csv(file3, header=None)

    # Extract the "map" data from the first column and create a new column
    df['Map'] = df.iloc[:, 0].str.extract(r'(map\d+ .+?)(?=\s*\()')
    df['Map'].fillna(method='ffill', inplace=True)

    # Create a boolean mask based on regex pattern match in first column
    mask = df.iloc[:, 0].str.extract(r'(map\d+ .+)').notna().squeeze()

    # Use boolean mask to select rows to be deleted and drop them
    df.drop(df[mask].index, inplace=True)
    
    # Drop rows with missing values in the 'Map' column
    df.dropna(subset=[0], inplace=True)

    # Create a download button
    def download_excel(data):
        excel_file = BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        b64 = base64.b64encode(excel_file.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
        return href

    # Display the download button
    st.markdown(download_excel(df), unsafe_allow_html=True)

    # Create a Streamlit app
    def app():
        st.title("Data Processing with Streamlit")
        
        # Display the processed data in a table
        st.write("Processed Data:")
        st.dataframe(df)

    if __name__ == '__main__':
        app()