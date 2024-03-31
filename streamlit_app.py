import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from st_files_connection import FilesConnection

# Page title
st.set_page_config(page_title='Test Dash', page_icon='📊')
st.title('📊 Test Dash 1')


with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
  st.markdown('**How to use the app?**')
  st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')
  
st.subheader('Which Movie Genre performs ($) best at the box office?')


# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('s3', type=FilesConnection)
df = conn.read("scoops-finder/baseline2.csv", input_format="csv", ttl=600)

# Specify the columns to keep
columns_to_keep = ['brand_name', 'model_name', 'product_type', 'marking_technology',
                   'color_capability', 'date_available_on_market', 'date_qualified',
                   'markets', 'monochrome_product_speed_ipm_or_mppm']

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
                  "Lexmark", "Ricoh", "Sharp", "Toshiba", "Xerox", "Pantum", "Fujifilm"]

# Specify the product types to filter
product_types_to_show = ['Printers', 'Multifunction Devices (MFD)']

# Filter the new DataFrame to only include specified brands, product types, and hide entries with "Label Printer" in the Model column
filtered_df = new_df[(new_df['Brand'].isin(brands_to_show)) & 
                     (new_df['Product Type'].isin(product_types_to_show)) & 
                     (~new_df['Model'].str.contains('Label Printer', case=False))]

# Print filtered results.
st.write(filtered_df)


# Load data
#df = pd.read_csv('data/movies_genres_summary.csv')
#df.year = df.year.astype('int')