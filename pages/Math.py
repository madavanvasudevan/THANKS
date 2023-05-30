import pandas as pd
import numpy as np
import streamlit as st
import base64

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

# Web App Title
st.markdown('''
# **The Math App**
---
''')

st.subheader("Upload a file")

# Create a file uploader using Streamlit
uploaded_file = st.file_uploader(label="hello", type=["xlsx"],label_visibility="collapsed")

st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1TeNzqgGVBdxoAVJeHiWoopngFyut9uUu/edit?usp=share_link&ouid=103232618408666892680&rtpof=true&sd=true)")
st.write("[Sample-Output](https://drive.google.com/file/d/1fmmqgGaZQ-J8OwGyOI3fLsTZMoYrELNR/view?usp=share_link)")

# Show the DataFrame if all columns except the first column are numeric
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Check if all columns except the first column are numeric
    if df.iloc[:, 1:].apply(lambda x: pd.to_numeric(x, errors='coerce').notnull().all()).all():
        st.header('**Input DataFrame**')
        st.write(df)
 
        # Add a button to calculate the minimum values
        if st.button('Calculate Minimum Values'):
            # Calculate the minimum value for each column by the first column
            # Get the list of column names except for the first column
            columns = [col for col in df.columns if col != df.columns[0]]
            # Group the DataFrame by the first column and calculate the minimum value for each column
            results = []
            for col in columns:
                id_groups = df.groupby(df.columns[0])
                min_values = id_groups.min()[col]
                # Combine the results into a single DataFrame
                results_df = pd.DataFrame(min_values)
                results_df.columns = [f"{col}_min"]
                # Add the results for this column to the overall results list
                results.append(results_df)

            # Combine the results for all columns into one DataFrame
            combined_results = pd.concat(results, axis=1)
            st.header('**Minimum Value by the first column**')
            st.write(combined_results)
            
            # Download button for minimum values
            tsv = combined_results.to_csv(index=True, sep='\t')
            b64 = base64.b64encode(tsv.encode()).decode()
            href = f'<a href="data:file/tsv;base64,{b64}" download="minimum_values.tsv">Download TSV file</a>'
            st.markdown(href, unsafe_allow_html=True) 
            
        # Add a button to calculate the maximum values
        if st.button('Calculate Maximum Values'):
            # Calculate the maximum value for each column by the first column
            # Get the list of column names except for the first column
            columns = [col for col in df.columns if col != df.columns[0]]
            # Group the DataFrame by the first column and calculate the maximum value for each column
            results = []
            for col in columns:
                id_groups = df.groupby(df.columns[0])
                max_values = id_groups.max()[col]
                # Combine the results into a single DataFrame
                results_df = pd.DataFrame(max_values)
                results_df.columns = [f"{col}_max"]
                # Add the results for this column to the overall results list
                results.append(results_df)

            # Combine the results for all columns into one DataFrame
            combined_results = pd.concat(results, axis=1)
            st.header('**Maximum Value by the first column**')
            st.write(combined_results)

            # Download button for maximum values
            tsv = combined_results.reset_index().to_csv(index=True, sep='\t')
            b64 = base64.b64encode(tsv.encode()).decode()
            href = f'<a href="data:file/tsv;base64,{b64}" download="maximum_values.tsv">Download TSV file</a>'
            st.markdown(href, unsafe_allow_html=True) 
        
        # Add a button to calculate the sum values
        if st.button('Calculate Sum Values'):
            # Calculate the sum value for each column by the first column
            # Get the list of column names except for the first column
            columns = [col for col in df.columns if col != df.columns[0]]
            # Group the DataFrame by the first column and calculate the sum value for each column
            results = []
            for col in columns:
                id_groups = df.groupby(df.columns[0])
                sum_values = id_groups.sum()[col]
                # Combine the results into a single DataFrame
                results_df = pd.DataFrame(sum_values)
                results_df.columns = [f"{col}_sum"]
                # Add the results for this column to the overall results list
                results.append(results_df)

            # Combine the results for all columns into one DataFrame
            combined_results = pd.concat(results, axis=1)
            st.header('**Sum Value by the first column**')
            st.write(combined_results)

            # Download button for sum values
            tsv = combined_results.reset_index().to_csv(index=True, sep='\t')
            b64 = base64.b64encode(tsv.encode()).decode()
            href = f'<a href="data:file/tsv;base64,{b64}" download="sum_values.tsv">Download TSV file</a>'
            st.markdown(href, unsafe_allow_html=True)
            
        # Add a button to calculate the mean values
        if st.button('Calculate Mean Values'):
            # Calculate the mean value for each column by the first column
            # Get the list of column names except for the first column
            columns = [col for col in df.columns if col != df.columns[0]]
            # Group the DataFrame by the first column and calculate the mean value for each column
            results = []
            for col in columns:
                id_groups = df.groupby(df.columns[0])
                mean_values = id_groups.mean()[col]
                # Combine the results into a single DataFrame
                results_df = pd.DataFrame(mean_values)
                results_df.columns = [f"{col}_mean"]
                # Add the results for this column to the overall results list
                results.append(results_df)

            # Combine the results for all columns into one DataFrame
            combined_results = pd.concat(results, axis=1)
            st.header('**Mean Value by the first column**')
            st.write(combined_results)

            # Download button for mean values
            tsv = combined_results.reset_index().to_csv(index=True, sep='\t')
            b64 = base64.b64encode(tsv.encode()).decode()
            href = f'<a href="data:file/tsv;base64,{b64}" download="mean_values.tsv">Download TSV file</a>'
            st.markdown(href, unsafe_allow_html=True)
            
        # Add a button to calculate the median values
        if st.button('Calculate Median Values'):
            # Calculate the median value for each column by the first column
            # Get the list of column names except for the first column
            columns = [col for col in df.columns if col != df.columns[0]]
            # Group the DataFrame by the first column and calculate the median value for each column
            results = []
            for col in columns:
                id_groups = df.groupby(df.columns[0])
                median_values = id_groups.median()[col]
                # Combine the results into a single DataFrame
                results_df = pd.DataFrame(median_values)
                results_df.columns = [f"{col}_median"]
                # Add the results for this column to the overall results list
                results.append(results_df)

            # Combine the results for all columns into one DataFrame
            combined_results = pd.concat(results, axis=1)
            st.header('**Median Value by the first column**')
            st.write(combined_results)

            # Download button for median values
            tsv = combined_results.reset_index().to_csv(index=True, sep='\t')
            b64 = base64.b64encode(tsv.encode()).decode()
            href = f'<a href="data:file/tsv;base64,{b64}" download="median_values.tsv">Download TSV file</a>'
            st.markdown(href, unsafe_allow_html=True)
            
        # Add a button to calculate the mode values
        if st.button('Calculate Mode Values'):
            # Calculate the mode value for each column by the first column
            # Get the list of column names except for the first column
            columns = [col for col in df.columns if col != df.columns[0]]
            # Group the DataFrame by the first column and calculate the mode value for each column
            results = []
            for col in columns:
                id_groups = df.groupby(df.columns[0])
                mode_values = id_groups[col].apply(lambda x: x.mode()[0])
                # Combine the results into a single DataFrame
                results_df = pd.DataFrame(mode_values)
                results_df.columns = [f"{col}_mode"]
                # Add the results for this column to the overall results list
                results.append(results_df)

            # Combine the results for all columns into one DataFrame
            combined_results = pd.concat(results, axis=1)
            st.header('**Mode Value by the first column**')
            st.write(combined_results)

            # Download button for mode values
            tsv = combined_results.reset_index().to_csv(index=True, sep='\t')
            b64 = base64.b64encode(tsv.encode()).decode()
            href = f'<a href="data:file/tsv;base64,{b64}" download="mode_values.tsv">Download TSV file</a>'
            st.markdown(href, unsafe_allow_html=True)
            
        # Add a button to calculate the percentile 50 values
        if st.button('Calculate Percentile 50 Values'):
            # Calculate the percentile 50 value for each column by the first column
            # Get the list of column names except for the first column
            columns = [col for col in df.columns if col != df.columns[0]]
            # Group the DataFrame by the first column and calculate the percentile 50 value for each column
            results = []
            for col in columns:
                id_groups = df.groupby(df.columns[0])
                percentile_50_values = id_groups.quantile(0.5)[col]
                # Combine the results into a single DataFrame
                results_df = pd.DataFrame(percentile_50_values)
                results_df.columns = [f"{col}_percentile_50"]
                # Add the results for this column to the overall results list
                results.append(results_df)

            # Combine the results for all columns into one DataFrame
            combined_results = pd.concat(results, axis=1)
            st.header('**Percentile 50 Value by the first column**')
            st.write(combined_results)

            # Download button for percentile 50 values
            tsv = combined_results.reset_index().to_csv(index=True, sep='\t')
            b64 = base64.b64encode(tsv.encode()).decode()
            href = f'<a href="data:file/tsv;base64,{b64}" download="percentile_50_values.tsv">Download TSV file</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        # Add a button to calculate the 75th percentile values
        if st.button('Calculate 75th Percentile Values'):
            # Calculate the 75th percentile value for each column by the first column
            # Get the list of column names except for the first column
            columns = [col for col in df.columns if col != df.columns[0]]
            # Group the DataFrame by the first column and calculate the 75th percentile value for each column
            results = []
            for col in columns:
                id_groups = df.groupby(df.columns[0])
                percentile75_values = id_groups.quantile(0.75)[col]
                # Combine the results into a single DataFrame
                results_df = pd.DataFrame(percentile75_values)
                results_df.columns = [f"{col}_75th_percentile"]
                # Add the results for this column to the overall results list
                results.append(results_df)

            # Combine the results for all columns into one DataFrame
            combined_results = pd.concat(results, axis=1)
            st.header('**75th Percentile Value by the first column**')
            st.write(combined_results)

            # Download button for 75th percentile values
            tsv = combined_results.reset_index().to_csv(index=True, sep='\t')
            b64 = base64.b64encode(tsv.encode()).decode()
            href = f'<a href="data:file/tsv;base64,{b64}" download="75th_percentile_values.tsv">Download TSV file</a>'
            st.markdown(href, unsafe_allow_html=True)

else: 
    st.info('Awaiting for CSV file to be uploaded.')
