import itertools
from collections import defaultdict
import streamlit as st
import os
import base64

st.set_page_config(layout="wide")

# URL of the image from the web
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREh-y7VJtrA03RIlxLNVxt0DUOZyGBXELj1vqaAm_c1kWOW0RUqdP7QrysLqvZ2tSLUVj6acdWlUI&usqp=CAU&ec=48665698"

# Display the image using Streamlit's image function
st.write("<p style='text-align:right;'><img src='"+image_url+"' width=250 height=150></p>",unsafe_allow_html=True)

# Define a Streamlit app title and description
st.title("Network Maker")
st.subheader("Upload your files")
# Function to trigger file download
def download_file(file_path, file_name):
    with open(file_path, "rb") as file:
        file_data = file.read()
    st.download_button(label=f"Download {file_name}", data=file_data, key=file_name)

# Create a file uploader
input_path = st.file_uploader(label="hello",type="txt", label_visibility="collapsed")

if input_path:
    # Define output file paths with ".txt" extension
    output_path_connections = f"{os.path.splitext(input_path.name)[0]}.connections.txt"
    output_path_bridge = f"{os.path.splitext(input_path.name)[0]}.bridge.txt"
    output_path_pathways = f"{os.path.splitext(input_path.name)[0]}.pathways.txt"

    # Create dictionaries to store data
    process_to_genes = defaultdict(list)
    gene_to_processes = defaultdict(list)

    # Read and process the uploaded file
    lines = input_path.read().decode("utf-8").splitlines()
    for line in lines:
        gene, process = line.strip().split("\t")
        process_to_genes[process].append(gene)
        gene_to_processes[gene].append(process)

    # Process and write connections
    with open(output_path_connections, "w") as output_connections:
        for process, genes in process_to_genes.items():
            for gene1, gene2 in itertools.combinations(genes, 2):
                output_connections.write(f"{gene1}\t{process}\t{gene2}\n")

    # Process and write bridges
    with open(output_path_bridge, "w") as output_bridge:
        for gene, processes in gene_to_processes.items():
            if len(processes) > 1:
                for process in processes:
                    output_bridge.write(f"{gene}\tregulate\t{process}\n")

    # Process and write pathways
    with open(output_path_pathways, "w") as output_pathways:
        for process1, genes1 in process_to_genes.items():
            for process2, genes2 in process_to_genes.items():
                if process1 < process2:
                    common_genes = set(genes1) & set(genes2)
                    if common_genes:
                        common_genes_str = " ; ".join(common_genes)
                        output_pathways.write(f"{process1}\tregulation\t{process2}\t{len(common_genes)}\t{common_genes_str}\n")

    # Provide download buttons for the generated files
    st.write("### Generated Files")
    
    download_file(output_path_connections, "connections.txt")
    download_file(output_path_bridge, "bridge.txt")
    download_file(output_path_pathways, "pathways.txt")
