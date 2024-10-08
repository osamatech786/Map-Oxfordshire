import folium
import requests
import streamlit as st
from streamlit.components.v1 import html
import csv

st.set_page_config(
    page_title="Prevista - Oxfordshire",
    page_icon="https://lirp.cdn-website.com/d8120025/dms3rep/multi/opt/social-image-88w.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Define specific places to highlight (example coordinates)
places = {}
csv_file_path = 'places.csv'
with open(csv_file_path, mode='r') as file:
    reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV file
    for row in reader:
        # Extract data from the row
        place = row['Place']
        latitude = float(row['Latitude'])
        longitude = float(row['Longitude'])
        info = row['Info']
        
        # Update the dictionary
        places[place] = {
            'location': (latitude, longitude),
            'info': info
        }
        

# Load the Oxfordshire GeoJSON data
@st.cache_data
def load_oxfordshire_data():
    url = 'https://raw.githubusercontent.com/glynnbird/ukcountiesgeojson/master/oxfordshire.geojson'
    response = requests.get(url)
    geojson_data = response.json()
    return geojson_data

def create_map(oxfordshire_geojson):
    # Extract coordinates from the GeoJSON
    coords = oxfordshire_geojson['geometry']['coordinates'][0]
    oxfordshire_center = [
        (sum(lat for lon, lat in coords) / len(coords),
         sum(lon for lon, lat in coords) / len(coords))
    ]
    # Adjust the zoom level here
    m = folium.Map(location=oxfordshire_center[0], zoom_start=10)  # Increased zoom level for a closer view

    # Add Oxfordshire boundary
    folium.GeoJson(
        oxfordshire_geojson,
        style_function=lambda x: {'fillColor': 'lightblue', 'color': 'black', 'weight': 2}
    ).add_to(m)

    # Add markers for specific places
    for place, details in places.items():
        folium.Marker(
            location=details["location"],
            popup=folium.Popup(details["info"], max_width=300),
            tooltip=place,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    return m

def main():
    st.title('Oxfordshire Map - UK')

    # Load and filter data
    oxfordshire_geojson = load_oxfordshire_data()

    # Create and display map
    m = create_map(oxfordshire_geojson)
    st.write("### Organisations Oxford")

    # Increase the height to ensure the map is visible and sufficiently large
    html_string = m._repr_html_()
    html(html_string, height=600)  # Adjust height here as needed

if __name__ == "__main__":
    main()

# pip install folium requests streamlit
# streamlit run app.py
# Dev : https://linkedin.com/in/osamatech786
