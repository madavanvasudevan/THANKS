import base64
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

st.title("SNP_Heatmap")
        
st.subheader("Upload your files")

# Define a function that creates a download link for a DataFrame
def download_csv(df):
    csv = df.to_csv(index=False, header=False)  # Added index=False and header=False
    b64 = base64.b64encode(csv.encode()).decode()  # Encoding the CSV data
    href = f'<a href="data:file/csv;base64,{b64}" download="SNP_Heatmap_Values.txt">Download CSV file</a>'
    return href
# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["txt"], label_visibility="collapsed",key="SNP")
st.write("[Sample-Input](https://drive.google.com/file/d/1zE60ETTTy4NB4mIQ1XPRoR8LjWn7JCUx/view?usp=sharing)")
st.write("[Sample-Output](https://drive.google.com/file/d/134t0kvOyzXO_P5YaIRHGS0azdrL6IVyA/view?usp=sharing)")
if file is not None:
    try:
        df = pd.read_csv(file, delimiter='\t')
        # Assuming you have a dataframe named 'df' with multiple columns
        selected_columns = ['Variant_Loci', 'Variant_Allele', 'RSID']
        df = df[selected_columns].sort_index(axis=1)
        column_name = df.columns
        
        df = df.dropna(subset=[column_name[0]]).copy()
        df = df.sort_values(by=[column_name[2], column_name[0]])
        df['variant_loci'] = df[column_name[2]].str.split('-').str[1]
        df = df.drop(column_name[2], axis=1)
        df[column_name[1]] = df[column_name[1]].str.replace('-', '/')

        column_name = df.columns
        delimiter=','
        new_data = df.groupby([column_name[0], column_name[2]], as_index=False).agg({column_name[1]: delimiter.join})
        column_name = new_data.columns

        split_cols = new_data[column_name[2]].str.split(',', expand=True)
        new_data = pd.concat([new_data, split_cols], axis=1).copy()
        new_data = new_data.drop(column_name[2], axis=1)
        transposed_df = new_data.T
        df_filled = transposed_df.fillna("N/A")
        st.write(df_filled)
        # Create a download link
        st.markdown(download_csv(df_filled), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
