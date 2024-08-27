import folium
import requests
import streamlit as st
from streamlit.components.v1 import html

# Define specific places to highlight (example coordinates)
places = {
    "Oxford": {"location": (51.754816, -1.254367), "info": "Oxford - University City"},
    "Bicester": {"location": (51.8984, -1.1514), "info": "Bicester - Market Town"}
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
    m = folium.Map(location=oxfordshire_center[0], zoom_start=9)  # Increased zoom level for a closer view

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
    html(html_string, height=800)  # Adjust height here as needed

if __name__ == "__main__":
    main()

# streamlit run app.py
# Dev : https://linkedin.com/in/osamatech786
