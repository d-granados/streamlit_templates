import streamlit as st
from PIL import Image
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from packaging import version


@st.cache_data
def load_data():
    return pd.read_csv('penguins.csv')

def get_logo_path(background_color):
    if background_color == "#0E1117":
        return "white_logo.png", "white_icon.png"
    else:
        return "logo.png", "icon.png"

# Get Streamlit version and background color
streamlit_version = st.__version__
background_color = st.get_option('theme.backgroundColor')

# Determine logo paths
logo_path, icon_path = get_logo_path(background_color)

# Display logo (for Streamlit version 1.35.0 or higher)
if version.parse(streamlit_version) >= version.parse("1.35.0"):
    st.logo(image=logo_path, icon_image=icon_path)
    display_sidebar_image = False
else:
    display_sidebar_image = True

# Set up the sidebar
with st.sidebar:
    if display_sidebar_image:
        logo_image = Image.open(logo_path)
        st.image(logo_image, width=250)
    st.title("Sidebar")

# Set up tabs
home_tab, pinguins_tab, about_tab = st.tabs(["Home", "Data", "About"])

with home_tab:
    st.title("Home")
    st.write("Welcome to the home tab.")

with pinguins_tab:

    df = load_data()

    st.title("Penguins Dataset Interactive Plot")

    # Dropdowns for selecting x and y axes
    x_axis_col, y_axis_col= st.columns(2)

    with x_axis_col:
        x_axis = st.selectbox("Select X-axis variable", df.columns)

    with y_axis_col:
        y_axis = st.selectbox("Select Y-axis variable", df.columns)

    # Slider to filter data based on bill length
    min_val, max_val = int(df["bill_length_mm"].min()), int(df["bill_length_mm"].max())
    bill_length = st.slider("Select Bill Length Range", min_val, max_val, (min_val, max_val))

    # Checkbox to show/hide species in the plot
    show_species = st.checkbox("Color by Species", value=True)

    # Filter the dataframe based on the slider value
    filtered_df = df[(df["bill_length_mm"] >= bill_length[0]) & (df["bill_length_mm"] <= bill_length[1])]

    # Create the plot
    fig, ax = plt.subplots()

    if show_species:
        sns.scatterplot(data=filtered_df, x=x_axis, y=y_axis, hue="species", ax=ax)
        plt.legend(title='Species')
    else:
        sns.scatterplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)

    plt.title(f'{y_axis} vs {x_axis}')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    st.pyplot(fig)

with about_tab:
    st.title("About this App")