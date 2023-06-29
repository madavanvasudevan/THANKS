import base64
import pandas as pd
import streamlit as st

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

st.title("Bubbles")
        
st.subheader("Upload your files")

# Define a function that creates a download link for a DataFrame
def download_csv(data):
    csv = data.to_csv(index=False, header=False)  # Added index=False and header=False
    b64 = base64.b64encode(csv.encode()).decode()  # Encoding the CSV data
    href = f'<a href="data:file/csv;base64,{b64}" download="Bubbles_out.txt">Download CSV file</a>'
    return href
# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed")
# st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1pQP-InV1VBTYVvQaYxak26_5Tm15bKI4/edit?usp=share_link&ouid=103232618408666892680&rtpof=true&sd=true)")
# st.write("[Sample-Output](https://drive.google.com/file/d/1wiWWTo6OK2qy75tnD7WQb6GooGXKWVCq/view?usp=share_link)")
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
        df_sorted = df.sort_values(by='count', ascending=False)

        # Group the sorted DataFrame by 'class' column and get the top 5 rows for each group
        data = df_sorted.groupby('class').head(5)
        # Create a download link
        st.markdown(download_csv(data), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# else:
#     st.markdown("You need to log in to access this page.")
#     # Display a message or redirect the user to the login page
