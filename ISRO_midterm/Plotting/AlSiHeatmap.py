import geopandas as gpd
import pandas as pd
import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
from matplotlib.patches import Polygon as mplPolygon
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors

# Path to the lunar map
map_path = r'D:\Interiit_isro\2024\lunar_map.tif'  # Adjust to your actual file path

# Define the known extent of the lunar map image
lunar_extent = {
    'latitude_min': -90,
    'latitude_max': 90,
    'longitude_min': -180,
    'longitude_max': 180
}

# Load the XRF data
xrf_data = pd.read_csv('D:\\Interiit_isro\\2024\\output.csv')

# Plotting function to convert latitude/longitude to image coordinates
def latitude_longitude_to_pixel(latitude, longitude, width, height, extent):
    x = ((longitude - extent['longitude_min']) / (extent['longitude_max'] - extent['longitude_min'])) * width
    y = ((extent['latitude_max'] - latitude) / (extent['latitude_max'] - extent['latitude_min'])) * height
    return x, y

# Check if the polygon crosses the -180/180 degree boundary and split if necessary
def handle_wraparound(corners, width):
    split_polygons = []
    adjusted_corners = []
    wraparound = False

    for i in range(len(corners)):
        lon1 = corners[i][0]
        lon2 = corners[(i + 1) % len(corners)][0]

        # Check if there's a large jump in longitude, indicating a wraparound
        if abs(lon1 - lon2) > 180:
            wraparound = True
            if lon1 > lon2:
                adjusted_corners.append((width, corners[i][1]))  # Edge point at 180
                split_polygons.append(adjusted_corners)
                adjusted_corners = [(0, corners[(i + 1) % len(corners)][1])]  # Edge point at -180
            else:
                adjusted_corners.append((0, corners[i][1]))  # Edge point at -180
                split_polygons.append(adjusted_corners)
                adjusted_corners = [(width, corners[(i + 1) % len(corners)][1])]  # Edge point at 180
        else:
            adjusted_corners.append(corners[i])

    if wraparound:
        split_polygons.append(adjusted_corners)
    else:
        split_polygons = [adjusted_corners]

    return split_polygons

# Main plotting function
def plot_abundance_heatmap(max_val):
    fig, ax = plt.subplots(figsize=(10, 10))
    thresh=17
    # Load the lunar map if available
    try:
        with rasterio.open(map_path) as lunar_map:
            show(lunar_map, ax=ax, cmap='gray')
            width = lunar_map.width
            height = lunar_map.height
    except FileNotFoundError:
        print("Lunar map file not found. Proceeding with only XRF coverage regions.")
        width, height = 1024, 512  # Assume image dimensions if missing

    cmap = plt.cm.jet
    # Set the scale
    norm = mcolors.Normalize(vmin=0, vmax=max_val)

    # Create patches for XRF data regions
    patches = []
    for _, row in xrf_data.iterrows():
        if(row['Lat1'] > 81 or row['Lat2'] > 81 or row['Lat3'] > 81 or row['Lat4'] > 81 or row['Lat1'] < -81 or row['Lat2'] < -81 or row['Lat3'] < -81 or row['Lat4'] < -81):
            continue
        if(row[f'Abundance_Mg (%)']>thresh or row[f'Abundance_Al (%)']>thresh or row[f'Abundance_Si (%)']>thresh or row[f'Abundance_Ca (%)']>thresh or row[f'Abundance_Fe (%)']>thresh):
            continue
        corners = [
            latitude_longitude_to_pixel(row['Lat1'], row['Lon1'], width, height, lunar_extent),
            latitude_longitude_to_pixel(row['Lat2'], row['Lon2'], width, height, lunar_extent),
            latitude_longitude_to_pixel(row['Lat3'], row['Lon3'], width, height, lunar_extent),
            latitude_longitude_to_pixel(row['Lat4'], row['Lon4'], width, height, lunar_extent)
        ]
        
        split_polygons = handle_wraparound(corners, width)
        
        for poly_corners in split_polygons:
            if len(poly_corners) > 2:
                # Color the polygon based on the selected element's abundance
                abundance = (row[f'Abundance_Al (%)']/1.2)/row[f'Abundance_Si (%)']
                
                color = cmap(norm(abundance))
                polygon = mplPolygon(poly_corners, closed=True, edgecolor="none", facecolor=color, alpha=0.6)
                patches.append(polygon)

    # Add polygons to plot
    p = PatchCollection(patches, match_original=True)
    ax.add_collection(p)

    # Set ticks to reflect latitude and longitude
    set_lat_lon_ticks(ax, width, height, lunar_extent)
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)

    ax.set_title(f"XRF Coverage Regions - Al/Si Ratio Heatmap")
    plt.xlabel("Longitude (degrees)")
    plt.ylabel("Latitude (degrees)")
    plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label=f'Ratio')
    plt.show()

# Adjust x- and y-ticks to reflect actual latitude and longitude
def set_lat_lon_ticks(ax, width, height, extent):
    x_ticks_pixels = ax.get_xticks()
    y_ticks_pixels = ax.get_yticks()

    x_ticks_lon = [(tick / width) * (extent['longitude_max'] - extent['longitude_min']) + extent['longitude_min'] for tick in x_ticks_pixels]
    y_ticks_lat = [extent['latitude_max'] - (tick / height) * (extent['latitude_max'] - extent['latitude_min']) for tick in y_ticks_pixels]

    ax.set_xticks(x_ticks_pixels)
    ax.set_xticklabels([f"{lon:.1f}" for lon in x_ticks_lon])

    ax.set_yticks(y_ticks_pixels)
    ax.set_yticklabels([f"{lat:.1f}" for lat in y_ticks_lat])

max_val = 1.5
plot_abundance_heatmap(max_val)