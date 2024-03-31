import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from st_files_connection import FilesConnection

st.set_page_config(
    page_title="Scooper Dashboard",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

st.title('Scooper Dashboard 🖨️')
st.markdown('**What can this app do?**')
st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
st.divider()

# Define columns
col1, col2 = st.columns(2)

# Left Column: Product Registrations
with col1:
    st.header('Certifications 📝')
    st.subheader('Energy Star ⚡')

    # Create connection object and retrieve file contents.
    # Specify input format is a csv and to cache the result for 600 seconds.
    conn = st.connection('s3', type=FilesConnection)
    df = conn.read("scoops-finder/baseline2.csv", input_format="csv", ttl=600)

    # Specify the columns to keep
    columns_to_keep = ['brand_name', 'model_name', 'product_type', 'marking_technology',
                       'color_capability', 'date_available_on_market', 'date_qualified',
                       'markets', 'monochrome_product_speed_ipm_or_mppm']

    # Create a new DataFrame with only the specified columns
    new_df = df[columns_to_keep]

    # Rename the columns
    new_df = new_df.rename(columns={
        'brand_name': 'Brand',
        'model_name': 'Model',
        'product_type': 'Product Type',
        'marking_technology': 'Technology',
        'color_capability': 'Color/Mono',
        'date_available_on_market': 'Date Available',
        'date_qualified': 'Date Qualified',
        'markets': 'Target Markets',
        'monochrome_product_speed_ipm_or_mppm': 'Print Speed'
    })

    # Specify the brands to filter
    brands_to_show = ["Canon", "Brother", "HP", "Epson", "Konica Minolta", "Kyocera",
                      "Lexmark", "Ricoh", "Sharp", "Toshiba", "Xerox", "Pantum", "Fujifilm", "HP Inc."]

    # Specify the product types to filter
    product_types_to_show = ['Printers', 'Multifunction Devices (MFD)']

    # Cut off the "Date Available" and "Date Qualified" columns to remove anything after the first 10 digits
    new_df['Date Available'] = new_df['Date Available'].str[:10]
    new_df['Date Qualified'] = new_df['Date Qualified'].str[:10]

    # Filter the new DataFrame to only include specified brands, product types, and hide entries with "Label Printer" in the Model column
    filtered_df = new_df[(new_df['Brand'].isin(brands_to_show)) &
                         (new_df['Product Type'].isin(product_types_to_show)) &
                         (~new_df['Model'].str.contains('Model Printer|Label Printer', case=False))]

    # Sort the filtered DataFrame by Date Available (Newest to Oldest)
    filtered_df.sort_values(by='Date Available', ascending=False, inplace=True)

    # Print filtered results.
    st.write(filtered_df)

    # Add metric to show latest 3 records based on product name
    # latest_records = filtered_df.head(3)['Model'].tolist()
    # st.metric("Latest 3 Products", ", ".join(latest_records))

    st.subheader('WiFi Alliance 📶')
    # Create connection object and retrieve file contents.
    # Specify input format is a csv and to cache the result for 600 seconds.
    conn = st.connection('s3', type=FilesConnection)
    df2 = conn.read("scoops-finder/baseline3.csv", input_format="csv", ttl=600)

    # Keep only the desired columns
    df2_modified = df2[["CID", "Date of Last Certification", "Brand", "Product", "Model Number"]]

    # Filter by specified brands
    df2_modified = df2_modified[df2_modified["Brand"].isin(brands_to_show)]

    # Sort the dataframe by "Date of Last Certification", from newest to oldest
    df2_modified.sort_values(by="Date of Last Certification", ascending=False, inplace=True)

    # Write the modified dataframe
    st.write(df2_modified)

    st.subheader('EPEAT 🌎')
    conn = st.connection('s3', type=FilesConnection)
    df3 = conn.read("scoops-finder/baseline4.csv", input_format="csv", ttl=600)

    # Keep only the desired columns
    df3_modified = df3[["Id", "Registered On", "Product Type", "Product Name", "Manufacturer"]]

    # Filter by specified brands
    df3_modified = df3_modified[df3_modified["Manufacturer"].isin(brands_to_show)]

    # Sort the dataframe by "Date of Last Certification", from newest to oldest
    df3_modified.sort_values(by="Registered On", ascending=False, inplace=True)

    # Write the modified dataframe
    st.write(df3_modified)

# Right Column: Placements
# Right Column: Placements
# Right Column: Placements
# Right Column: Placements
with col2:
    st.header('Placements 💡')
    st.subheader('Changelog 🔄')

    st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    
    for index, row in latest_df4.iterrows():
        brand = row['Brand']
        count = df5[df5['Brand'] == brand]['Count'].values[0]
        metric_label = row['Action']
        metric_value = row['Product Name']
        metric_delta = str(count)
        # Change color based on action
        delta_color = 'normal' if metric_label == 'Added' else 'inverse' if metric_label == 'Removed' else 'normal'
        st.metric(label=metric_label, value=metric_value, delta=metric_delta, delta_color=delta_color)
    
    st.subheader('Current Placement Count By Brand')

    conn = st.connection('s3', type=FilesConnection)
    df5 = conn.read("scoops-finder/brand_counts.csv", input_format="csv", ttl=600)
    df5 = df5[-10:]
    df5 = df5.sort_values(by='Brand').reset_index(drop=True)
    st.bar_chart(df5.set_index('Brand')['Count'], width=200, height=500, color='#FFA500')
    st.write(df5)
    
    # Add your placements data here
    conn = st.connection('s3', type=FilesConnection)
    df4 = conn.read("scoops-finder/tracking.csv", input_format="csv", ttl=600)
    df4.drop_duplicates(subset="Product Name", inplace=True)
    latest_df4 = df4.tail(5)  # Get the latest 5 records
    st.write(df4)
    
    # Create metrics for the latest 5 records

    




    
