import base64
import numpy as np
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

st.title("Go_path")
        
st.subheader("Upload your files")
# Define a function that creates a download link for a DataFrame
def download_excel(result):
            excel_file = BytesIO()
            result.to_excel(excel_file, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Gopath_out.xlsx">Download Excel file</a>'
            return href
# Function to label values
def label_value(value):
    if value <= -2:
        return "down"
    elif value >= 2:
        return "up"
    else:
        return value
# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed",key="Go_path")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1vGKInt4xUTVAx3ioc2HnbtyqSwZYUmT4/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1rvCMP9VUZoCI3b1fVXxQaFqJkpZ_XXU1/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Example-Plots](https://docs.google.com/spreadsheets/d/1MLteFvllUoiBob-F43xKcJ3GYIT0_9Ob/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")

if file is not None:
    try:
        df = pd.read_excel(file)
        # Apply the function to the 'logFC' column and create a new 'Label' column
        df['Label'] = df['logFC'].apply(label_value)

        # Select the columns needed for further processing
        selected_columns = ['Label', 'BIOCARTA', 'GOTERM_BP_DIRECT', 'GOTERM_CC_DIRECT', 'GOTERM_MF_DIRECT', 'KEGG_PATHWAY', 'REACTOME_PATHWAY', 'WIKIPATHWAYS']
        df1 = df[selected_columns].sort_index(axis=1)

        # Combine values in all rows, skipping the 'Label' column
        delimiter = ','
        df1['GO_Pathway'] = df1.drop('Label', axis=1).apply(lambda x: delimiter.join(x.astype(str)), axis=1)

        # Select the columns needed for the final result
        selected_columns = ['Label', 'GO_Pathway']
        d = df1[selected_columns].sort_index(axis=1)

        # Create an empty DataFrame to store the new data
        new_data = pd.DataFrame(columns=d.columns)

        # Iterate over each row in the DataFrame
        for index, row in d.iterrows():
            # Split values in the 'GO_Pathway' column by the specified delimiter
            split_values = row['GO_Pathway'].split(delimiter)
            
            # Create a new row for each split value, using the 'Label' column as the identifier
            for value in split_values:
                new_row = row.copy()
                new_row['GO_Pathway'] = value.strip()
                new_data = new_data.append(new_row, ignore_index=True)

        # Group by 'GO_Pathway' and count the occurrences of 'up' and 'down' in the 'Label' column
        result = new_data.groupby('GO_Pathway').agg(up_count=('Label', lambda x: (x == 'up').sum()), down_count=('Label', lambda x: (x == 'down').sum())).reset_index()

        # Calculate the total count for each 'GO_Pathway'
        result['total_count'] = result['up_count'] + result['down_count']

        # Replace different types of missing values with NaN
        result['GO_Pathway'].replace(['', 'NaN','nan', None], np.nan, inplace=True)

        # Drop rows with NaN values in the 'Combined' column
        result.dropna(subset=['GO_Pathway'], inplace=True)
        
        result['logFC'] = np.log2(result['up_count'] / result['down_count'])
        
        # Create a download link
        st.markdown(download_excel(result), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# else:
#     st.markdown("You need to log in to access this page.")
#     # Display a message or redirect the user to the login page
