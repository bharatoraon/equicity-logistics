# 🏙️ Equicity GeoAI v2.6  
### _GeoAI for Smarter Urban Logistics_

![Equicity Poster](assets/poster.png)

---

## 🌍 Overview

**Equicity GeoAI** is an AI-powered geospatial intelligence platform designed to identify **optimal logistics hubs and corridors** within urban regions.  
By combining **GIS datasets**, **spatial analytics**, and **machine learning-driven suitability modeling**, it supports planners, government agencies, and logistics developers in making **data-backed infrastructure decisions**.

---

## 🧠 Core Idea

> _“Use data, not guesswork, to shape the future of logistics-ready cities.”_

Equicity integrates geospatial datasets, accessibility measures, and environmental parameters to compute a **logistics suitability index (LSI)**.  
The app visualizes suitability zones interactively using Folium and provides downloadable GeoJSON outputs for GIS-based planning and analysis.

---

## ⚙️ Features

✅ AI-driven spatial suitability modeling  
✅ Multi-criteria weighting (Manual / AHP-ready)  
✅ Integration with both **vector** and **raster** data  
✅ Dynamic Folium map with legend and auto-centering  
✅ GeoJSON export for further analysis  
✅ Clean UI with persistent map display and branding  

---

## 🗺️ Required Datasets (8 Layers)

| Dataset | Description | Format |
|----------|--------------|--------|
| 🗺️ District Boundary | Study area boundary | `.geojson` / `.shp` |
| 🛣️ Road Network | DRRP / National / State highways | `.geojson` / `.shp` |
| 🏭 Industrial Locations | Points of industries / clusters | `.csv` / `.geojson` |
| 🏢 Depots & Warehouses | Logistics & storage facilities | `.csv` / `.geojson` |
| 🚆 Railway Network | Line features for connectivity | `.geojson` / `.shp` |
| 🌿 LULC | Land Use Land Cover or zoning | `.tif` / `.geojson` |
| ⛰️ DEM | Elevation or slope raster | `.tif` / `.tiff` |
| 👥 Population / Workforce | Density or worker concentration | `.csv` / `.geojson` |

---

## 🧩 Technical Workflow

1. Upload the 8 required datasets  
2. Choose manual weights for each factor (or default)  
3. The app generates a **hexagonal grid** and computes suitability metrics  
4. Suitability index is classified as **Low / Medium / High**  
5. Results are visualized interactively on the Folium map  
6. Export the results as GeoJSON for QGIS / ArcGIS / Kepler.gl  

---

## 💻 How to Run Locally

```bash
# 1️⃣ Clone the repository
git clone https://github.com/bharatoraon/equicity-logistics.git
cd equicity-geoai

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Run the Streamlit app
python -m streamlit run app.py

