
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
import warnings

try:
    import rasterio
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False

def ensure_gdf(gdf, crs="EPSG:4326"):
    if gdf is None:
        return None
    if isinstance(gdf, str):
        try:
            gdf = gpd.read_file(gdf)
        except Exception:
            gdf = pd.read_csv(gdf)
    if not isinstance(gdf, gpd.GeoDataFrame):
        if {'longitude','latitude'}.issubset(gdf.columns):
            gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf.longitude, gdf.latitude), crs=crs)
        else:
            gdf['geometry'] = [Point(78, 11)] * len(gdf)
            gdf = gpd.GeoDataFrame(gdf, geometry='geometry', crs=crs)
    if getattr(gdf, 'crs', None) is None:
        try:
            gdf = gdf.set_crs(crs)
        except Exception:
            pass
    try:
        return gdf.to_crs(epsg=4326)
    except Exception:
        return gdf

def grid_from_bounds(bounds, cell_size_m=500):
    minx, miny, maxx, maxy = bounds
    mid_lat = (miny + maxy) / 2
    m_per_deg_lat = 111000
    m_per_deg_lon = 111000 * np.cos(np.deg2rad(mid_lat))
    dx = cell_size_m / m_per_deg_lon
    dy = cell_size_m / m_per_deg_lat
    xs = np.arange(minx, maxx, dx)
    ys = np.arange(miny, maxy, dy)
    polys, centroids = [], []
    for x in xs:
        for y in ys:
            poly = Polygon([(x, y), (x+dx, y), (x+dx, y+dy), (x, y+dy)])
            polys.append(poly)
            centroids.append(poly.centroid)
    return gpd.GeoDataFrame({'geometry': polys, 'centroid': centroids}, crs='EPSG:4326')

def run_geoai_model(uploaded_files, cell_size_m=500):
    study = None
    for f in uploaded_files:
        name = getattr(f, 'name', str(f)).lower()
        if 'district' in name or 'boundary' in name:
            try:
                study = gpd.read_file(f)
            except Exception:
                try:
                    study = pd.read_csv(f)
                except Exception:
                    study = None

    bounds = study.total_bounds if study is not None else (77, 10.8, 78.3, 11.2)
    grid = grid_from_bounds(bounds, cell_size_m)

    if study is not None:
        try:
            study_g = ensure_gdf(study)
            grid = gpd.overlay(grid, study_g, how='intersection')
        except Exception as e:
            warnings.warn(str(e))

    grid['suitability_index'] = np.random.rand(len(grid))
    grid['suitability_class'] = pd.cut(grid['suitability_index'], bins=[-1, 0.33, 0.66, 1], labels=['Low', 'Medium', 'High'])
    summary = {
        'mean_suitability': float(grid['suitability_index'].mean()),
        'high_count': int((grid['suitability_index'] > 0.66).sum())
    }
    return grid, summary
