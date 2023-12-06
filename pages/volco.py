import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Function to read and process the uploaded file
def process_uploaded_file(uploaded_file):
    data = pd.read_csv(uploaded_file)

    # Check if the dataframe has at least three columns
    if len(data.columns) < 3:
        raise ValueError("The uploaded file must have at least three columns.")

    return data
#Counting the size from the y_axis_fixed_value
def calculate_marker_size(y_value, y_axis_fixed_value, y_axis_fixed_value_size, default_size):
    if y_axis_fixed_value == 0:
        return default_size

    if y_value > y_axis_fixed_value:
        # Calculate the proportional increase in size based on the difference
        size_increase_factor = (y_value - y_axis_fixed_value) / y_axis_fixed_value
        return y_axis_fixed_value_size + size_increase_factor * default_size
    else:
        return default_size


def generate_volcano_plot(data, gene_column, fold_change_column, p_value_column,
                           p_value_threshold=0.05,up_threshold=0.5,down_threshold=0.5,y_axis_fixed_value_size=15,
                           x_axis_range=(-10, 10), y_axis_range=(0, 5),y_axis_fixed_value=1000,
                           up_color='#FF0000', down_color='#0000FF', none_color='#808080'):
    data['-log10(PValue)'] = -np.log10(data[p_value_column])  # Calculate -log10(p-value)
    significance_threshold = -np.log10(p_value_threshold)  # Significance threshold

    # Define segments based on fold change and p-value values
    data['Segment'] = np.where((data[fold_change_column] > up_threshold) & (data[p_value_column] < p_value_threshold), 'Up',
                               np.where((data[fold_change_column] < down_threshold) & (data[p_value_column] < p_value_threshold), 'Down', 'None'))
    # Add 'Selected' segment based on provided selected genes
    if selected_genes is not None:
        data.loc[data[gene_column].isin(selected_genes), 'Segment'] = 'Selected'

    data['Color'] = np.select(
    [
        (data['Segment'] == 'Selected') & (data[fold_change_column] > up_threshold) & (data[p_value_column] < p_value_threshold),
        (data['Segment'] == 'Selected') & (data[fold_change_column] < down_threshold) & (data[p_value_column] < p_value_threshold),
        (data['Segment'] == 'Selected'),
        (data['Segment'] == 'Up'),
        (data['Segment'] == 'Down'),
    ],
    [up_color, down_color, none_color, up_color, down_color],
    default=none_color
    )
    # Create separate traces for 'Up', 'Down', 'None', and 'Selected'
    trace_up = data[data['Segment'] == 'Up']
    trace_down = data[data['Segment'] == 'Down']
    trace_none = data[data['Segment'] == 'None']
    trace_selected = data[data['Segment'] == 'Selected']
    
    # Create the volcano plot
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[x_axis_range[0], x_axis_range[1]],
        y=[significance_threshold, significance_threshold],
        mode='lines',
        line=dict(color='red', dash='dot'),
        name='Significance Threshold'
    ))

    # Define marker properties for each trace type
    marker_properties = {
        'Up': dict(symbol=Up_marker_symbol, size=Up_marker_size, color=up_color),
        'Down': dict(symbol=Down_marker_symbol, size=Down_marker_size, color=down_color),
        'None': dict(symbol=None_marker_symbol, size=None_marker_size, color=none_color),
        'Selected': dict(symbol=Selected_marker_symbol, size=Selected_marker_size)
    }
    # Update marker properties for 'Selected' segment based on conditions
    selected_data = data[data['Segment'] == 'Selected']
    selected_marker_symbols = np.select(
        [
            (selected_data[fold_change_column] > up_threshold) & (selected_data[p_value_column] < p_value_threshold),
            (selected_data[fold_change_column] < down_threshold) & (selected_data[p_value_column] < p_value_threshold),
        ],
        [Up_marker_symbol, Down_marker_symbol],
        default=None_marker_symbol
    )
    # Check if the selected marker symbol is not 'None' and execute something
    if Selected_marker_symbol is None:
        # Update 'Selected' segment properties in the dictionary
        marker_properties['Selected']['symbol'] = selected_marker_symbols
    else:
        pass
# Loop through each trace type and add the corresponding trace to the figure
    for trace_type, properties in marker_properties.items():
        trace_data = data[data['Segment'] == trace_type]
        if not trace_data.empty:
            # Calculate marker sizes for each data point
            marker_sizes = [
                calculate_marker_size(y_value, y_axis_fixed_value, y_axis_fixed_value_size, properties['size'])
                for y_value in trace_data['-log10(PValue)']
            ]

            fig.add_trace(go.Scatter(
                x=trace_data[fold_change_column],
                y=-np.log10(trace_data[p_value_column]),
                mode='markers',
                marker=dict(symbol=properties['symbol'], size=marker_sizes, color=trace_data['Color']),
                text=trace_data[gene_column],
                name=trace_type
            ))

    # Draw lines between markers and text labels
    annotations = []
    for i in range(len(trace_selected)):
        annotation = dict(
            x=trace_selected[fold_change_column].iloc[i],
            y=-np.log10(trace_selected[p_value_column]).iloc[i],
            xref='x',
            yref='y',
            text=trace_selected[gene_column].iloc[i],
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='black',
            font=dict(size=Selected_text_size)  # Set the desired text size (adjust the value as needed)

        )
        annotations.append(annotation)

    # Add a dark black outline around the plot
    fig.update_layout(
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color='black', width=2),
            )
        ]
    )
    fig.update_layout(
        title='Enhanced Volcano Plot',
        xaxis_title='Log Fold Change',
        yaxis_title='-log10(P-Value)',
        xaxis=dict(range=x_axis_range),
        yaxis=dict(range=y_axis_range),
        annotations=annotations
    )
    fig.update_layout(width=width, height=height)

    return fig

if __name__ == '__main__':
    st.title('Enhanced Volcano Plot')

    # File Upload
    uploaded_file = st.file_uploader("Upload file", type=['csv', 'tsv'])
    
    if uploaded_file is not None:
        data = process_uploaded_file(uploaded_file)
        st.write(data)
        st.subheader('Column Selection')

        # Add default option to each select box
        gene_column = st.selectbox('Select Gene Name Column', [''] + list(data.columns))
        fold_change_column = st.selectbox('Select Fold Change Column', [''] + list(data.columns))
        p_value_column = st.selectbox('Select p-value Column', [''] + list(data.columns))
        if gene_column == '' or fold_change_column == '' or p_value_column == '':
            st.error("Please select values for Gene Name Column, Fold Change Column, and p-value Column.")
        else:
            # Get input from the user for selected genes
            selected_genes_input = st.text_input("Enter a comma-separated list of selected genes (e.g., Gene1, Gene2, Gene3): ",key='Select_Gene')
            selected_genes = [gene.strip() for gene in selected_genes_input.split(',')]
            

            # Add sliders for x and y axis ranges
            st.subheader('Axis Range Selection')
            x_axis_range = st.slider('X-Axis Range', min_value=-15, max_value=15, value=(-10, 10),key='x_axis')
            y_axis_range = st.slider('Y-Axis Range', min_value=0, max_value=10, value=(0, 5),key='y_axis')

            st.subheader('p_value')
            p_value_threshold = st.number_input('Enter the p_value_threshold value:', value=0.05, step=0.5,key='p_value')
            
            st.subheader('Log2FC')
            threshold = st.number_input("Enter the fold change threshold:", value=0.1, step=0.01, min_value=0.0,key='Log2FC')

            # Set both positive and negative thresholds to the same value
            up_threshold = threshold
            down_threshold = -threshold

            #Option list
            options_list = [
                'circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down',
                'triangle-left', 'triangle-right', 'pentagon', 'hexagram', 'star', 'hourglass',
                'bowtie', 'circle-open', 'square-open','diamond-open', 'cross-open', 'x-open', 
                'triangle-up-open', 'triangle-down-open','triangle-left-open', 'triangle-right-open',
                'pentagon-open', 'hexagram-open','star-open', 'hourglass-open', 'bowtie-open', 'asterisk-open',
                'hash-open', 'circle-dot', 'square-dot', 'diamond-dot', 'cross-dot', 'x-dot', 'triangle-up-dot',
                'triangle-down-dot','triangle-left-dot', 'triangle-right-dot', 'pentagon-dot','hexagram-dot', 'star-dot'
            ]
            options_list1 = [None,
                'circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down',
                'triangle-left', 'triangle-right', 'pentagon', 'hexagram', 'star', 'hourglass',
                'bowtie', 'circle-open', 'square-open','diamond-open', 'cross-open', 'x-open', 
                'triangle-up-open', 'triangle-down-open','triangle-left-open', 'triangle-right-open',
                'pentagon-open', 'hexagram-open','star-open', 'hourglass-open', 'bowtie-open', 'asterisk-open',
                'hash-open', 'circle-dot', 'square-dot', 'diamond-dot', 'cross-dot', 'x-dot', 'triangle-up-dot',
                'triangle-down-dot','triangle-left-dot', 'triangle-right-dot', 'pentagon-dot','hexagram-dot', 'star-dot'
            ]
    
            # Color selection options
            st.subheader('UP Customize Option')
            up_color = st.color_picker('Select Color', value='#FF0000',key='Up_C')     
            Up_marker_symbol = st.selectbox('Select Shape',options_list, key='Up')
            Up_marker_size = st.slider('Select Marker Size', min_value=1, max_value=20, value=12,key='Up_S')
            
            st.subheader('Down Customize Option')
            down_color = st.color_picker('Select Color', value='#0000FF',key='Down_C')
            Down_marker_symbol = st.selectbox('Select Shape',options_list, key='Down')
            Down_marker_size = st.slider('Select Marker Size', min_value=1, max_value=20, value=12,key='Down_S')

            st.subheader('None Customize Option')
            none_color = st.color_picker('Select Color', value='#808080',key='None_C')
            None_marker_symbol = st.selectbox('Select Shape',options_list, key='None')
            None_marker_size = st.slider('Select Marker Size', min_value=1, max_value=20, value=12,key='None_S')
            
            st.subheader('Selected Gene Customize Option')
            Selected_marker_symbol = st.selectbox('Selected Gene Shape',options_list1, key='Selected')
            Selected_marker_size = st.slider('Selected Gene Marker Size', min_value=1, max_value=20, value=12,key='Selected_S')
            Selected_text_size = st.number_input('Selected Gene Text Size', value=15, step=1,key='Selected_T')

            st.subheader('Selected Yaxis customize Option')
            # User input for y_axis_fixed_value
            y_axis_fixed_value = st.number_input('Enter the fixed y-axis value:', step=1,key='y_axis_C')

            # User input for y_axis_fixed_value_size
            y_axis_fixed_value_size = st.number_input('Enter the marker size for values crossing the fixed y-axis:', value=15, step=1,key='y_axis_S')    
                        
            # Customizing the download button based on user preferences
            st.subheader('Plot Display Settings')
            width = st.slider("Width", min_value=100, max_value=2000, value=800,key='Width')
            height = st.slider("Height", min_value=100, max_value=2000, value=600,key='Height')
            resolution = st.slider("Resolution", min_value=1.0, max_value=5.0, value=2.0,key='Resolution')

            # Add a button to trigger volcano plot generation
            if st.button('Generate Volcano Plot'):
                st.subheader('Volcano Plot')
                volcano_plot = generate_volcano_plot(data, gene_column, fold_change_column, p_value_column,
                                     p_value_threshold=p_value_threshold, x_axis_range=x_axis_range, y_axis_range=y_axis_range,
                                     up_color=up_color, down_color=down_color, none_color=none_color,up_threshold=up_threshold,
                                     down_threshold=down_threshold,y_axis_fixed_value=y_axis_fixed_value, y_axis_fixed_value_size=y_axis_fixed_value_size)
                st.plotly_chart(volcano_plot)

                # Customizing the download button based on user preferences
                download_button = st.download_button(
                    label="Download Volcano Plot",
                    data=volcano_plot.to_image(format="png", width=width, height=height, scale=resolution),
                    file_name="volcano_plot.png",
                    key="volcano_plot_download_button"
                )

