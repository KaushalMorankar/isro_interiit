import geopandas as gpd
import pandas as pd
import rasterio
import numpy as np
from rasterio.plot import show
from rasterio.transform import from_bounds
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as mplPolygon
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Paths
albedo_map_path = 'lunar_albedo_map.tif'
output_tiff_path = 'lunar_overlay_with_polygons.tif'
xrf_data_path = 'output.csv'

# Load data
xrf_data = pd.read_csv(xrf_data_path)

# Lunar extent
lunar_extent = {
    'latitude_min': -90,
    'latitude_max': 90,
    'longitude_min': -180,
    'longitude_max': 180
}

# Helper functions
def latitude_longitude_to_pixel(latitude, longitude, width, height, extent):
    x = ((longitude - extent['longitude_min']) / (extent['longitude_max'] - extent['longitude_min'])) * width
    y = ((extent['latitude_max'] - latitude) / (extent['latitude_max'] - extent['latitude_min'])) * height
    return x, y

def handle_wraparound(corners, width):
    split_polygons = []
    adjusted_corners = []
    wraparound = False

    for i in range(len(corners)):
        lon1 = corners[i][0]
        lon2 = corners[(i + 1) % len(corners)][0]

        if abs(lon1 - lon2) > 180:
            wraparound = True
            if lon1 > lon2:
                adjusted_corners.append((width, corners[i][1]))
                split_polygons.append(adjusted_corners)
                adjusted_corners = [(0, corners[(i + 1) % len(corners)][1])]
            else:
                adjusted_corners.append((0, corners[i][1]))
                split_polygons.append(adjusted_corners)
                adjusted_corners = [(width, corners[(i + 1) % len(corners)][1])]
        else:
            adjusted_corners.append(corners[i])

    if wraparound:
        split_polygons.append(adjusted_corners)
    else:
        split_polygons = [adjusted_corners]

    return split_polygons

def overlay_and_save(element, max_val, scale_factor, abundance_threshold):
    with rasterio.open(albedo_map_path) as lunar_albedo:
        meta = lunar_albedo.meta
        albedo_image = lunar_albedo.read(1)  # Load the first band (grayscale)
        width, height = lunar_albedo.width, lunar_albedo.height
        transform = lunar_albedo.transform

    fig = Figure(figsize=(width / 100, height / 100), dpi=100)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.imshow(albedo_image, cmap='gray', extent=(0, width, height, 0))

    cmap = plt.cm.jet
    norm = mcolors.Normalize(vmin=0, vmax=max_val)

    patches = []
    for _, row in xrf_data.iterrows():
        if row[['Lat1', 'Lat2', 'Lat3', 'Lat4']].max() > 81 or row[['Lat1', 'Lat2', 'Lat3', 'Lat4']].min() < -81:
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
                abundance = row[f'Abundance_{element} (%)'] / scale_factor
                if abundance < abundance_threshold:
                    continue

                color = cmap(norm(abundance))
                polygon = mplPolygon(poly_corners, closed=True, edgecolor="none", facecolor=color, alpha=0.3)
                patches.append(polygon)

    p = PatchCollection(patches, match_original=True)
    ax.add_collection(p)
    ax.axis('off')

    canvas.draw()
    combined_image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
    combined_image = combined_image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # Save the overlay as a new TIFF file
    with rasterio.open(
        output_tiff_path,
        'w',
        driver='GTiff',
        height=combined_image.shape[0],
        width=combined_image.shape[1],
        count=3,
        dtype=combined_image.dtype,
        transform=transform
    ) as dst:
        for i in range(3):  # RGB channels
            dst.write(combined_image[:, :, i], i + 1)

    print(f"Overlay saved as {output_tiff_path}")

while(True):
    element = input("Enter element (e to exit): ")
    
    if(element == "e"):
        break

    max_val = int(input("Enter maximum value for colour scale: "))
    scale_factor = float(input("Enter scaling factor for abundance: "))
    abundance_threshold = float(input("Enter abundance threshold for region to be plotted: "))
    overlay_and_save(element, max_val, scale_factor, abundance_threshold)

