import base64
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode  

st.set_page_config(layout="wide")

@st.cache_data()
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("image.jpg")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

st.title("Filter07")

st.subheader("Upload your files")

# Define a function that creates a download link for a DataFrame
def create_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} CSV file</a>'
    return href

# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1pQP-InV1VBTYVvQaYxak26_5Tm15bKI4/edit?usp=share_link&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://drive.google.com/file/d/1wiWWTo6OK2qy75tnD7WQb6GooGXKWVCq/view?usp=share_link)")
if file is not None:
    df = pd.read_excel(file)
    # Allow the user to select a column to sort by
    sort_columns = st.multiselect("Select columns to sort by:", df.columns)

    # Allow the user to choose the sorting order
    sort_order = st.radio("Select sorting order:", ("Ascending", "Descending"))

    # Sort the DataFrame based on the selected column and sorting order
    if sort_order == "Ascending":
        sorted_df = df.sort_values(by=sort_columns)
    else:
        sorted_df = df.sort_values(by=sort_columns, ascending=False)

    gb = GridOptionsBuilder.from_dataframe(sorted_df)
    gridOptions = gb.build()

    return_mode_value = DataReturnMode.__members__['FILTERED_AND_SORTED']
    update_mode_value = GridUpdateMode.__members__['GRID_CHANGED']

    #Display the grid
    st.header("Streamlit Ag-Grid")

    grid_response = AgGrid(
        sorted_df, 
        gridOptions=gridOptions,
        height=400, 
        data_return_mode=return_mode_value, 
        update_mode=update_mode_value
        )

    sorted_df = grid_response['data']
    selected = grid_response['selected_rows']
    selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')

    # Add a download button to the Streamlit app
    if st.button('Proceed to Download'):
        filename = "filtered_data"
        csv = grid_response['data'].to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} CSV file</a>'
        st.markdown(href, unsafe_allow_html=True) 
