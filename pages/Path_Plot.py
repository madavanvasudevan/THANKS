import base64
import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

st.title("Path_Plot")
        
st.subheader("Upload a file")
# Define a function that creates a download link for a DataFrame
def download_excel(result):
            excel_file = BytesIO()
            result.to_excel(excel_file, index=False)
            excel_file.seek(0)
            b64 = base64.b64encode(excel_file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="output.xlsx">Download Excel file</a>'
            return href

# Create a file uploader using Streamlit
file = st.file_uploader(label="hello", type=["xlsx"], label_visibility="collapsed",key="Path")
st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1zhFzNnTdWLSFsuK_Ya-2LCdJXPEa8nfK/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1R6L4yFUPpN9eEUGdiedMir90YSbVari0/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")


if file is not None:
    try:
        df = pd.read_excel(file)
        
        if df.empty:
            st.warning("Uploaded file is empty.")
        else:
            TERM = st.selectbox('Select TERM Column', [''] + list(df.columns))
            Category = st.selectbox('Select Category Column', [''] + list(df.columns))
            Fold_Enrichment = st.selectbox('Select Fold_Enrichment Column', [''] + list(df.columns))
            if TERM == '' or Category == ''or Fold_Enrichment == '':
                st.error("Please select values for Gene Name Column, Logfc Column.")
            else:
                data = df[[TERM, Category,Fold_Enrichment]].copy()  # Ensure that you create a copy of the DataFrame

                # Renaming the columns
                new = {
                    'TERM': 'GOterm',
                    'Category': 'Subgroup',
                    'Fold Enrichment': 'Enrichment score'
                }

                data = data.rename(columns=new)
                
                data.loc[data['Subgroup'].str.contains('BP|bp'), 'Subgroup'] = 'Biological process'
                data.loc[data['Subgroup'].str.contains('CC|cc'), 'Subgroup'] = 'Cellular component'
                data.loc[data['Subgroup'].str.contains('MF|mf'), 'Subgroup'] = 'Molecular function'

                st.write(data)
                # Create a bar graph using Plotly
                fig = go.Figure()

                subgroups = data['Subgroup'].unique()

                for subgroup in subgroups:
                    subgroup_data = data[data['Subgroup'] == subgroup]
                    fig.add_trace(go.Bar(
                        x=subgroup_data['GOterm'],
                        y=subgroup_data['Enrichment score'],
                        name=subgroup,
                        marker_color=hash(subgroup)  # Assigning a color based on the subgroup name hash
                    ))

                fig.update_layout(
                    title='Enrichment Score by GO Term',
                    xaxis=dict(title='GO Term'),
                    yaxis=dict(title='Enrichment Score'),
                    barmode='group'  # Setting the bar mode to group to separate bars by subgroup
                )

                st.plotly_chart(fig)
        # Create a download link
        st.markdown(download_excel(data), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
