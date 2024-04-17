import base64
import pandas as pd
import streamlit as st
from io import BytesIO
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

st.title("↑&↓Gene_Plot")
        
st.subheader("Upload a file")

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
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1uosww0G-VFF1XNQxWD33HZFAcwmkYv3X/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
if file is not None:
    try:
        df = pd.read_excel(file)
        
        if df.empty:
            st.warning("Uploaded file is empty.")
        else:
            gene = st.selectbox('Select Gene Name Column', [''] + list(df.columns))
            Logfc = st.selectbox('Select Logfc Change Column', [''] + list(df.columns))
            if gene == '' or Logfc == '':
                st.error("Please select values for Gene Name Column, Logfc Column.")
            else:
                data = df[[gene, Logfc]].copy()  # Ensure that you create a copy of the DataFrame
                data.loc[:, Logfc] = pd.to_numeric(data[Logfc])
                column_names = data.columns.tolist()
                fold_changes = data[Logfc].tolist()
                gene_names = data[gene].tolist()
                
                
                # Create a download button
                st.markdown(download_excel(data), unsafe_allow_html=True)
                    
                st.write(data)
                # Split positive fold changes and sort them from small to large
                positive_gene_names, positive_fold_changes = zip(*sorted(
                    [(gene, fc) for gene, fc in zip(gene_names, fold_changes) if fc > 0],
                    key=lambda x: x[1]
                ))

                negative_gene_names, negative_fold_changes = zip(*sorted(
                    [(gene, fc) for gene, fc in zip(gene_names, fold_changes) if fc <= 0],
                    key=lambda x: x[1],
                    reverse=True
                ))

                # Create bars for positive fold changes
                negative_bar = go.Bar(
                    x=list(range(-1, -(len(negative_gene_names) + 1), -1)),
                    y=negative_fold_changes,
                    marker_color='green',
                    text=negative_gene_names,
                    textposition='inside',  # Place gene names inside bars
                )

                # Create bars for negative fold changes
                positive_bar = go.Bar(
                    x=list(range(1, len(positive_gene_names) + 1)),
                    y=positive_fold_changes,
                    marker_color='red',
                    text=positive_gene_names,
                    textposition='inside',  # Place gene names inside bars
                )

                # Create layout
                layout = go.Layout(
                    title='Gene Fold Change Bar Plot',
                    xaxis=dict(title='Genes'),  # x-axis represents genes
                    yaxis=dict(title='Fold Change'),
                )

                # Create figure
                fig = go.Figure(data=[positive_bar, negative_bar], layout=layout)

                # Show the plot
                st.plotly_chart(fig)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
