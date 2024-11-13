import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import cm
from fastapi import HTTPException

class PlotService:
    def __init__(self, albedo_map_path: str, xrf_data_path: str):
        self.albedo_map_path = albedo_map_path
        self.xrf_data_path = xrf_data_path
        self.lunar_extent = {
            'latitude_min': -90,
            'latitude_max': 90,
            'longitude_min': -180,
            'longitude_max': 180
        }
        self.xrf_data = pd.read_csv(xrf_data_path)

    def latitude_longitude_to_pixel(self, latitude, longitude, width, height, extent):
        x = ((longitude - extent['longitude_min']) / (extent['longitude_max'] - extent['longitude_min'])) * width
        y = ((extent['latitude_max'] - latitude) / (extent['latitude_max'] - extent['latitude_min'])) * height
        return x, y

    def handle_wraparound(self, corners, width):
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

    def generate_plot(self, max_val: int):
        fig, ax = plt.subplots(figsize=(10, 10))

        try:
            # Placeholder for lunar albedo map logic
            # Load lunar map if available
            ax.set_title(f"Generated Plot - Max Value: {max_val}")
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Lunar albedo map not found: {str(e)}")

        # Normalize for color scaling
        cmap = cm.jet
        norm = plt.Normalize(vmin=0, vmax=max_val)

        # Create patches for XRF data regions
        patches = []
        for _, row in self.xrf_data.iterrows():
            if(row['Lat1'] > 81 or row['Lat2'] > 81 or row['Lat3'] > 81 or row['Lat4'] > 81 or row['Lat1'] < -81 or row['Lat2'] < -81 or row['Lat3'] < -81 or row['Lat4'] < -81):
                continue

            corners = [
                self.latitude_longitude_to_pixel(row['Lat1'], row['Lon1'], 1024, 512, self.lunar_extent),
                self.latitude_longitude_to_pixel(row['Lat2'], row['Lon2'], 1024, 512, self.lunar_extent),
                self.latitude_longitude_to_pixel(row['Lat3'], row['Lon3'], 1024, 512, self.lunar_extent),
                self.latitude_longitude_to_pixel(row['Lat4'], row['Lon4'], 1024, 512, self.lunar_extent)
            ]
            
            split_polygons = self.handle_wraparound(corners, 1024)
            
            for poly_corners in split_polygons:
                if len(poly_corners) > 2:
                    abundance = (row[f'Abundance_Mg (%)'])/row[f'Abundance_Al (%)']
                    color = cmap(norm(abundance))
                    polygon = plt.Polygon(poly_corners, closed=True, edgecolor="none", facecolor=color, alpha=0.6)
                    patches.append(polygon)

        # Add polygons to plot
        ax.add_collection(plt.collections.PatchCollection(patches, match_original=True))

        # Save the plot to an in-memory buffer
        buf = io.BytesIO()
        canvas = FigureCanvas(fig)
        canvas.print_png(buf)
        buf.seek(0)
        return buf
