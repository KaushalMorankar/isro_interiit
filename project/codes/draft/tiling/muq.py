import subprocess
import os

def convert_tiff_to_tiles(tiff_file, output_dir):
    """
    Converts a TIFF file to XYZ tiles using gdal2tiles.py.

    Parameters:
    tiff_file (str): The path to the input TIFF file.
    output_dir (str): The directory where the tiles will be saved.

    Returns:
    None
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Use subprocess to call gdal2tiles
    try:
        # Run gdal2tiles command
        subprocess.check_call(['gdal2tiles.py', tiff_file, output_dir])
        print(f"Tiles have been generated and saved to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error during gdal2tiles conversion: {e}")
    except FileNotFoundError as e:
        print(f"gdal2tiles.py not found. Ensure that GDAL is installed: {e}")

# Example usage
tiff_file = "your_file.tif"  # Path to your TIFF file
output_dir = "output_tiles"  # Path where the tiles will be saved
convert_tiff_to_tiles(tiff_file, output_dir)
