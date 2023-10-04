import streamlit as st
import pandas as pd
import io
import seaborn as sn
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

class Gene:
    def __init__(self, name=""):
        self.gene_name = name
        self.condition_names = set()

class DataProcessor:
    def __init__(self):
        self.genes = {}
        self.result_df = None

    def read_data(self, file):
        try:
            
            df = pd.read_csv(file, delimiter='\t', header=None, names=['gene_name', 'condition_name'])
            for _, row in df.iterrows():
                gene_name = row['gene_name']
                condition_name = row['condition_name']
                
                gene = self.genes.get(gene_name, Gene(gene_name))
                gene.condition_names.add(condition_name)
                self.genes[gene_name] = gene

        except FileNotFoundError as e:
            st.error("File not found: " + str(e))
            st.stop()

    def do_process(self):
        unique_conditions = sorted(set(condition for gene in self.genes.values() for condition in gene.condition_names))
        combinations = [(c1, c2) for c1 in unique_conditions for c2 in unique_conditions]
        
        combination_freq = {cmb: 0 for cmb in combinations}
        
        for gene in self.genes.values():
            gene_conditions = list(gene.condition_names)
            for combis in combinations:
                if all(condition in gene_conditions for condition in combis):
                    combination_freq[combis] += 1

        # Create a DataFrame for the results
        self.result_df = self.create_result_dataframe(unique_conditions, combination_freq)

        # Print the number of samples
        st.write("Number of Samples:", len(unique_conditions))

        # Display the result DataFrame as a table
        st.dataframe(self.result_df)

    def create_result_dataframe(self, sample_names, combination_freq):
        data = []
        for sample1 in sample_names:
            row = []
            for sample2 in sample_names:
                if sample1 == sample2:
                    # Calculate intersection and subtract union
                    intersection = combination_freq.get((sample1, sample2), 0) - sum(
                        combination_freq.get((sample1, cond), 0) for cond in sample_names if cond != sample1
                    )
                    # Set negative intersection to None (null)
                    if intersection < 0:
                        intersection = None
                    row.append(intersection)
                else:
                    row.append(combination_freq.get((sample1, sample2), 0))
            data.append(row)

        result_df = pd.DataFrame(data, index=sample_names, columns=sample_names)
        return result_df
        
    def download_excel(self):
        if self.result_df is not None:
            # Create a stream to store the Excel data
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                self.result_df.to_excel(writer, index=True, sheet_name='Sheet1')
            output.seek(0)

            # Create a download link for the Excel file
            st.download_button(
                label="Download Excel",
                data=output,
                file_name="Differentiate_Matrix.xlsx",
                key="excel_button",
            )
    def create_corr_matrix_and_plot(self):
        if self.result_df is not None:
            corr_matrix = self.result_df.corr()  # Calculate the correlation matrix
            st.write("Correlation Matrix:")
            st.dataframe(corr_matrix)  # Display the correlation matrix as a table

            # Create a heatmap plot of the correlation matrix
            st.set_option('deprecation.showPyplotGlobalUse', False)
            sn.heatmap(corr_matrix, annot=True)
            plt.title("Correlation Heatmap")
            st.pyplot()  # Display the plot using Streamlit

def main():
    st.title("Differentiate Matrix")

    # File upload widget
    st.subheader("Upload a file")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["txt"], label_visibility="collapsed",key='Differentiate_Matrix')
    st.write("[Sample-Input](https://drive.google.com/file/d/1n2V7E-6quDcVO23Qv6PLC_E7enwtxGZ2/view?usp=sharing)")
    st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1r-_UX5ybnHA1ec_cJtbYtBe9ZmZAYLNo/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")

    if uploaded_file is not None:
        dp = DataProcessor()
        dp.read_data(uploaded_file)
        dp.do_process()
        # Add the Excel download button after processing and displaying the data
        dp.download_excel()
        dp.create_corr_matrix_and_plot()  # Call the new function to create and display the correlation matrix
        
if __name__ == "__main__":
    main()
