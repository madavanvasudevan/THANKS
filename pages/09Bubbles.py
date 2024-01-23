import base64
import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

st.title("Bubbles")
        
st.subheader("Upload a file")

# Define a function that creates a download link for a DataFrame
def download_excel(data):
            excel_file = BytesIO()
            data.to_excel(excel_file, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Bubbles_out.xlsx">Download Excel</a>'
            return href
# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed",key="bubble")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1YW7njIXQcjdP2RZsjHn2kHlzy5T1PUOO/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/19UxgXCAMp5VPG_M6MT0vOo5cW8_PCjv3PogMTYkBu98/edit?usp=sharing)")
if file is not None:
    try:
        df = pd.read_excel(file)
        st.write(df)
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
        df_sorted = df.sort_values(by='count', ascending=False)
        # Group the sorted DataFrame by 'class' column and get the top 5 rows for each group
        data = df_sorted.groupby('class').head(5)
        st.write(data)
        # Create a download button
        st.markdown(download_excel(data), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

