import base64
import pandas as pd
import streamlit as st
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

st.title("Bubble_Plot")
        
st.subheader("Upload a file")

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
# st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1pQP-InV1VBTYVvQaYxak26_5Tm15bKI4/edit?usp=share_link&ouid=103232618408666892680&rtpof=true&sd=true)")
# st.write("[Sample-Output](https://drive.google.com/file/d/1wiWWTo6OK2qy75tnD7WQb6GooGXKWVCq/view?usp=share_link)")

if file is not None:
    try:
        df = pd.read_excel(file)
        st.write(df)
        st.subheader('Column Selection')
        Category = st.selectbox('Select Category Column', [''] + list(df.columns)+['None'])
        Term = st.selectbox('Select Term Column', [''] + list(df.columns))
        Count = st.selectbox('Select Count Column', [''] + list(df.columns))
        PValue = st.selectbox('Select PValue Column', [''] + list(df.columns))
        Fold_Enrichment = st.selectbox('Select Fold_Enrichment Column', [''] + list(df.columns))
        
        
        # Assuming you have a dataframe named 'df' with multiple columns
        # Check if all columns are selected
        if  Term == '' or Count == '' or PValue == '' or Fold_Enrichment == '':
            st.error("Please select values for all the columns.")
        else:
            # Check if 'Category' is not 'None' before proceeding with data manipulation
            if Category == 'None':
                selected_columns = [Term, Count, PValue, Fold_Enrichment]
                selected_df = df[selected_columns].sort_index(axis=1)
            # Create a new DataFrame with selected columns
            else:
                # If 'Category' is 'None', skip data manipulation
                selected_columns = [Category, Term, Count, PValue, Fold_Enrichment]
                selected_df = df[selected_columns].sort_index(axis=1)
                selected_df['class'] = selected_df[Category].str.extract(r'_(.*?)_')
                selected_df['class'].fillna(selected_df[Category], inplace=True)
                selected_df['class'].replace({'REACTOME_PATHWAY': 'RC', 'KEGG_PATHWAY': 'KG'}, inplace=True)
                selected_df.drop(Category, axis=1, inplace=True)
                selected_df = selected_df.groupby('class').head(5)

            # Display the modified DataFrame
            # Sort the DataFrame by 'count' column in descending order
            df_sorted = selected_df.sort_values(by=[Fold_Enrichment], ascending=False)
            df_sorted[PValue] = -np.log10(df_sorted[PValue])            
####            
            st.subheader('Select Color Option')
            Low_color = st.color_picker('Select Low Color', value='#0000FF',key='low_C')
            high_color = st.color_picker('Select high Color', value='#808080',key='high_C')
        
            st.subheader('Selected Plot Text Customise Option')
            Selected_xtext_size = st.number_input('Selected xlabel Text Size', value=12, step=1,key='Selected_x')
            Selected_ytext_size = st.number_input('Selected ylabel Text Size', value=12, step=1,key='Selected_y')
            Selected_ltext_size = st.number_input('Selected legend Text Size', value=12, step=1,key='Selected_l')
            Selected_ttext_size = st.number_input('Selected Tick_params Text Size', value=12, step=1,key='Selected_T')
            st.subheader('Plot Axis Setting')
            x_axis_c = st.slider("Width", min_value=1, max_value=1000, value=15,key='x_axis_c')
            # Customizing the download button based on user preferences
            st.subheader('Plot Display Settings')
            width = st.slider("Width", min_value=1, max_value=100, value=15,key='Width')
            height = st.slider("Height", min_value=1, max_value=100, value=15,key='Height')
            size1 = st.number_input('Selected plotting size', value=80, step=1,key='size1')
            size2 = st.number_input('Selected plotting size', value=400, step=1,key='size2')
            
            aspect = st.slider("grid_plot", min_value=0.0, max_value=5.0, value=0.5, key='aspect')
            
            # Customizing the download button based on user preferences
            st.subheader('Plot download Settings')
            resolution_d = st.slider("Resolution", min_value=100, max_value=1000, value=600, step=50, key='Resolution_d')

####
            # Replace with your p-value column name
            pvalue_column = PValue

            # Number of intervals (adjust based on desired color range)
            num_intervals = 2

            # # Calculate quantiles
            quantiles = np.quantile(df_sorted[pvalue_column], np.linspace(0, 1, num_intervals + 1))
            color_range = [Low_color, high_color]  # Bright red and bright green#change the colour

            # Create bin labels based on quantiles (skip the last quantile)
            bin_labels = [f"[{q:.2f},{quantiles[i+1]:.2f})" for i, q in enumerate(quantiles[:-1])]

            # Assign p-values to bins based on quantiles
            df_sorted['PValue_Range'] = pd.cut(df_sorted[pvalue_column], bins=quantiles, labels=bin_labels, include_lowest=True)
            st.write(df_sorted)
            
            # Create a scatter plot using seaborn and matplotlib
            fig, ax = plt.subplots(figsize=(width, height))#with and height change
            scatter_plot = sns.scatterplot(
                data=df_sorted,
                x=Fold_Enrichment,
                y=Term,
                hue='PValue_Range',
                size=Count,
                palette=color_range,
                sizes=(size1, size2),#change the size
                ax=ax
            )

            # Setting labels and title#font_size to change all sizes
            ax.set_xlabel('Enrichment', fontsize=Selected_xtext_size)
            ax.set_ylabel('Enriched Pathway Name', fontsize=Selected_ytext_size)

            scatter_plot.legend(title='-log10(P-value)', bbox_to_anchor=(1, 1), loc='upper left', fontsize=Selected_ltext_size)
            ax.set_xlim(left=0, right=x_axis_c)

            # Adjust font size for tick labels
            ax.tick_params(axis='both', labelsize=Selected_ttext_size)  # Adjust the font size here


            if 'class' in df_sorted.columns:
                unique_classes = df_sorted['class'].unique()
                if len(unique_classes) > 1:
                    g = sns.FacetGrid(df_sorted, col='class', height=height/2, aspect=aspect)
                    g.map(sns.scatterplot, Fold_Enrichment, Term, 'PValue_Range', palette=color_range)
                    g.set_axis_labels("Enrichment", "Enriched Pathway Name")
                    g.add_legend(title='-log10(P-value)')
                    # Show the plots in Streamlit
                    st.pyplot(g)
                    g.savefig("grid_bubble.png", format="png", dpi=resolution_d,bbox_inches='tight')
                    # Customizing the download button based on user preferences
                    download_button = st.download_button(
                    label="Download grid_bubble Plot",
                    data=open("grid_bubble.png", "rb").read(),
                    file_name="grid_bubble.png",
                    key="grid_bubble_download_button"
                    )

                else:
                    print("Only one class present, cannot facet.")

            # Show the plot in Streamlit
            st.pyplot(fig)
            # Save the plot as a PNG file
            fig.savefig("bubble.png.png", format="png", dpi=resolution_d,bbox_inches='tight')
            
            download_button = st.download_button(
                    label="Download bubble Plot",
                    data=open("bubble.png.png", "rb").read(),
                    file_name="bubble.png.png",
                    key="bubble_download_button"
            )
            
        # Create a download button
        st.markdown(download_excel(df_sorted), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


