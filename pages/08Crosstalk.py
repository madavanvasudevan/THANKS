import base64
import pandas as pd
import streamlit as st
import io

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

st.title("Crosstalk")
        
st.subheader("Upload a file")

# Define a function that creates a download link for a DataFrame
def download(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl', mode='xlsx') as writer:
        df.to_excel(writer, index=False)  # Export DataFrame to Excel format
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()  # Encoding the Excel data
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="OUTPUT.xlsx">Download Excel file</a>'
    return href

# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed",key="Crosstalk")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/18eQ_n_lP6VEh56U5fQ6YIqFR7pjRrfax/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1hguFNoZO5CX2Eu0UKwbX53-Kwe1gbEyt/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
if file is not None:
    try:
        df = pd.read_excel(file)

        # Separate values in the "Genes" column and create a new DataFrame with redundant values
        genes_split = df['Genes'].str.split(', ')
        new_df = pd.DataFrame({
            'node 1': genes_split.explode().reset_index(drop=True),
            'interaction': 'regulate',
            'node 2': df['Term'].repeat(genes_split.str.len()).reset_index(drop=True)
        })

        # Filter the DataFrame to keep only redundant values in the 'node1' column
        redundant_df = new_df[new_df.duplicated(subset='node 1', keep=False)]
        st.write(redundant_df)
        # Create a download link
        st.markdown(download(redundant_df), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
