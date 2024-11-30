from PIL import Image
import os

def generate_tiles(image_path, output_dir, max_zoom):
    # Open the input image
    image = Image.open(image_path)
    width, height = image.size

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for zoom in range(max_zoom + 1):
        # Calculate the number of tiles per row and column
        tiles_per_side = 2 ** zoom
        tile_width = width // tiles_per_side
        tile_height = height // tiles_per_side

        zoom_dir = os.path.join(output_dir, f"zoom_{zoom}")
        os.makedirs(zoom_dir, exist_ok=True)

        # Generate tiles for the current zoom level
        for row in range(tiles_per_side):
            for col in range(tiles_per_side):
                # Calculate the tile's bounding box
                left = col * tile_width
                upper = row * tile_height
                right = left + tile_width
                lower = upper + tile_height

                # Crop the tile
                tile = image.crop((left, upper, right, lower))

                # Save the tile
                tile_filename = os.path.join(zoom_dir, f"tile_{row}_{col}.png")
                tile.save(tile_filename)

                print(f"Saved: {tile_filename}")

if __name__ == "__main__":
    # Path to the input image
    input_image = "lunar_albedo_map.tif"

    # Output directory for the tiles
    output_directory = "tiles_output"

    # Maximum zoom level
    max_zoom_level = 5

    generate_tiles(input_image, output_directory, max_zoom_level)