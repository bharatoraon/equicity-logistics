import streamlit as st
from geoai_engine import run_geoai_model
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon

st.set_page_config(
    page_title="Equicity GeoAI v1.0 — Smart Urban Logistics",
    page_icon="assets/favicon.png",
    layout="wide"
)
st.title("Equicity GeoAI v1.0 — Folium Edition")
st.markdown("### GeoAI for Smarter Urban Logistics")
st.image("assets/poster.png", use_container_width=True)
st.markdown("""
This interactive web application identifies **logistics hub and corridor suitability**
based on spatial datasets, infrastructure connectivity, and environmental conditions.
It integrates **AI-driven spatial analytics** with **GIS visualization**
to support data-backed decision-making for **urban logistics planning**.
""")
st.divider()
st.sidebar.header("Controls Panels")

with st.sidebar.expander("📂 Data Upload (8 datasets)", expanded=True):
    district = st.file_uploader("🗺️ District Boundary", type=['geojson', 'shp'], key='district')
    roads = st.file_uploader("🛣️ Road Network", type=['geojson', 'shp'], key='roads')
    industries = st.file_uploader("🏭 Industrial Locations", type=['csv', 'geojson'], key='industries')
    depots = st.file_uploader("🏢 Depots & Warehouses", type=['geojson', 'csv'], key='depots')
    railways = st.file_uploader("🚆 Railway Network", type=['geojson', 'shp'], key='railways')
    lulc = st.file_uploader("🌿 LULC", type=['geojson', 'tif', 'tiff'], key='lulc')
    dem = st.file_uploader("⛰️ DEM", type=['tif', 'tiff'], key='dem')
    population = st.file_uploader("👥 Population", type=['geojson', 'csv'], key='population')
    
with st.sidebar.expander("⚖️ Weighting Options", expanded=True):
    use_manual = st.checkbox("Use manual weights", value=True)
    criteria = [
        'road_access', 'rail_access', 'industry_proximity',
        'depot_density', 'lulc_score', 'terrain_suitability', 'population_score'
    ]
    manual = None
    if use_manual:
        manual = {c: st.slider(c.replace('_', ' ').title(), 0.0, 1.0, 0.15, 0.05) for c in criteria}
        total = sum(manual.values()) or 1
        manual = {k: v / total for k, v in manual.items()}

with st.sidebar.expander("⚙️ Run & Export", expanded=True):
    run_button = st.button("🚀 Run Model")

uploaded = [
    district, roads, industries, depots,
    railways, lulc, dem, population
]
uploaded_files = [f for f in uploaded if f]

if len(uploaded_files) < 8:
    st.warning("Please upload all 8 datasets.")
else:
    if run_button:
        with st.spinner("Running model..."):
            grid, summary = run_geoai_model(uploaded_files)
        st.session_state['grid'] = grid
        st.session_state['summary'] = summary
        st.session_state['map_ready'] = False

    if 'grid' in st.session_state:
        grid = st.session_state['grid']
        summary = st.session_state['summary']

        st.subheader("📊 Summary")
        st.json(summary)

        import folium
        from streamlit_folium import st_folium


        color_map = {'Low': '#f94144', 'Medium': '#f9c74f', 'High': '#43aa8b'}

        try:
            center = grid.geometry.unary_union.centroid
            lon, lat = float(center.x), float(center.y)
        except Exception:
            lon, lat = 78.0, 11.0

        if 'map_ready' not in st.session_state:
            st.session_state['map_ready'] = False

        if st.button("🗺️ Show Suitability Map") or st.session_state['map_ready']:
            st.session_state['map_ready'] = True

            m = folium.Map(location=[lat, lon], zoom_start=10, tiles='CartoDB positron')

            for cls, df in grid.groupby('suitability_class'):
                df = df[df.geometry.apply(lambda g: isinstance(g, (Polygon, MultiPolygon)))].copy()
                df = df.drop(columns=['centroid'], errors='ignore')
                if len(df) == 0:
                    continue
                gj = df.__geo_interface__
                color = color_map.get(str(cls), '#cccccc')
                folium.GeoJson(
                    gj,
                    style_function=lambda feature, col=color: {
                        'fillColor': col,
                        'color': 'black',
                        'weight': 0.4,
                        'fillOpacity': 0.6
                    },
                    name=f"{cls} Suitability"
                ).add_to(m)

            
            legend = '''
            <div style="position: fixed; bottom: 50px; left: 50px; width: 150px; height: 110px;
                        border:2px solid grey; z-index:9999; font-size:14px; background-color:white; padding:10px;">
            <b>Suitability Legend</b><br>
            <i style="background:#43aa8b; width:18px; height:18px; display:inline-block; margin-right:8px;"></i> High<br>
            <i style="background:#f9c74f; width:18px; height:18px; display:inline-block; margin-right:8px;"></i> Medium<br>
            <i style="background:#f94144; width:18px; height:18px; display:inline-block; margin-right:8px;"></i> Low
            </div>
            '''
            m.get_root().html.add_child(folium.Element(legend))

            st.subheader("🌈 Folium Suitability Map with Legend")
            st_folium(m, width=900, height=700)

        
        if st.button("🔄 Reset Map"):
            st.session_state['map_ready'] = False
            st.success("Map reset. Click 'Show Suitability Map' to render again.")

      
        export_grid = grid.drop(columns=['centroid'], errors='ignore')
        geojson_data = export_grid.to_json()
        st.download_button(
            "📥 Download GeoJSON",
            data=geojson_data.encode('utf-8'),
            file_name="equicity_suitability.geojson",
            mime="application/json"
        )

st.caption("© 2025 Buildsoc — GeoAI for Cities & Communities")
