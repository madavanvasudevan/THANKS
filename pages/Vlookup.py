import base64
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("image.jpg")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=175></p>",unsafe_allow_html=True)

st.title("Vlookup")
        
st.subheader("Upload your files")

# Define a function that creates a download link for a DataFrame
def download_csv(data):
    csv = data.to_csv(index=False)  # Added index=False and header=False
    b64 = base64.b64encode(csv.encode()).decode()  # Encoding the CSV data
    href = f'<a href="data:file/csv;base64,{b64}" download="Vlook_output.txt">Download CSV file</a>'
    return href
# Create a file uploader using Streamlit
file = st.file_uploader(label="upload your excel file with gene names/values", type=["xlsx"],key="Vlookup0")
file1 = st.file_uploader(label="upload the main text file", type=["txt"],key="Vlookup1")
st.write("[Sample-Input_Excel](https://docs.google.com/spreadsheets/d/1Dzt9UX5NFOk0dhQOBe53qlVDaGz__SBs/edit?usp=drive_link&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Input_Text](https://drive.google.com/file/d/1GOZRSLbKMj9JEFYxWC5FrvLgWmJyyUtQ/view?usp=sharing)")
st.write("[Sample-Output](https://drive.google.com/file/d/1lfx8c0QWMR5XBVeHaKU2bvwzFPL2k8tb/view?usp=sharing)")
if file1 is not None:
    try:
        df_values = pd.read_excel(file)
        values_list = df_values['GeneSymbol'].tolist()
        
        # Load the .txt file
        df_txt = pd.read_csv(file1, encoding='utf-8', delimiter='\t')
        # Remove everything including and after [ in GeneSymbol column
        df_txt['GeneSymbol'] = df_txt['GeneSymbol'].str.split(r'\s+\[').str[0]

        # Filter the DataFrame based on matching values in the specified column
        data = df_txt[df_txt['GeneSymbol'].isin(values_list)]
        # Create a download button
        st.markdown(download_csv(data), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
