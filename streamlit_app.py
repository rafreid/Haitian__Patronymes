import streamlit as st
import pandas as pd
import pydeck as pdk
from collections import defaultdict
import csv

# City coordinates
HAITI_CITIES = {
    'ABRICOTS': [18.6287, -74.3037],
    'ANGLAIS': [18.3047, -73.8878],
    'ANSE A GALETS': [18.8344, -72.8664],
    'ANSE D\'HAINAULT': [18.5070, -74.4737],
    'ANSE-A-FOLEUR': [19.8728, -72.7808],
    'ANSE-A-PITRE': [18.0444, -71.7575],
    'ANSE-A-VEAU': [18.5006, -73.3406],
    'AQUIN': [18.2797, -73.3875],
    'ARCAHAIE': [18.8375, -72.5153],
    'ARNAUD': [18.4247, -73.8964],
    'ARNIQUET': [18.2603, -73.9333],
    'BAHON': [19.6667, -72.1333],
    'BAIE DE HENNE': [19.6739, -73.1844],
    'BAINET': [18.2667, -72.7333],
    'BARADERES': [18.4833, -73.6333],
    'BAS LIMBE': [19.7000, -72.4000],
    'BASSIN BLEU': [19.7000, -72.8333],
    'BEAUMONT': [18.5500, -73.9667],
    'BELLADERE': [18.9500, -71.9333],
    'BELLE ANSE': [18.2381, -72.0956],
    'BOMBARDOPOLIS': [19.7167, -73.0833],
    'BONBON': [18.5333, -74.2333],
    'BORGNE': [19.8500, -72.5333],
    'BOUCAN CARRE': [19.0333, -72.0833],
    'CABARET': [18.7333, -72.4333],
    'CAMP-PERRIN': [18.3333, -73.8500],
    'CAPOTILLE': [19.7167, -71.8333],
    'CARACOL': [19.6833, -72.0167],
    'CARICE': [19.3333, -71.9333],
    'CAVAILLON': [18.3000, -73.6667],
    'CAYES': [18.2000, -73.7500],
    'CAYES JACMEL': [18.2333, -72.4500],
    'CERCA CARVAJAL': [19.1167, -71.9500],
    'CERCA LA SOURCE': [19.1667, -71.9500],
    'CHAMBELLAN': [18.5500, -74.3167],
    'CHANTAL': [18.2000, -73.8833],
    'CHAPELLE': [19.1333, -72.8333],
    'CHARDONNIERES': [18.2833, -74.1667],
    'CITE-SOLEIL': [18.5819, -72.3365],
    'CORAIL': [18.5500, -74.1333],
    'CORNILLON': [18.6833, -71.9500],
    'COTE-DE-FER': [18.1333, -73.1000],
    'DAME-MARIE': [18.5611, -74.4208],
    'DESDUNES': [19.3333, -72.7000],
    'DESSALINES': [19.2617, -72.5161],
    'DONDON': [19.5167, -72.2500],
    'ENNERY': [19.4833, -72.4833],
    'FERRIER': [19.6167, -71.8500],
    'FONDS DES NEGRES': [18.4000, -73.4333],
    'FONDS-VERRETTES': [18.3964, -71.8706],
    'FORT-LIBERTE': [19.6625, -71.8381],
    'GANTHIER': [18.5600, -72.1100],
    'GRAND-GOSIER': [18.1333, -71.9667],
    'GRAND-GOAVE': [18.4333, -72.7667],
    'GRANDE SALINE': [19.2000, -72.7667],
    'GRDE RIVIERE DU NORD': [19.5778, -72.1767],
    'GRESSIER': [18.5406, -72.5269],
    'GROS MORNE': [19.6667, -72.6833],
    'HINCHE': [19.1500, -72.0167],
    'JEAN RABEL': [19.8500, -73.1917],
    'JEREMIE': [18.6397, -74.1169],
    'KENSCOFF': [18.4478, -72.2844],
    'L\'ASILE': [18.4833, -73.4167],
    'L\'ACUL DU NORD': [19.6500, -72.2833],
    'L\'ANSE ROUGE': [19.6167, -73.0333],
    'L\'ARCAHAIE': [18.7728, -72.5156],
    'L\'ESTERE': [19.2667, -72.7000],
    'L\'ILE A VACHE': [18.0667, -73.6833],
    'LA TORTUE': [20.0333, -72.7833],
    'LA VALLEE': [18.3500, -72.3667],
    'LASCAHOBAS': [18.8333, -71.9333],
    'LES IROIS': [18.4028, -74.4500],
    'LIMBE': [19.7000, -72.4000],
    'LIMONADE': [19.6667, -72.1333],
    'MAISSADE': [19.1667, -72.1333],
    'MANICHE': [18.3167, -73.7333],
    'MARMELADE': [19.5000, -72.3500],
    'MARIGOT': [18.2319, -72.3125],
    'MILOT': [19.6167, -72.2167],
    'MIRAGOANE': [18.4500, -73.0833],
    'MIREBALAIS': [18.8333, -72.1000],
    'MOLE ST NICOLAS': [19.8000, -73.3833],
    'MOMBIN CROCHU': [19.3667, -71.8833],
    'MONT-ORGANISE': [19.6667, -71.9333],
    'MORON': [18.5667, -74.2500],
    'OUANAMINTHE': [19.5500, -71.7250],
    'PAILLANT': [18.4500, -73.4333],
    'PERCHES': [19.6333, -71.9500],
    'PESTEL': [18.5389, -73.8897],
    'PETION-VILLE': [18.5127, -72.2855],
    'PETIT-GOAVE': [18.4311, -72.8667],
    'PETIT-TROU-DE-NIPPES': [18.4667, -73.5000],
    'PETITE RIVIERE': [19.1167, -72.5000],
    'PETITE-RIVIERE': [19.1167, -72.5000],
    'PIGNON': [19.3333, -72.1167],
    'PILATE': [19.6333, -72.5333],
    'PLAINE DU NORD': [19.6833, -72.2667],
    'PLAISANCE': [19.5933, -72.4683],
    'POINTE A RAQUETTE': [18.8333, -72.8500],
    'PORT MARGOT': [19.7833, -72.4167],
    'PORT-A-PIMENT': [18.2333, -74.0000],
    'PORT-AU-PRINCE': [18.5944, -72.3074],
    'PORT-DE-PAIX': [19.9392, -72.8306],
    'PORT-SALUT': [18.0833, -73.9167],
    'QUARTIER MORIN': [19.6833, -72.1500],
    'RANQUITE': [19.3833, -72.0833],
    'ROCHE A BATEAU': [18.1833, -73.9333],
    'ROSEAUX': [18.5833, -74.0333],
    'SAINT JEAN DU SUD': [18.1833, -73.8500],
    'SAINT LOUIS DU SUD': [18.2667, -73.5333],
    'SAINT LOUIS NORD': [19.8667, -72.6667],
    'SAINT MARC': [19.1082, -72.6932],
    'SAINT RAPHAEL': [19.4333, -72.2000],
    'SAINT-MICHEL': [19.3667, -72.3333],
    'SAINTE SUZANNE': [19.5833, -72.1667],
    'SAUT D\'EAU': [18.9333, -72.2167],
    'SAVANETTE': [18.9500, -71.9500],
    'TABARRE': [18.5778, -72.2972],
    'TERRE-NEUVE': [19.4833, -72.7167],
    'TERRIER ROUGE': [19.6833, -72.1333],
    'THIOTTE': [18.2500, -71.8500],
    'THOMASSIQUE': [19.2333, -71.8500],
    'THOMAZEAU': [18.6500, -72.0833],
    'THOMONDE': [19.0500, -71.9500],
    'TIBURON': [18.3297, -74.3944],
    'TORBECK': [18.1833, -73.8167],
    'TROU DU NORD': [19.6167, -72.0250],
    'VALLIERES': [19.4333, -71.9333],
    'VERRETTES': [19.0500, -72.4667],
    'VICTOIRE': [19.5167, -72.2500]
}

@st.cache_data
def load_data():
    df = pd.read_csv('Haitian_patronymes.csv')
    
    # Create city-level aggregation
    city_data = defaultdict(list)
    for city in HAITI_CITIES.keys():
        city_names = df[df['CITY'] == city].sort_values('COUNT', ascending=False)
        top_names = [f"{row['NAME']}: {row['COUNT']}" for _, row in city_names.head(10).iterrows()]
        lat, lon = HAITI_CITIES[city]
        city_data['city'].append(city)
        city_data['lat'].append(lat)
        city_data['lon'].append(lon)
        city_data['top_names'].append('<br>'.join(top_names))
    
    return pd.DataFrame(city_data)

# Set up the app
st.title('Haitian Patronymes')
st.text('Top 10 Haitian patronymes by city - excluding first-name-last-names like JEAN, JOSEPH, PIERRE, etc')

# Load the processed data
df = load_data()

# Create the map
view_state = pdk.ViewState(
    latitude=18.9712,
    longitude=-72.2852,
    zoom=7,
    pitch=0
)

tooltip = {
    "html": "<b>{city}</b><br>{top_names}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

layer = pdk.Layer(
    'ScatterplotLayer',
    df,
    get_position=['lon', 'lat'],
    get_radius=1000,
    get_fill_color=[255, 140, 0],
    pickable=True
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9',
    tooltip=tooltip
)

st.pydeck_chart(deck)
st.text('CItadier S.A. (C) 2025')
