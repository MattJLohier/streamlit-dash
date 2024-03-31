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

# Specify the brands to filter
brands_to_show = ["Canon", "Brother", "HP", "Epson", "Konica Minolta", "Kyocera", 
                  "Lexmark", "Ricoh", "Sharp", "Toshiba", "Xerox", "Pantum", "Fujifilm"]

# Filter DataFrame to only include specified brands
filtered_df = df[df['brand_name'].isin(brands_to_show)]

# Print filtered results.
st.write(filtered_df)

# Load data
#df = pd.read_csv('data/movies_genres_summary.csv')
#df.year = df.year.astype('int')