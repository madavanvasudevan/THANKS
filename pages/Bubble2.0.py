import base64
import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(layout="wide")

# Check if the user is logged in
# if st.session_state.get('logged_in', False):
#     # st.markdown("Welcome to the protected page!")
#     # Display the contents of the protected page

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("image.jpg")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

st.title("Bubble_2.0")
        
st.subheader("Upload your files")

# Define a function that creates a download link for a DataFrame
def download_excel(data):
            excel_file = BytesIO()
            data.to_excel(excel_file, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Bubbles_out.xlsx">Download Excel</a>'
            return href
# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed",key="bubble2.0")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1HKCUiqTlOBpx8BrE60fBoxw9-iCdGDRL/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1YtGlKsGDfmfbL5iDrt6LFMzhl6yiGEUS/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
if file is not None:
    try:
        df = pd.read_excel(file)
        # Assuming you have a dataframe named 'df' with multiple columns
        selected_columns = ['Category', 'Term', 'Count','PValue','Fold Enrichment']
        new_names = ['count', 'enrichment', 'pvalue', 'pathway', 'class']
        df = df[selected_columns].sort_index(axis=1)
        column_name = df.columns
        
        df['class'] = df['Category'].str.extract(r'_(.*?)_')
        df['class'].fillna(df['Category'], inplace=True)
        df['class'].replace({'REACTOME_PATHWAY': 'RC', 'KEGG_PATHWAY': 'KG'}, inplace=True)
        df.drop('Category', axis=1, inplace=True)
        df.columns = new_names

        # Sort the DataFrame by 'count' column in descending order
        data = df.sort_values(by='count', ascending=False)
        # Create a download button
        st.markdown(download_excel(data), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# else:
#     st.markdown("You need to log in to access this page.")
#     # Display a message or redirect the user to the login page
