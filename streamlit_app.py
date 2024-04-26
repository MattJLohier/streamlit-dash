import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from st_files_connection import FilesConnection
import hashlib
from io import BytesIO
from PIL import Image
import requests

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
    st.sidebar.image("https://i.postimg.cc/XJdg0y7b/scooper-logo.png", use_column_width=True)  # Adjust the image path as needed
    st.sidebar.markdown("---")
    # Set up a container for the buttons
    button_container = st.sidebar.container()
    
    # Inject CSS to make container's children (buttons) 100% width
    st.sidebar.markdown("""
    <style>
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
        background-color: #0056b3;       /* Set active state background color */
        color: white;                    /* Set text color in active state */
    }
    </style>
    """, unsafe_allow_html=True)
    
    with button_container:
        if st.button("Home", key="home_button"):
            st.session_state['page'] = 'home'
        if st.button("Certifications", key="certifications_button"):
            st.session_state['page'] = 'certifications'
        if st.button("Placements", key="placements_button"):
            st.session_state['page'] = 'placements'


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
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if st.session_state['logged_in']:
        if 'page' not in st.session_state:
            st.session_state['page'] = 'home'
        sidebar()
        if st.session_state['page'] == 'home':
            display_dashboard()
        elif st.session_state['page'] == 'certifications':
            page3()
        elif st.session_state['page'] == 'placements':
            page2()
    else:
        display_login_form()


def page1():
    st.title("Page 1")
    st.write("Welcome to Page 1")
    sidebar()



def page2():
    st.header('Placements 💡')
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
    st.subheader('Recent Certifications')
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
    border-radius: 22px;
    color: #ffffff;
    overflow: hidden;
    background: #ffffff;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .content .heading {
    font-weight: 700;
    font-size: 20px;
    line-height: 1;
    z-index: 1;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .content .para {
    z-index: 1;
    opacity: 0.8;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .card::before {
    content: "";
    position: absolute;
    height: 300%;
    width: 300%;
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
    num_columns = 2
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
                                Brand: {brand}<br>
                                Product Type: {metric_value}<br>
                                Certification Date: {date_detected}<br>
                                Source: {title} {emoji}
                            </p>
                        </div>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)

                    row_index += 1   

    # Example: st.write(data_recent)

def show_raw_data():
    # Code to display raw data
    st.subheader('Raw Certification Data')

def show_changelog():
    # Code to display changelog
    st.subheader('Changelog')
    # Example: st.write(data_changelog)

def show_insights():
    # Code to display insights
    st.subheader('Insights')
    # Example: st.write(data_insights)


def page3():
    st.header('Certifications 📝')

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
    
    st.subheader('Recent Certifications')
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
        min-height: 500px;
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
    border-radius: 15px;
    color: #ffffff;
    overflow: hidden;
    background: #ffffff;
    transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .content .heading {
    font-weight: 600;
    font-size: 24px;
    line-height: 1.3;
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
    height: 300%;
    width: 300%;
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
    st.header('Raw Certification Data 📝')
    st.subheader('Energy Star ⚡')
    st.subheader('WiFi Alliance 📶')
    st.subheader('EPEAT 🌎')

def show_changelog_cert():
    # Code to display changelog
    st.subheader('Changelog')
    # Example: st.write(data_changelog)

def show_insights_cert():
    # Code to display insights
    st.subheader('Insights')
    # Example: st.write(data_insights)


if __name__ == "__main__":
    main()

    
