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

st.title("Heatmap")
        
st.subheader("Upload your files")

# Define a function that creates a download link for a DataFrame
def download_excel(data):
            excel_file = BytesIO()
            data.to_excel(excel_file, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
            return href
# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/18GRS4nCIa0gtWJPO-fRSDVU-y81V1_q_/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1ePqmO6YCP9UYO-cwt-3F7rVm6mkXboQp/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
if file is not None:
    try:
        df = pd.read_excel(file)
        # Get user input for column selection
        column_range = st.text_input("Enter the range of columns (start-end):")

        # Check if the column range is valid
        if column_range:
            try:
                start_column, end_column = map(int, column_range.split('-'))

                if 1 <= start_column <= end_column <= len(df.columns):
                    # Select the columns
                    data = df.iloc[:, start_column - 1 : end_column]
                    data["Gene_Symbol"] = df.iloc[:, 1]
                    st.write(data)
                    # Create a download button
                    st.markdown(download_excel(data), unsafe_allow_html=True)
                else:
                    st.error("Invalid column range. Please enter a valid range.")

            except ValueError:
                st.error("Invalid input format. Please use the format 'start-end' (e.g., 1-3).")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# else:
#     st.markdown("You need to log in to access this page.")
#     # Display a message or redirect the user to the login page
