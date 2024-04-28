import streamlit as st
import datetime
import numpy as np
import pandas as pd
import altair as alt
from st_files_connection import FilesConnection
import hashlib
from io import BytesIO
from PIL import Image
import requests
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts
import pytz


# URL of the image you want to use as the page icon
icon_url = "https://i.postimg.cc/Y0XLcpg7/scooper-s.png"

# Download the image
response = requests.get(icon_url)
image = Image.open(BytesIO(response.content))

# Set the Streamlit page configuration with the custom icon
st.set_page_config(
    page_title="Scooper Dashboard",
    page_icon=image,
    layout="wide",
    initial_sidebar_state="expanded"
)

def display_dashboard():
    alt.themes.enable("dark")
    st.markdown("<h1 style='text-align: left;'><span style='color: #317bd4;'>Scooper</span> Dashboard</h1>", unsafe_allow_html=True)
    st.markdown('**Welcome to Scooper Dashboard**')
    st.info('Scooper is a Python tool hosted on AWS (Lambda/S3/EC2) that uses Selenium and Pandas to scrape new product certifications and placements from official manufacturer websites.') 
    st.caption('Scooper currently scrapes certifications from EnergyStar, WiFi Alliance, and the EPEAT registry, and checks for new products on the official sites of HP, Canon, Kyocera, Konica Minolta, Lexmark, Ricoh, Sharp, Toshiba, Xerox, and Fujifilm')
    with st.container():
        st.write("")  # Optional: Use st.empty() if you prefer no filler text at all
        linkedin_url = "https://www.linkedin.com/in/matt-lohier/"  # Change this URL to your specific LinkedIn profile or page
        personal_website_url = "https://matt-lohier.com/"  # Change this to your personal website URL
        st.markdown(f"""
        <a href="{linkedin_url}" target="_blank" style='display: inline-block; padding-right: 10px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' style='width:32px; height:32px;'>
        </a><!--
        --><a href="{personal_website_url}" target="_blank" style='display: inline-block;'>
            <img src='https://i.postimg.cc/9MbrTWL9/portfolio.png' style='width:32px; height:32px;'>
        </a>
        """, unsafe_allow_html=True)


def sidebar():
    st.sidebar.image("https://i.postimg.cc/XJdg0y7b/scooper-logo.png", use_column_width=True)
    st.sidebar.markdown("---")

    # Define product categories and their corresponding buttons
    product_categories = {
        'Imaging Equipment': ['Home', 'Certifications', 'Placements'],
        'Computers': ['Home', 'Certifications'],
        'Televisions': ['Home', 'Certifications']
    }

    # Allow the user to select a product type
    selected_category = st.sidebar.selectbox("Select Your Product Type", list(product_categories.keys()))
    st.session_state['selected_product_type'] = selected_category
    # Get buttons for the selected product category
    buttons = product_categories[selected_category]

    button_container = st.sidebar.container()

    # Button display logic based on selected product category
    with button_container:
        if 'Home' in buttons and st.button("Home", key="home_button"):
            st.session_state['page'] = 'home'
        if 'Certifications' in buttons and st.button("Certifications", key="certifications_button"):
            st.session_state['page'] = 'certifications'
        if 'Placements' in buttons and st.button("Placements", key="placements_button"):
            st.session_state['page'] = 'placements'
    
    # Inject CSS to make container's children (buttons) 100% width
    st.sidebar.markdown("""
    <style>

    .stButton button:hover{
        border-color: #3775cb !important;
        color: #3775cb;
    }

    .stButton button:focus{
        border-color: #3775cb !important;
        color: #3775cb;
        background-color: white;
    }

    .st-emotion-cache-32r2nf:focus:not(:active){
        border-color: #3775cb !important;
        color: #3775cb;
        background-color: white;
    }

    [data-testid="stSidebarUserContent"] .stButton button {
        width: 100%;
        font-weight: bold;               /* Make text bold */
        color: white;                    /* Set text color to white */
        background-color: #3775cb;       /* Set normal state background color */
        transition: background-color 0.3s, color 0.3s; /* Smooth transition for hover effect */
    }
    [data-testid="stSidebarUserContent"] .stButton button:hover {
        color: #3775cb;                  /* Text color on hover */
        background-color: white;         /* Background color on hover */

    }
    [data-testid="stSidebarUserContent"] .stButton button:active {
        background-color: #1f4476;       /* Set active state background color */
        color: white;                    /* Set text color in active state */
    }
    [data-testid="stSidebarUserContent"] .stButton button:focus {
        background-color: #1f4476;       /* Set active state background color */
        color: white;                    /* Set text color in active state */
    }
    </style>
    """, unsafe_allow_html=True)

    # Custom CSS to change the progress bar color
    progress_bar_color_style = """
    <style>
    /* CSS selector for the Streamlit progress bar */
    .stProgress > div > div > div > div {
        background-color: #0078D7 !important; /* Set to desired shade of blue */
    }
    </style>
    """
    st.sidebar.markdown(progress_bar_color_style, unsafe_allow_html=True)

    # Timezone setting for PST
    timezone = pytz.timezone('America/Los_Angeles')
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(timezone)
    
    # Determine the next refresh time (9 AM PST)
    next_refresh = now.replace(hour=9, minute=0, second=0, microsecond=0)
    if now.hour >= 9 or (now.hour == 9 and now.minute > 0):  # Check past 9 AM PST
        next_refresh += datetime.timedelta(days=1)
    
    # Calculate time left until next refresh
    time_left = next_refresh - now
    total_seconds = time_left.total_seconds()

    # Calculate progress (based on how many seconds have elapsed in the current 24-hour period)
    progress = (1 - (time_left.seconds / 86400)) * 100

    # Display the progress bar and time left in rounded hours
    hours_left = round(time_left.total_seconds() / 3600)
    st.sidebar.progress(int(progress))
    st.sidebar.markdown(f"**Refresh in: {hours_left} hours**")


def login(username, password):
    hashed_password = st.secrets["hashed_password"]
    # Check if the username and hashed password match
    # You would typically retrieve this information from a database
    # Here, we'll hardcode a username and password for demonstration
    if username == "admin" and hashlib.sha256(password.encode()).hexdigest() == hashed_password:
        return True
    else:
        return False

def display_login_form():
    # Create three columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:  # Middle column for the form
        st.markdown("""
        <center>
            <img src='https://i.postimg.cc/XJdg0y7b/scooper-logo.png' width='300'>
        </center>
        """, unsafe_allow_html=True)
        with st.form(key='login_form'):
            # Input fields for username and password
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

            if login_button:
                if login(username, password):  # Assume login is a function defined to check credentials
                    st.session_state['logged_in'] = True  # Update session state
                    st.rerun()
                else:
                    st.error("Invalid username or password")

def display_certifications_page():
    # Check the selected product type
    product_type = st.session_state['selected_product_type']

    if product_type == 'Imaging Equipment':
        display_certifications_imaging()
    elif product_type == 'Computers':
        display_certifications_computers()
    elif product_type == 'Televisions':
        display_certifications_televisions()
    else:
        st.write("No specific certifications are available for this category.")


def display_placements_page():    
    # Check the selected product type
    product_type = st.session_state['selected_product_type']

    if product_type == 'Imaging Equipment':
        display_placements_imaging()
    elif product_type == 'Computers':
        display_placements_computers()
    elif product_type == 'Televisions':
        display_placements_televisions()
    else:
        st.write("No specific certifications are available for this category.")

def display_certifications_imaging():
    st.title("Imaging Certifications 🖨️")
    st.markdown('---')
    # Define buttons for navigation
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Recent'

    # Create four columns for the interactive tiles
    col1, col2, col3, col4 = st.columns(4)

    # Define interactive tiles that update the session state upon clicking
    if col1.button('Recent 🆕', key='1', use_container_width=True):
        st.session_state['current_page'] = 'Recent'
    if col2.button('Raw Data 📝', key='2', use_container_width=True):
        st.session_state['current_page'] = 'Raw Data'
    if col3.button('Changelog 🔄', key='3', use_container_width=True):
        st.session_state['current_page'] = 'Changelog'
    if col4.button('Insights 🔍', key='4', use_container_width=True):
        st.session_state['current_page'] = 'Insights'

    # Conditional rendering based on selected page
    if st.session_state['current_page'] == 'Recent':
        show_recent_cert()
    elif st.session_state['current_page'] == 'Raw Data':
        show_raw_data_cert()
    elif st.session_state['current_page'] == 'Changelog':
        show_changelog_cert()
    elif st.session_state['current_page'] == 'Insights':
        show_insights_cert()    


def show_recent_cert():
    conn = st.connection('s3', type=FilesConnection)
    df = conn.read("scoops-finder/baseline2.csv", input_format="csv", ttl=600)

    # Specify the columns to keep
    columns_to_keep = ['brand_name', 'model_name', 'product_type',
                    'color_capability', 'date_available_on_market', 'date_qualified',
                    'markets', 'monochrome_product_speed_ipm_or_mppm']

    # Create a new DataFrame with only the specified columns
    new_df = df[columns_to_keep]

    # Rename the columns
    new_df = new_df.rename(columns={
        'brand_name': 'Brand',
        'model_name': 'Model',
        'product_type': 'Product Type',
        'color_capability': 'Color/Mono',
        'date_available_on_market': 'Date Available',
        'date_qualified': 'Date Qualified',
        'markets': 'Target Markets',
        'monochrome_product_speed_ipm_or_mppm': 'Print Speed'
    })

    # Specify the brands to filter
    brands_to_show = ["Canon", "Brother", "HP", "Epson", "Konica Minolta", "Kyocera",
                    "Lexmark", "Ricoh", "Sharp", "Toshiba", "Xerox", "Pantum", "Fujifilm", "HP Inc.", "Zhuhai Pantum Electronics Co., Ltd."]

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
    filtered_df.reset_index(drop=True, inplace=True)
    estardf = filtered_df

    # Print filtered results.
    # Add metric to show latest 3 records based on product name
    # latest_records = filtered_df.head(3)['Model'].tolist()
    # st.metric("Latest 3 Products", ", ".join(latest_records))
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
    df2_modified.reset_index(drop=True, inplace=True)
    df2_modified.drop_duplicates(inplace=True)
    # Write the modified dataframe
    conn = st.connection('s3', type=FilesConnection)
    df3 = conn.read("scoops-finder/baseline4.csv", input_format="csv", ttl=600)
    # Keep only the desired columns
    df3_modified = df3[["Id", "Registered On", "Product Type", "Product Name", "Manufacturer"]]
    # Filter by specified brands
    df3_modified = df3_modified[df3_modified["Manufacturer"].isin(brands_to_show)]
    # Sort the dataframe by "Date of Last Certification", from newest to oldest
    df3_modified.sort_values(by="Registered On", ascending=False, inplace=True)
    df3_modified.reset_index(drop=True, inplace=True)
    df3_modified.drop_duplicates(inplace=True)
    # Write the modified dataframe
    # Rename and remove columns for filtered_df
    filtered_df = filtered_df.rename(columns={'Model': 'Product Name', 'Date Available': 'Certification Date'})
    filtered_df = filtered_df.drop(columns=['Color/Mono', 'Date Qualified', 'Target Markets', 'Print Speed'])
    filtered_df = filtered_df[['Product Name', 'Brand', 'Certification Date', 'Product Type']]
    # Rename and remove columns for df2_modified
    df2_modified = df2_modified.rename(columns={'Manufacturer': 'Brand', 'Product': 'Product Name', 'Date of Last Certification': 'Certification Date'})
    df2_modified = df2_modified.drop(columns=['CID', 'Model Number'])
    df2_modified = df2_modified[['Product Name', 'Brand', 'Certification Date']]
    # Rename and remove columns for df3_modified
    df3_modified = df3_modified.rename(columns={'Registered On': 'Certification Date', 'Manufacturer': 'Brand'})
    df3_modified = df3_modified.drop(columns=['Id'])
    df3_modified = df3_modified[['Product Name', 'Brand', 'Certification Date', 'Product Type']]
    df3_modified = df3_modified[df3_modified['Product Type'].isin(['Printer', 'Multifunction Device'])]
    
    # Add a "Source" column to each dataframe
    filtered_df['Source'] = 'Energy Star'
    df2_modified['Source'] = 'WiFi Alliance'
    df3_modified['Source'] = 'EPEAT Registry'
    
    # Concatenate the dataframes
    combined_df = pd.concat([filtered_df, df2_modified, df3_modified], ignore_index=True)
    # Assuming "Certification Date" is already in string format
    # If not, convert it to string before truncating
    
    # Truncate the date to keep only the first 10 characters
    combined_df['Certification Date'] = combined_df['Certification Date'].str[:10]
    # Convert the truncated date to datetime format
    combined_df['Certification Date'] = pd.to_datetime(combined_df['Certification Date'], errors='coerce')
    # Sort the combined dataframe by "Certification Date" in descending order
    combined_df.sort_values(by='Certification Date', ascending=False, inplace=True)
    # Reset index

    combined_df.reset_index(drop=True, inplace=True)
    combined_df.drop_duplicates(inplace=True)
    combined_df['Certification Date'] = combined_df['Certification Date'].astype(str).str[:10]
    # Show only the newest 5 records
    newest_records = combined_df.head(10)
    
    st.header('Recent Certifications')
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    wch_colour_font = (0, 0, 0)
    fontsize = 14
    valign = "left"
    iconname = "fas fa-xmark"
    sline = "New Certifications Detected"
    container = st.container()

    st.markdown('''
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* Maintains 3 columns */
        grid-gap: 20px; /* Space between cards */
        padding: 10px;
        width: auto; /* Adjust based on the actual space available or use 100% if it should be fully responsive */
    }

    .card {
        height: auto;
        min-height: 120px;
        position: relative;
        width: 100%; /* This makes each card responsive within its grid column */
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2px;
        border-radius: 24px;
        overflow: hidden;
        line-height: 1.6;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        margin: 15px; /* Added margin */
    }

    .content {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 24px;
    padding: 20px;
    padding-bottom: 0px;
    border-radius: 22px;
    color: #ffffff;
    overflow: hidden;
    background: #ffffff;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .content .heading {
    font-weight: 600;
    font-size: 20px;
    line-height: 1;
    z-index: 1;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .content .para {
    z-index: 1;
    opacity: 0.8;
    font-size: 16px;
    font-weight: 400;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .card::before {
    content: "";
    position: absolute;
    height: 500%;
    width: 500%;
    border-radius: inherit;
    background: #3775cb;
    background: linear-gradient(to right, #3775cb, #3775cb);
    transform-origin: center;
    animation: moving 9.8s linear infinite paused;
    transition: all 0.88s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .card:hover::before {
    animation-play-state: running;
    z-index: -1;
    width: 20%;
    }

    .card:hover .content .heading,
    .card:hover .content .para {
    color: #000000;
    }

    .card:hover {
    box-shadow: 0rem 6px 13px rgba(10, 60, 255, 0.1),
        0rem 24px 24px rgba(10, 60, 255, 0.09),
        0rem 55px 33px rgba(10, 60, 255, 0.05),
        0rem 97px 39px rgba(10, 60, 255, 0.01), 0rem 152px 43px rgba(10, 60, 255, 0);
    scale: 1.00;
    color: #000000;
    }

    @keyframes moving {
    0% {
        transform: rotate(0);
    }

    100% {
        transform: rotate(360deg);
    }
    }
    </style>
    ''', unsafe_allow_html=True)

    emoji_dict = {
            "Energy Star": "⚡",
            "WiFi Alliance": "📶",
            "EPEAT": "🌎"
        }

    # Sample data iteration - replace 'newest_records' with your actual DataFrame
    
    # Define the number of columns
    num_columns = 2
    rows = [st.columns(num_columns) for _ in range((len(newest_records) + num_columns - 1) // num_columns)]

    # Initialize a counter for DataFrame row indices
    row_index = 0

    # Fill each cell in the grid with content
    for row in rows:
        for col in row:
            if row_index < len(newest_records):
                with col:
                    row_data = newest_records.iloc[row_index]
                    product_name = row_data['Product Name']
                    certification_date = row_data['Certification Date']
                    brand = row_data['Brand']
                    product_type = row_data['Product Type']
                    source = row_data['Source']
                    emoji = emoji_dict.get(source, "📝")

                    # Embed data into HTML
                    html_content = f"""
                    <div class="card">
                        <div class="content">
                            <p class="heading">{product_name}</p>
                            <p class="para">
                                Brand: {brand}<br>
                                Product Type: {product_type}<br>
                                Certification Date: {certification_date}<br>
                                Source: {source} {emoji}
                            </p>
                        </div>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)

                    row_index += 1   


def show_raw_data_cert():
    st.header('Raw Certification Data')
    st.subheader('Energy Star ⚡')
    conn = st.connection('s3', type=FilesConnection)
    df_raw_certs2 = conn.read("scoops-finder/baseline2.csv", input_format="csv", ttl=600)
    df_sorted = df_raw_certs2.sort_values(by="date_available_on_market", ascending=False)

    def extract_unique_countries(market_col):
        unique_countries = set()
        # Split each row's market string by comma and strip spaces
        market_col.apply(lambda x: unique_countries.update(map(str.strip, x.split(','))))
        return ['any'] + sorted(unique_countries)

    unique_countries = extract_unique_countries(df_sorted['markets'])

    # Organizing filters into a 2x2 grid
    col1, col2 = st.columns(2)
    with col1:
        # Filter by product category
        categories = ['any'] + list(df_sorted['product_type'].unique())
        selected_category = st.selectbox('Select a product category', categories, index=0 if 'any' in categories else 1)
        if selected_category != 'any':
            df_sorted = df_sorted[df_sorted['product_type'] == selected_category]
            

        # Filter by brand
        brands = ['any'] + list(df_sorted['brand_name'].unique())
        selected_brand = st.selectbox('Select a brand', brands, index=0 if 'any' in brands else 1)
        if selected_brand != 'any':
            df_sorted = df_sorted[df_sorted['brand_name'] == selected_brand]

        remanufactured_options = ['any', 'Yes', 'No']
        selected_remanufactured = st.selectbox('Remanufactured Product', remanufactured_options, index=0)
        if selected_remanufactured == 'Yes':
            df_sorted = df_sorted[df_sorted['remanufactured_product'] == True]
        elif selected_remanufactured == 'No':
            df_sorted = df_sorted[df_sorted['remanufactured_product'] == False]

    with col2:
        # Filter by Markets
        selected_country = st.selectbox('Select a market', unique_countries, index=0 if 'any' in unique_countries else 1)
        if selected_country != 'any':
            df_sorted = df_sorted[df_sorted['markets'].apply(lambda x: selected_country in map(str.strip, x.split(',')))]

        # Filter by Color/Mono
        color_capabilities = ['any'] + list(df_sorted['color_capability'].unique())
        selected_color_capability = st.selectbox('Select a color capability', color_capabilities, index=0 if 'any' in color_capabilities else 1)
        if selected_color_capability != 'any':
            df_sorted = df_sorted[df_sorted['color_capability'] == selected_color_capability]

        sort_options = {'date_qualified': 'Date Qualified', 'date_available_on_market': 'Date Available on Market'}
        selected_sort = st.selectbox('Sort by', options=list(sort_options.keys()), format_func=lambda x: sort_options[x], index=1)
        df_sorted = df_sorted.sort_values(by=selected_sort, ascending=False)

    # Display the filtered dataframe
    st.write(df_sorted)

    st.subheader('EPEAT 🌎')
    conn = st.connection('s3', type=FilesConnection)
    df_raw_certs4 = conn.read("scoops-finder/baseline4.csv", input_format="csv", ttl=600)
    # Organizing filters into a 2x2 grid
    col1, col2 = st.columns(2)
    with col1:
        # Filter by product category
        categories3 = ['any'] + list(df_raw_certs4['Product Type'].unique())
        selected_category1 = st.selectbox('Select a product category', categories3, index=0 if 'any' in categories3 else 1)
        if selected_category1 != 'any':
            df_raw_certs4 = df_raw_certs4[df_raw_certs4['Product Type'] == selected_category1]
            

        brands = ['any'] + list(df_raw_certs4['Manufacturer'].unique())
        selected_brand1 = st.selectbox('Select a brand', brands, index=0 if 'any' in brands else 1)
        if selected_brand1 != 'any':
            df_raw_certs4 = df_raw_certs4[df_raw_certs4['Manufacturer'] == selected_brand1]

        remanufactured_options = ['any', 'Active', 'NA']
        selected_remanufactured1 = st.selectbox('Status', remanufactured_options, index=0)
        if selected_remanufactured1 == 'Active':
            df_raw_certs4 = df_raw_certs4[df_raw_certs4['Status'] == "Active"]
        elif selected_remanufactured1 == 'NA':
            df_raw_certs4 = df_raw_certs4[df_raw_certs4['Status'] == False]

    with col2:
        # Filter by Market
        markets = ['any'] + list(df_raw_certs4['Registered In'].unique())
        # Defaulting to 'United States' if it exists in the options
        default_market_index = markets.index('United States') if 'United States' in markets else 0
        selected_market = st.selectbox('Select a market', markets, index=default_market_index)
        if selected_market != 'any':
            df_raw_certs4 = df_raw_certs4[df_raw_certs4['Registered In'] == selected_market]


        # Filter by EPEAT Tier
        color_capabilities1 = ['any'] + list(df_raw_certs4['EPEAT Tier'].unique())
        selected_color_capability1 = st.selectbox('Select an EPEAT Tier', color_capabilities1, index=0 if 'any' in color_capabilities1 else 1)
        if selected_color_capability1 != 'any':
            df_raw_certs4 = df_raw_certs4[df_raw_certs4['EPEAT Tier'] == selected_color_capability1]

        # Filter by Registration Date
        sort_options = ['Newest', 'Oldest']
        selected_sort = st.selectbox('Sort by Registration Date', sort_options, index=0)  # Default to Newest
        if selected_sort == 'Newest':
            df_raw_certs4 = df_raw_certs4.sort_values(by='Registered On', ascending=False)
        elif selected_sort == 'Oldest':
            df_raw_certs4 = df_raw_certs4.sort_values(by='Registered On', ascending=True)

    st.write(df_raw_certs4)


    st.subheader('WiFi Alliance 📶')
    conn = st.connection('s3', type=FilesConnection)
    df_raw_certs5 = conn.read("scoops-finder/baseline3.csv", input_format="csv", ttl=600)

    col1, col2 = st.columns(2)
    with col1:
        # Filter by product category
        categories1 = ['any'] + list(df_raw_certs5['Category'].unique())
        selected_category2 = st.selectbox('Select a product category', categories1, index=0 if 'any' in categories1 else 1)
        if selected_category2 != 'any':
            df_raw_certs5 = df_raw_certs5[df_raw_certs5['Category'] == selected_category2]

        # Filter by brand
        brands = ['any'] + list(df_raw_certs5['Brand'].unique())
        selected_brand2 = st.selectbox('Select a brand', brands, index=0 if 'any' in brands else 1)
        if selected_brand2 != 'any':
            df_raw_certs5 = df_raw_certs5[df_raw_certs5['Brand'] == selected_brand2]

    with col2:
        # Filter by Registration Date
        sort_options = ['Newest', 'Oldest']
        selected_sort2 = st.selectbox('Sort by Date', sort_options, index=0)  # Default to Newest
        if selected_sort2 == 'Newest':
            df_raw_certs5 = df_raw_certs5.sort_values(by='Date of Last Certification', ascending=False)
        elif selected_sort2 == 'Oldest':
            df_raw_certs5 = df_raw_certs5.sort_values(by='Date of Last Certification', ascending=True)

    st.write(df_raw_certs5)

def show_changelog_cert():
    # Code to display changelog
    st.header('Changelogs')
    # Example: st.write(data_changelog)
    st.subheader('Energy Star ⚡')
    # Example: st.write(data_changelog)
    conn = st.connection('s3', type=FilesConnection)
    placement_changelog1 = conn.read("scoops-finder/changelog-estar.csv", input_format="csv", ttl=600)
    df_clean = placement_changelog1.drop_duplicates(subset=['pd_id'])  # Drop duplicates based on 'pd_id'
    
    # Define the columns you want to keep
    columns_to_keep = [
        'Date', 'model_name', 'brand_name', 'product_type', 'color_capability', 
        'monochrome_product_speed_ipm_or_mppm', 'date_available_on_market', 
        'date_qualified', 'markets'
    ]

    # Select only the specified columns
    df_clean = df_clean[columns_to_keep]

    # Keep only the first 10 characters of the "Date" column
    df_clean['Date'] = df_clean['Date'].str[:10]

    # Rename the columns
    df_clean.rename(columns={
        'Date': 'Date Detected',
        'model_name': 'Model Name',
        'brand_name': 'Brand',
        'product_type': 'Product Type',
        'color_capability': 'Color/BW',
        'monochrome_product_speed_ipm_or_mppm': 'Print Speed',
        'date_available_on_market': 'Date Available on Market',
        'date_qualified': 'Date Qualified',
        'markets': 'Markets'
    }, inplace=True)
    

    df_clean['Date Available on Market'] = df_clean['Date Available on Market'].str[:10]
    df_clean['Date Qualified'] = df_clean['Date Qualified'].str[:10]
    df_clean = df_clean.sort_values(by='Date Detected', ascending=False)
    st.write(df_clean)

    st.subheader('EPEAT 🌎')
    conn = st.connection('s3', type=FilesConnection)
    placement_tracking2 = conn.read("scoops-finder/changelog-epeat.csv", input_format="csv", ttl=600)
    df_epeat_changelog = placement_tracking2

    columns_to_keep2 = ["Date", "Product Name", "Manufacturer", "Climate+", "Product Category", 
                    "Product Type", "Status", "Registered In", "Total Score", "EPEAT Tier", "Registered On"]

    # Modify the dataframe to keep only the specified columns
    df_epeat_changelog = df_epeat_changelog[columns_to_keep2]
    
    df_epeat_changelog['Date'] = df_epeat_changelog['Date'].str[:10]

    # Rename the "Date" column to "Date Detected"
    df_epeat_changelog.rename(columns={'Date': 'Date Detected'}, inplace=True)
    df_epeat_changelog = df_epeat_changelog.sort_values(by='Date Detected', ascending=False)
    st.write(df_epeat_changelog)

    st.subheader('WiFi Alliance 📶')
    conn = st.connection('s3', type=FilesConnection)
    placement_tracking3 = conn.read("scoops-finder/changelog-wifi.csv", input_format="csv", ttl=600)

    df_wifi_changelog = placement_tracking3

    columns_to_keep3 = ["Date", "Product", "Brand", "Model Number", "Category"]

    df_wifi_changelog = df_wifi_changelog[columns_to_keep3]
    df_wifi_changelog['Date'] = df_wifi_changelog['Date'].str[:10]
    df_wifi_changelog.rename(columns={'Date': 'Date Detected'}, inplace=True)
    df_wifi_changelog = df_wifi_changelog.sort_values(by='Date Detected', ascending=False)

    st.write(df_wifi_changelog)


def show_insights_cert():
    # Code to display insights
    st.header('Insights')
    # Example: st.write(data_insights)
    conn = st.connection('s3', type=FilesConnection)
    df = conn.read("scoops-finder/baseline2.csv", input_format="csv", ttl=600)

    # Specify the columns to keep
    columns_to_keep = ['brand_name', 'model_name', 'product_type',
                    'color_capability', 'date_available_on_market', 'date_qualified',
                    'markets', 'monochrome_product_speed_ipm_or_mppm']

    # Create a new DataFrame with only the specified columns
    new_df = df[columns_to_keep]

    # Rename the columns
    new_df = new_df.rename(columns={
        'brand_name': 'Brand',
        'model_name': 'Model',
        'product_type': 'Product Type',
        'color_capability': 'Color/Mono',
        'date_available_on_market': 'Date Available',
        'date_qualified': 'Date Qualified',
        'markets': 'Target Markets',
        'monochrome_product_speed_ipm_or_mppm': 'Print Speed'
    })

    # Specify the brands to filter
    brands_to_show = ["Canon", "Brother", "HP", "Epson", "Konica Minolta", "Kyocera",
                    "Lexmark", "Ricoh", "Sharp", "Toshiba", "Xerox", "Pantum", "Fujifilm", "HP Inc.", "Zhuhai Pantum Electronics Co., Ltd."]

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
    filtered_df.reset_index(drop=True, inplace=True)
    estardf = filtered_df

    # Print filtered results.
    # Add metric to show latest 3 records based on product name
    # latest_records = filtered_df.head(3)['Model'].tolist()
    # st.metric("Latest 3 Products", ", ".join(latest_records))
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
    df2_modified.reset_index(drop=True, inplace=True)
    df2_modified.drop_duplicates(inplace=True)
    # Write the modified dataframe
    conn = st.connection('s3', type=FilesConnection)
    df3 = conn.read("scoops-finder/baseline4.csv", input_format="csv", ttl=600)
    # Keep only the desired columns
    df3_modified = df3[["Id", "Registered On", "Product Type", "Product Name", "Manufacturer"]]
    # Filter by specified brands
    df3_modified = df3_modified[df3_modified["Manufacturer"].isin(brands_to_show)]
    # Sort the dataframe by "Date of Last Certification", from newest to oldest
    df3_modified.sort_values(by="Registered On", ascending=False, inplace=True)
    df3_modified.reset_index(drop=True, inplace=True)
    df3_modified.drop_duplicates(inplace=True)
    # Write the modified dataframe
    # Rename and remove columns for filtered_df
    filtered_df = filtered_df.rename(columns={'Model': 'Product Name', 'Date Available': 'Certification Date'})
    filtered_df = filtered_df.drop(columns=['Color/Mono', 'Date Qualified', 'Target Markets', 'Print Speed'])
    filtered_df = filtered_df[['Product Name', 'Brand', 'Certification Date', 'Product Type']]
    # Rename and remove columns for df2_modified
    df2_modified = df2_modified.rename(columns={'Manufacturer': 'Brand', 'Product': 'Product Name', 'Date of Last Certification': 'Certification Date'})
    df2_modified = df2_modified.drop(columns=['CID', 'Model Number'])
    df2_modified = df2_modified[['Product Name', 'Brand', 'Certification Date']]
    # Rename and remove columns for df3_modified
    df3_modified = df3_modified.rename(columns={'Registered On': 'Certification Date', 'Manufacturer': 'Brand'})
    df3_modified = df3_modified.drop(columns=['Id'])
    df3_modified = df3_modified[['Product Name', 'Brand', 'Certification Date', 'Product Type']]
    df3_modified = df3_modified[df3_modified['Product Type'].isin(['Printer', 'Multifunction Device'])]
    
    # Add a "Source" column to each dataframe
    filtered_df['Source'] = 'Energy Star'
    df2_modified['Source'] = 'WiFi Alliance'
    df3_modified['Source'] = 'EPEAT Registry'
    
    # Concatenate the dataframes
    combined_df = pd.concat([filtered_df, df2_modified, df3_modified], ignore_index=True)
    # Assuming "Certification Date" is already in string format
    # If not, convert it to string before truncating
    
    # Truncate the date to keep only the first 10 characters
    # Convert the truncated date to datetime format
    combined_df['Certification Date'] = pd.to_datetime(combined_df['Certification Date'], errors='coerce')
    combined_df['Brand'] = combined_df['Brand'].replace('HP Inc.', 'HP')
    # Sort the combined dataframe by "Certification Date" in descending order
    combined_df.sort_values(by='Certification Date', ascending=False, inplace=True)

    st.title('Certification Analysis By Brand Over Time')

    # Assuming combined_df is loaded correctly
    combined_df['Certification Date'] = pd.to_datetime(combined_df['Certification Date'])
    combined_df['Quarter'] = combined_df['Certification Date'].dt.to_period('Q')

    # Sort quarters and create quarter strings
    unique_quarters = combined_df['Quarter'].drop_duplicates().sort_values()
    combined_df['Quarter String'] = combined_df['Quarter'].apply(lambda q: f'{q.year}-Q{q.quarter}')
    unique_quarters_str = [f'{q.year}-Q{q.quarter}' for q in unique_quarters]  # Sorted and formatted quarter strings

    # Set up the slider for Quarter selection
    latest_quarter = unique_quarters_str[-1]  # Ensure to set to the latest quarter
    earliest_quarter = unique_quarters_str[0]  # Ensure to set to the earliest quarter

    # Set default value of slider to include the entire range of available quarters
    quarter_range = st.select_slider(
        'Select Quarter Range',
        options=unique_quarters_str,
        value=(earliest_quarter, latest_quarter),
        key='quarter_range_selector2'
    )

    # Filters for the charts
    selected_source = st.multiselect(
        'Select Sources',
        options=combined_df['Source'].unique(),
        default=combined_df['Source'].unique(),
        key='source_selector2'
    )

    selected_brand = st.multiselect(
        'Select Brands',
        options=combined_df['Brand'].unique(),
        default=combined_df['Brand'].unique(),
        key='brand_selector2'
    )

    # Apply filters based on Source, Brand, and quarter range
    filtered_data = combined_df[
        (combined_df['Source'].isin(selected_source)) &
        (combined_df['Brand'].isin(selected_brand)) &
        (combined_df['Quarter String'] >= quarter_range[0]) &
        (combined_df['Quarter String'] <= quarter_range[1])
    ]

    # Group by Source, Brand, and Quarter and count the occurrences
    grouped_data = filtered_data.groupby(['Source', 'Brand', 'Quarter String']).size().reset_index(name='Counts')

    # Interactive line chart
    line_chart = alt.Chart(grouped_data).mark_line(point=True).encode(
        x=alt.X('Quarter String:O', sort=unique_quarters_str, title='Quarter'),
        y=alt.Y('Counts:Q', title='Number of Certifications'),
        color='Brand:N',
        detail='Source:N',
        tooltip=['Source', 'Brand', 'Quarter String', 'Counts']
    ).interactive()

    st.altair_chart(line_chart, use_container_width=True)

    st.title('Certification Analysis By Brand Over Time')

    # Assuming combined_df is loaded correctly
    combined_df['Certification Date'] = pd.to_datetime(combined_df['Certification Date'])
    combined_df['Quarter'] = combined_df['Certification Date'].dt.to_period('Q')
    combined_df['Quarter String'] = combined_df['Quarter'].apply(lambda q: f'{q.year}-Q{q.quarter}')
    unique_quarters_str = [f'{q.year}-Q{q.quarter}' for q in combined_df['Quarter'].drop_duplicates().sort_values()]

    # Slider for selecting quarter range
    latest_quarter = unique_quarters_str[-1]
    earliest_quarter = unique_quarters_str[0]
    quarter_range = st.select_slider(
        'Select Quarter Range',
        options=unique_quarters_str,
        value=(earliest_quarter, latest_quarter),
        key='quarter_range_selector5'
    )

    # Filters for the charts
    selected_source = st.multiselect(
        'Select Sources',
        options=['EPEAT Registry', 'Energy Star', 'WiFi Alliance'],
        default=['EPEAT Registry', 'Energy Star', 'WiFi Alliance'],
        key='source_selector5'
    )

    selected_brand = st.multiselect(
        'Select Brands',
        options=combined_df['Brand'].unique(),
        default=combined_df['Brand'].unique(),
        key='brand_selector5'
    )

    # Apply filters
    filtered_data = combined_df[
        (combined_df['Source'].isin(selected_source)) &
        (combined_df['Brand'].isin(selected_brand)) &
        (combined_df['Quarter String'] >= quarter_range[0]) &
        (combined_df['Quarter String'] <= quarter_range[1])
    ]

    # Group and prepare data for visualization
    grouped_data = filtered_data.groupby(['Source', 'Brand', 'Quarter String']).size().reset_index(name='Counts')

    # Define custom dash styles
    dash_styles = {
        "EPEAT Registry": [10, 5],
        "Energy Star": [5, 1],
        "WiFi Alliance": [1, 5]
    }

    # Chart with custom stroke dashes for each source
    line_chart = alt.Chart(grouped_data).mark_line(point=True).encode(
        x=alt.X('Quarter String:O', sort=unique_quarters_str, title='Quarter'),
        y=alt.Y('Counts:Q', title='Number of Certifications'),
        color='Brand:N',
        detail='Source:N',
        strokeDash=alt.StrokeDash(
            'Source:N', 
            scale=alt.Scale(domain=list(dash_styles.keys()), range=list(dash_styles.values())),
            legend=None
        ),
        tooltip=['Source', 'Brand', 'Quarter String', 'Counts']
    ).interactive()

    st.altair_chart(line_chart, use_container_width=True)

    st.title('Certification Analysis By Source Over Time')

   # Assuming combined_df is loaded correctly
    combined_df['Certification Date'] = pd.to_datetime(combined_df['Certification Date'])
    combined_df['Quarter'] = combined_df['Certification Date'].dt.to_period('Q')

    # Sort quarters and create quarter strings
    unique_quarters = combined_df['Quarter'].drop_duplicates().sort_values()
    combined_df['Quarter String'] = combined_df['Quarter'].apply(lambda q: f'{q.year}-Q{q.quarter}')
    unique_quarters_str = [f'{q.year}-Q{q.quarter}' for q in unique_quarters]  # Sorted and formatted quarter strings

    # Set up the slider for Quarter selection
    latest_quarter = unique_quarters_str[-1]  # Ensure to set to the latest quarter
    earliest_quarter = unique_quarters_str[0]  # Ensure to set to the earliest quarter

    # Set default value of slider to include the entire range of available quarters
    quarter_range = st.select_slider(
        'Select Quarter Range',
        options=unique_quarters_str,
        value=(earliest_quarter, latest_quarter),
        key='quarter_range_selector'
    )

    # Filters for the charts
    selected_source = st.multiselect(
        'Select Sources',
        options=combined_df['Source'].unique(),
        default=combined_df['Source'].unique(),
        key='source_selector'
    )

    selected_brand = st.multiselect(
        'Select Brands',
        options=combined_df['Brand'].unique(),
        default=combined_df['Brand'].unique(),
        key='brand_selector'
    )

    # Apply filters based on Source and quarter range
    filtered_data = combined_df[
        (combined_df['Source'].isin(selected_source)) &
        (combined_df['Quarter String'] >= quarter_range[0]) &
        (combined_df['Quarter String'] <= quarter_range[1])
    ]

    # Group by Source and Quarter and count the occurrences
    grouped_data = filtered_data.groupby(['Source', 'Quarter String']).size().reset_index(name='Counts')

    # Interactive line chart
    line_chart = alt.Chart(grouped_data).mark_line(point=True).encode(
        x=alt.X('Quarter String:O', sort=unique_quarters_str, title='Quarter'),
        y=alt.Y('Counts:Q', title='Number of Certifications'),
        color='Source:N',
        tooltip=['Source', 'Quarter String', 'Counts']
    ).interactive()

    st.altair_chart(line_chart, use_container_width=True)


    bar_chart2 = alt.Chart(grouped_data).mark_bar().encode(
    x=alt.X('Quarter String:O', sort=unique_quarters_str, title='Quarter'),
    y=alt.Y('Counts:Q', title='Number of Certifications'),
    color='Source:N',
    tooltip=['Source', 'Quarter String', 'Counts']
    ).interactive()

    st.altair_chart(bar_chart2, use_container_width=True)
    



    st.title('Certification by Brand This Quarter')

    # Assuming combined_df is loaded correctly
    combined_df['Certification Date'] = pd.to_datetime(combined_df['Certification Date'])
    combined_df['Quarter'] = combined_df['Certification Date'].dt.to_period('Q')

    # Sort quarters and create quarter strings
    unique_quarters = combined_df['Quarter'].drop_duplicates().sort_values(ascending=True)  # Sort ascending
    combined_df['Quarter String'] = combined_df['Quarter'].apply(lambda q: f'Q{q.quarter} {q.year}')
    unique_quarters_str = [f'Q{q.quarter} {q.year}' for q in unique_quarters]  # Sorted and formatted quarter strings

    # Filters for the charts
    selected_source = st.multiselect(
        'Select Sources',
        options=combined_df['Source'].unique(),
        default=combined_df['Source'].unique(),
        key='source_selector4'
    )

    selected_brand = st.multiselect(
        'Select Brands',
        options=combined_df['Brand'].unique(),
        default=combined_df['Brand'].unique(),
        key='brand_selector4'
    )

    # Slider for selecting a quarter
    selected_quarter = st.select_slider(
        'Select a Quarter',
        options=unique_quarters_str,
        value=unique_quarters_str[-1]  # Default to the latest quarter, which is now the last item in the sorted list
    )

    # Filter data for the selected quarter and by selected filters
    filtered_data = combined_df[
        (combined_df['Source'].isin(selected_source)) &
        (combined_df['Brand'].isin(selected_brand)) &
        (combined_df['Quarter String'] == selected_quarter)
    ]

    # Group by Brand and Source, and count the occurrences for the selected quarter
    grouped_data = filtered_data.groupby(['Brand', 'Source']).size().reset_index(name='Counts')

    # Bar chart for selected quarter data by brand, colored by source
    bar_chart = alt.Chart(grouped_data).mark_bar().encode(
        x=alt.X('Brand:N', title='Brand'),
        y=alt.Y('Counts:Q', title='Number of Certifications'),
        color=alt.Color('Source:N', legend=alt.Legend(title="Source")),
        tooltip=['Brand', 'Source', 'Counts']
    ).properties(
        height=500  # Set the height of the chart here
    ).interactive()

    st.altair_chart(bar_chart, use_container_width=True)

def display_certifications_computers():
    st.title("Computers Certifications 💻")
    st.markdown("---")
    # Define buttons for navigation
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Recent'

    # Create four columns for the interactive tiles
    col1, col2, col3, col4 = st.columns(4)

    # Define interactive tiles that update the session state upon clicking
    if col1.button('Recent 🆕', key='1', use_container_width=True):
        st.session_state['current_page'] = 'Recent'
    if col2.button('Raw Data 📝', key='2', use_container_width=True):
        st.session_state['current_page'] = 'Raw Data'
    if col3.button('Changelog 🔄', key='3', use_container_width=True):
        st.session_state['current_page'] = 'Changelog'
    if col4.button('Insights 🔍', key='4', use_container_width=True):
        st.session_state['current_page'] = 'Insights'

    # Conditional rendering based on selected page
    if st.session_state['current_page'] == 'Recent':
        show_recent_cert_computers()
    elif st.session_state['current_page'] == 'Raw Data':
        show_raw_data_cert_computers()
    elif st.session_state['current_page'] == 'Changelog':
        show_changelog_cert_computers()
    elif st.session_state['current_page'] == 'Insights':
        show_insights_cert_computers()    

def show_recent_cert_computers():
    st.write("Coming Soon")
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    wch_colour_font = (0, 0, 0)
    fontsize = 14
    valign = "left"
    iconname = "fas fa-xmark"
    sline = "New Certifications Detected"
    container = st.container()

    st.markdown('''
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* Maintains 3 columns */
        grid-gap: 20px; /* Space between cards */
        padding: 10px;
        width: auto; /* Adjust based on the actual space available or use 100% if it should be fully responsive */
    }

    .card {
        height: auto;
        min-height: 120px;
        position: relative;
        width: 100%; /* This makes each card responsive within its grid column */
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2px;
        border-radius: 24px;
        overflow: hidden;
        line-height: 1.6;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        margin: 15px; /* Added margin */
    }

    .content {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 24px;
    padding: 20px;
    padding-bottom: 0px;
    border-radius: 22px;
    color: #ffffff;
    overflow: hidden;
    background: #ffffff;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .content .heading {
    font-weight: 600;
    font-size: 20px;
    line-height: 1;
    z-index: 1;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .content .para {
    z-index: 1;
    opacity: 0.8;
    font-size: 16px;
    font-weight: 400;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .card::before {
    content: "";
    position: absolute;
    height: 500%;
    width: 500%;
    border-radius: inherit;
    background: #3775cb;
    background: linear-gradient(to right, #3775cb, #3775cb);
    transform-origin: center;
    animation: moving 9.8s linear infinite paused;
    transition: all 0.88s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .card:hover::before {
    animation-play-state: running;
    z-index: -1;
    width: 20%;
    }

    .card:hover .content .heading,
    .card:hover .content .para {
    color: #000000;
    }

    .card:hover {
    box-shadow: 0rem 6px 13px rgba(10, 60, 255, 0.1),
        0rem 24px 24px rgba(10, 60, 255, 0.09),
        0rem 55px 33px rgba(10, 60, 255, 0.05),
        0rem 97px 39px rgba(10, 60, 255, 0.01), 0rem 152px 43px rgba(10, 60, 255, 0);
    scale: 1.00;
    color: #000000;
    }

    @keyframes moving {
    0% {
        transform: rotate(0);
    }

    100% {
        transform: rotate(360deg);
    }
    }
    </style>
    ''', unsafe_allow_html=True)

    emoji_dict = {
            "Energy Star": "⚡",
            "WiFi Alliance": "📶",
            "EPEAT": "🌎"
        }

    # Sample data iteration - replace 'newest_records' with your actual DataFrame
    
    # Define the number of columns
    num_columns = 2
    conn = st.connection('s3', type=FilesConnection)
    newest_records = conn.read("scoops-finder/computers-data.csv", input_format="csv", ttl=600)
    newest_records = newest_records.sort_values('date_available_on_market', ascending=False)
    newest_records = newest_records.head(10)
    st.write(newest_records)

    rows = [st.columns(num_columns) for _ in range((len(newest_records) + num_columns - 1) // num_columns)]

    # Initialize a counter for DataFrame row indices
    row_index = 0

    # Fill each cell in the grid with content
    for row in rows:
        for col in row:
            if row_index < len(newest_records):
                with col:
                    row_data = newest_records.iloc[row_index]
                    product_name = row_data['model_name']
                    certification_date = row_data['date_available_on_market']
                    brand = row_data['brand_name']
                    product_type = row_data['type']

                    # Embed data into HTML
                    html_content = f"""
                    <div class="card">
                        <div class="content">
                            <p class="heading">{product_name}</p>
                            <p class="para">
                                Brand: {brand}<br>
                                Product Type: {product_type}<br>
                                Certification Date: {certification_date}<br>
                                Source: {source} {emoji}
                            </p>
                        </div>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)

                    row_index += 1
    
def show_raw_data_cert_computers():
    st.write("Coming Soon")
    # Add industry-specific details or requirements.
    conn = st.connection('s3', type=FilesConnection)
    df = conn.read("scoops-finder/computers-data.csv", input_format="csv", ttl=600)
    st.write(df)

def show_changelog_cert_computers():
    st.write("Coming Soon")
def show_insights_cert_computers():
    st.write("Coming Soon")


def display_certifications_televisions():
    st.header("Automotive Certifications")
    st.write("Critical certifications for automotive professionals.")
    # Include relevant data or courses available.

def display_placements_computers():
    st.header("Automotive Certifications")
    st.write("Critical certifications for automotive professionals.")
    # Include relevant data or courses available.

def display_placements_televisions():
    st.header("Automotive Certifications")
    st.write("Critical certifications for automotive professionals.")
    # Include relevant data or courses available.



def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        if 'page' not in st.session_state:
            st.session_state['page'] = 'home'
        
        sidebar()

        # Redirect based on the selected page
        if st.session_state['page'] == 'home':
            display_dashboard()
        elif st.session_state['page'] == 'certifications':
            display_certifications_page()  # Renamed for clarity
        elif st.session_state['page'] == 'placements':
            display_placements_page()  # Renamed for clarity
    else:
        display_login_form()


def page1():
    st.title("Page 1")
    st.write("Welcome to Page 1")
    sidebar()

def display_placements_imaging():
    st.title("Imaging Placements 🖨️")
    st.markdown('---')
    # Define buttons for navigation
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Recent'

    # Create four columns for the interactive tiles
    col1, col2, col3, col4 = st.columns(4)

    # Define interactive tiles that update the session state upon clicking
    if col1.button('Recent 🆕', key='1', use_container_width=True):
        st.session_state['current_page'] = 'Recent'
    if col2.button('Raw Data 📝', key='2', use_container_width=True):
        st.session_state['current_page'] = 'Raw Data'
    if col3.button('Changelog 🔄', key='3', use_container_width=True):
        st.session_state['current_page'] = 'Changelog'
    if col4.button('Insights 🔍', key='4', use_container_width=True):
        st.session_state['current_page'] = 'Insights'

    # Conditional rendering based on selected page
    if st.session_state['current_page'] == 'Recent':
        show_recent()
    elif st.session_state['current_page'] == 'Raw Data':
        show_raw_data()
    elif st.session_state['current_page'] == 'Changelog':
        show_changelog()
    elif st.session_state['current_page'] == 'Insights':
        show_insights()


def show_recent():
    # Code to display recent data
    st.header('Recent Placements')
    conn = st.connection('s3', type=FilesConnection)
    df5 = conn.read("scoops-finder/brand_counts.csv", input_format="csv", ttl=600)
    df5 = df5[-10:]
    df5 = df5.sort_values(by='Brand').reset_index(drop=True)

    # Create metrics for the latest 5 records

    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    wch_colour_font = (0, 0, 0)
    fontsize = 20
    valign = "left"
    iconname = "fas fa-xmark"
        
    container = st.container()

    # Add your placements data here
    conn = st.connection('s3', type=FilesConnection)
    df4 = conn.read("scoops-finder/tracking.csv", input_format="csv", ttl=600)
    df4.drop_duplicates(subset="Product Name", inplace=True)
    df4 = df4.sort_values(by='Date Detected', ascending=True)
    latest_df4 = df4.tail(5)  # Get the latest 5 records
    latest_df4 = latest_df4.iloc[::-1]

    
    st.markdown('''
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* Maintains 3 columns */
        grid-gap: 20px; /* Space between cards */
        padding: 10px;
        width: auto; /* Adjust based on the actual space available or use 100% if it should be fully responsive */
    }

    .card {
        height: auto;
        min-height: 120px;
        position: relative;
        width: 100%; /* This makes each card responsive within its grid column */
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2px;
        border-radius: 24px;
        overflow: hidden;
        line-height: 1.6;
        transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
        margin: 15px; /* Added margin */
    }

    .content {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 24px;
    padding: 20px;
    padding-bottom: 0px;
    border-radius: 22px;
    color: #ffffff;
    overflow: hidden;
    background: #ffffff;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .content .heading {
    font-weight: 600;
    font-size: 20px;
    line-height: 1;
    z-index: 1;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .content .para {
    z-index: 1;
    opacity: 0.8;
    font-size: 16px;
    font-weight: 400;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .card::before {
    content: "";
    position: absolute;
    height: 500%;
    width: 500%;
    border-radius: inherit;
    background: #3775cb;
    background: linear-gradient(to right, #3775cb, #3775cb);
    transform-origin: center;
    animation: moving 9.8s linear infinite paused;
    transition: all 0.88s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .card:hover::before {
    animation-play-state: running;
    z-index: -1;
    width: 20%;
    }

    .card:hover .content .heading,
    .card:hover .content .para {
    color: #000000;
    }

    .card:hover {
    box-shadow: 0rem 6px 13px rgba(10, 60, 255, 0.1),
        0rem 24px 24px rgba(10, 60, 255, 0.09),
        0rem 55px 33px rgba(10, 60, 255, 0.05),
        0rem 97px 39px rgba(10, 60, 255, 0.01), 0rem 152px 43px rgba(10, 60, 255, 0);
    scale: 1.00;
    color: #000000;
    }

    @keyframes moving {
    0% {
        transform: rotate(0);
    }

    100% {
        transform: rotate(360deg);
    }
    }
    </style>
    ''', unsafe_allow_html=True)


    # Sample data iteration - replace 'newest_records' with your actual DataFrame
    # Define the number of columns
    # Provide a layout option for the user to switch
    num_columns = 2

    # Generate rows with the appropriate number of columns
    rows = [st.columns(num_columns) for _ in range((len(latest_df4) + num_columns - 1) // num_columns)]

    # Initialize a counter for DataFrame row indices
    row_index = 0

    # Fill each cell in the grid with content
    for row in rows:
        for col in row:
            if row_index < len(latest_df4):
                with col:
                    row_data = latest_df4.iloc[row_index]
                    brand = row_data['Brand']
                    count = df5[df5['Brand'] == brand]['Count'].values[0]
                    metric_label = row_data['Action']
                    metric_value = row_data['Product Name']
                    metric_delta = str(count)
                    date_detected = row_data['Date Detected']  # Assuming 'Date Detected' is the column name in df4


                    if metric_label == 'Added':
                        title = "New Product Added"
                        emoji = "🆕"
                    elif metric_label == 'Removed':
                        title = "Product Removed"
                        emoji = "❌"
                    else:
                        title = "Certification Spotted"

                    # Embed data into HTML
                    html_content = f"""
                    <div class="card">
                        <div class="content">
                            <p class="heading">{metric_value}</p>
                            <p class="para">
                                {title} {emoji}
                                <br>
                                Brand: {brand}<br>
                                Product Type: {metric_value}<br>
                                Certification Date: {date_detected}<br>
                            </p>
                        </div>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)

                    row_index += 1   

    # Example: st.write(data_recent)

def show_raw_data():
    # Code to display raw data
    st.header('Raw Placement Data')
    conn2 = st.connection('s3', type=FilesConnection)

    # Read data from CSV
    raw_data_placements = conn2.read("scoops-finder/combined_products.csv", input_format="csv", ttl=600)

    # Convert 'Date Detected' to datetime and sort descending
    raw_data_placements['Date Detected'] = pd.to_datetime(raw_data_placements['Date Detected'])
    raw_data_placements.sort_values('Date Detected', ascending=False, inplace=True)

    # Create a list of unique brands for the selectbox, with an 'All Brands' option
    unique_brands = ['All Brands'] + sorted(raw_data_placements['Brand'].unique().tolist())

    # Sidebar to select brand
    selected_brand = st.selectbox('Select a brand to display', unique_brands)

    # Filter data based on selected brand, unless 'All Brands' is selected
    if selected_brand != 'All Brands':
        filtered_data = raw_data_placements[raw_data_placements['Brand'] == selected_brand].reset_index(drop=True)
    else:
        filtered_data = raw_data_placements.reset_index(drop=True)

    # Display the filtered data
    st.write(filtered_data)


def show_changelog():
    # Code to display changelog
    st.header('Changelog')
    conn5 = st.connection('s3', type=FilesConnection)
    placement_tracking5 = conn5.read("scoops-finder/tracking.csv", input_format="csv", ttl=600)
    # Establishing connection and reading the data
    conn = st.connection('s3', type=FilesConnection)
    placement_tracking = conn.read("scoops-finder/tracking.csv", input_format="csv", ttl=600)

    conn = st.connection('s3', type=FilesConnection)
    placement_changelog = conn.read("scoops-finder/brand_counts.csv", input_format="csv", ttl=600)

    # Reshape the DataFrame
    pivoted_df = placement_changelog.pivot_table(index='Date', columns='Brand', values='Count', fill_value=0)
    #pivoted_df = pivoted_df.sort_values('Date', ascending=False)
    pivoted_df = pivoted_df.iloc[::-1]
    # Display the transposed DataFrame


    # Streamlit UI for brand filtering
    st.title('Brand Counts Over Time')
    all_brands = list(pivoted_df.columns)
    selected_brands = st.multiselect('Select Brands', all_brands, default=all_brands)
    # Filter data based on selected brands
    filtered_data = pivoted_df[selected_brands]
    # Display the bar chart
    st.dataframe(filtered_data, use_container_width=True)

def show_insights():
    # Code to display insights
    st.header('Insights')
    # Assuming 'st.connection' and 'FilesConnection' are valid in your environment
    conn = st.connection('s3', type=FilesConnection)
    placement_changelog = conn.read("scoops-finder/brand_counts.csv", input_format="csv", ttl=600)

    # Reshape the DataFrame
    pivoted_df = placement_changelog.pivot_table(index='Date', columns='Brand', values='Count', fill_value=0)
    #pivoted_df = pivoted_df.sort_values('Date', ascending=False)
    pivoted_df = pivoted_df.iloc[::-1]
    # Display the transposed DataFrame


    # Streamlit UI for brand filtering
    st.title('Brand Counts Over Time')
    all_brands = list(pivoted_df.columns)
    selected_brands = st.multiselect('Select Brands', all_brands, default=all_brands)

    # Filter data based on selected brands
    filtered_data = pivoted_df[selected_brands]

    # Display the line chart
    st.line_chart(filtered_data, height=500)

    st.title('Brand Counts Over Time')
    all_brands = list(pivoted_df.columns)
    selected_brands = st.multiselect('Select Brands', all_brands, default=all_brands, key='quarter_range_selector6')

    # Filter data based on selected brands
    filtered_data = pivoted_df[selected_brands]

    # Display the bar chart
    st.bar_chart(filtered_data, height=500)


if __name__ == "__main__":
    main()

    
