import base64
import pandas as pd
import streamlit as st
from io import BytesIO
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

st.title("Heatmap_Plot")
        
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
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed",key="Heatmap")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/18GRS4nCIa0gtWJPO-fRSDVU-y81V1_q_/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1ePqmO6YCP9UYO-cwt-3F7rVm6mkXboQp/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
if file is not None:
    try:
        df = pd.read_excel(file)
        st.write(df)  
        
        # Identify non-numerical columns for Gene Symbol selection
        non_numerical_columns = df.select_dtypes(exclude=['number']).columns.tolist()
        
        # Identify numerical columns for data selection
        numerical_columns = df.select_dtypes(include=['number']).columns.tolist()

        # Column selection
        st.subheader('Column Selection')
        Gene_Symbol = st.selectbox('Select Gene Symbol Column', non_numerical_columns)
        df_columns = st.multiselect('Select Data Columns', numerical_columns)
        
        if Gene_Symbol and df_columns:
            # Set the index to the selected Gene Symbol column
            df.set_index(Gene_Symbol, inplace=True)
            
            # Create a new DataFrame with the selected columns
            new_df = df[df_columns]
            
            # Display the new DataFrame
            st.write(new_df)
            # User inputs for heatmap customization
        st.subheader('Heatmap Customization')
        
        row_cluster = st.checkbox('Row Clustering', value=True)
        col_cluster = st.checkbox('Column Clustering', value=True)
        cmap = st.selectbox('Color Map', ['viridis', 'plasma', 'inferno', 'magma', 'cividis'])
        method = st.selectbox('Clustering Method', ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward'])
        #Streamlit App
        st.title('Heatmap')
        # Button to generate the heatmap
        if st.button('Generate Heatmap'):
            # Create a clustered heatmap using seaborn with user inputs
            fig = sns.clustermap(new_df, cmap=cmap, method=method, figsize=(16, 16), fmt=".2f", cbar_kws={'label': 'Color Scale'}, row_cluster=row_cluster, col_cluster=col_cluster)
            
            # Show the plot in Streamlit
            st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
