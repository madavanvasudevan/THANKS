import streamlit as st
import pandas as pd
import io
import seaborn as sn
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

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
                file_name="gene_data.xlsx",
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
    st.title("Correlation Matrix")

    # File upload widget
    st.subheader("Upload a file")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["txt"], label_visibility="collapsed")
    st.write("[Sample-Input](https://docs.google.com/spreadsheets/d/1vGKInt4xUTVAx3ioc2HnbtyqSwZYUmT4/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")
    st.write("[Sample-Output](https://docs.google.com/spreadsheets/d/1rvCMP9VUZoCI3b1fVXxQaFqJkpZ_XXU1/edit?usp=sharing&ouid=103232618408666892680&rtpof=true&sd=true)")

    if uploaded_file is not None:
        dp = DataProcessor()
        dp.read_data(uploaded_file)
        dp.do_process()
        dp.create_corr_matrix_and_plot()  # Call the new function to create and display the correlation matrix

if __name__ == "__main__":
    main()
