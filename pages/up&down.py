import base64
import pandas as pd
import streamlit as st
from io import BytesIO
import plotly.graph_objects as go

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

st.title("GeneUp&Down")
        
st.subheader("Upload your files")

# Define a function that creates a download link for a DataFrame
def download_excel(data):
            excel_file = BytesIO()
            data.to_excel(excel_file,index=True)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
            return href
# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed")
# st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1pQP-InV1VBTYVvQaYxak26_5Tm15bKI4/edit?usp=share_link&ouid=103232618408666892680&rtpof=true&sd=true)")
# st.write("[Sample-Output](https://drive.google.com/file/d/1wiWWTo6OK2qy75tnD7WQb6GooGXKWVCq/view?usp=share_link)")
if file is not None:
    try:
        df = pd.read_excel(file)
        gene = st.selectbox('Select Gene Name Column', [''] + list(df.columns))
        Logfc = st.selectbox('Select Logfc Change Column', [''] + list(df.columns))
        if gene == '' or Logfc == '':
            st.error("Please select values for Gene Name Column, Logfc Column.")
        else:
            data = df[[gene, Logfc]].copy()  # Ensure that you create a copy of the DataFrame
            data.loc[:, Logfc] = pd.to_numeric(data[Logfc])
            column_names = data.columns.tolist()
            # Extract labels from the first column
            labels = data.iloc[:, 0].tolist()
            
            # Create a download button
            st.markdown(download_excel(data), unsafe_allow_html=True)
                
            st.write(data)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
# Create a bar plot using Plotly
fig = go.Figure()

# Add bars to the plot
fig.add_trace(go.Bar(x=labels, y=data[Logfc], marker_color=['green' if fc > 0 else 'red' for fc in data[Logfc]]))

# Add a horizontal line at y=0 for reference
fig.add_shape(type="line", x0=0, y0=0, x1=len(labels), y1=0, line=dict(color="black", width=0.8, dash="dash"))

# Update layout
fig.update_layout(title='Gene Fold Change Bar Plot', xaxis_title='Genes', yaxis_title='Fold Change', bargap=0.1)

# Adjust the position of gene labels based on fold change
for i, (gene, fold_change) in enumerate(zip(labels, data[Logfc])):
    fold_change = float(fold_change)  # Convert fold_change to float
    if fold_change > 0:
        fig.add_annotation(text=gene, x=i, y=fold_change, showarrow=False, yshift=5, font=dict(color="green"))
    else:
        fig.add_annotation(text=gene, x=i, y=fold_change, showarrow=False, yshift=-5, font=dict(color="red"))

# Display the plot using Streamlit
st.plotly_chart(fig)
# # Show the plot
# plt.show()
#     # Create a bar plot
#     plt.figure(figsize=(10, 6))
#     for i in range(len(column_names)):
#         values = pd.to_numeric(data.iloc[:, i], errors='coerce')  # Convert values to numeric, handling errors
#         color = ['green' if value > 0 else 'red' for value in values]
#         plt.bar(labels, values, width=0.4, color=color, label=column_names[i])

#     # Add labels and title
#     plt.xlabel('Genes')
#     plt.ylabel('Fold Change')
#     plt.title('Gene Fold Change Bar Plot')

#     # Add a horizontal line at y=0 for reference
#     plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)

#     # Add legend
#     plt.legend()

#     # Rotate x-axis labels for better readability
#     plt.xticks(rotation=45, ha='right')

#     # Show the plot
#     st.pyplot(plt) 
# else:
#     st.markdown("You need to log in to access this page.")
#     # Display a message or redirect the user to the login page
