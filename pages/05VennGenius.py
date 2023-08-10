import pandas as pd
import streamlit as st
from venn import venn
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

# Web App Title
st.markdown('''
# **VennGenius**
''')

st.subheader("Upload your files")

# Function to create dataframes for all uploaded files
def create_dataframes(uploaded_files):
    dataframes = {}
    for input_file in uploaded_files:
        # Check if file already exists
        if input_file.name in dataframes:
            st.warning(f"{input_file.name} already exists. Please choose a different file name.")
        else:
            # Load the dataframe from the input file
            df = pd.read_excel(input_file)
            
            # Check if dataframe has 3 columns
            if len(df.columns) != 3:
                st.warning(f"{input_file.name} should have 3 columns.")
            # Check if the first column is text and the other two are numeric
            elif not (df.iloc[:,0].dtype == 'object' and 
                      df.iloc[:,1].dtype == 'float64' and 
                      df.iloc[:,2].dtype == 'float64'):
                st.warning(f"{input_file.name} should have the first column as text and the other two as numeric.")
            else:
                # Do something with the dataframe
                st.success(f"{input_file.name} uploaded successfully!")
                
                # Use file name as dataframe name
                dataframes[input_file.name] = df
    return dataframes

# Main Streamlit app code
uploaded_files = st.file_uploader(
    label="hi",
    type="xlsx",
    label_visibility="collapsed",
    accept_multiple_files=True,
    key="VennGenius"
)
st.write("User can input up-to 6 files but the file should be in the format of sample input")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1BJcJ2djLZTbQv-yA0UFJHbsIvZclc8FW/edit?usp=share_link&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://drive.google.com/file/d/1WG5--ruEnO44GAUgvwlhEyDM0S8tgFUY/view?usp=share_link)")

if uploaded_files is not None:
    # Call the create_dataframes function to create dataframes for all uploaded files
    dataframes = create_dataframes(uploaded_files)
    st.write(f"Created {len(dataframes)} dataframes from uploaded files:")
    
    # Create dictionaries to store the up and down dataframes for each file
    up_dfs = {}
    down_dfs = {}
    
with st.form(key='input_form'):    
    # Ask the user for input
    logFC_upregulator = st.number_input("Select the uplogFC threshold value:", key='logFC_upinput', min_value=0.0, step=0.1)
    logFC_downregulator = st.number_input("Select the downlogFC threshold value:", key='logFC_downinput', min_value=-1e6, max_value=-0.1, step=-0.1, value=-0.1)
    
    # Add a submit button
    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        for df_name, df in dataframes.items():
            # Remove file extension from dataframe name
            df_name_clean = df_name.split('.')[0]
            
            # Create two sub-dataframes based on the values in column 'logFC'
            df_up = df[df['logFC'] >= logFC_upregulator]
            df_down = df[df['logFC'] <= logFC_downregulator]    
            # Store the sub-dataframes in the dictionaries
            up_dfs[df_name_clean] = df_up
            down_dfs[df_name_clean] = df_down
    
    # Convert sub-dataframes to sets
    if len(up_dfs) > 0 and len(down_dfs) > 0:
        up_sets = {name: set(df.iloc[:, 0].tolist()) for name, df in up_dfs.items()}
        down_sets = {name: set(df.iloc[:, 0].tolist()) for name, df in down_dfs.items()}
        
        # # Display the sets of gene names for the up-regulated and down-regulated genes
        # st.write("Up-regulated genes:")
        # st.write(up_sets)
        # st.write("Down-regulated genes:")
        # st.write(down_sets)
            
        # Create a Streamlit app
        st.title("Venn Diagram")
        font_size = st.slider("Select font size:", 6, 16, 10)
        # Display the venn diagram
        fig, ax = plt.subplots(figsize=(12,12))
        venn(up_sets, ax=ax, legend_loc="upper left", fontsize = font_size)
        ax.set_title("UpRegulated Venn Diagram", fontsize=font_size+4)
        st.pyplot(fig)
            
        # Display the venn diagram
        fig1, ax = plt.subplots(figsize=(12,12))
        venn(down_sets, ax=ax, legend_loc="upper left", fontsize = font_size)
        ax.set_title("DownRegulated Venn Diagram", fontsize=font_size+4)
        st.pyplot(fig1)
