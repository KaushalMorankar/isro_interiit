import os
import shutil

# Define the source directory containing subfolders with FITS files
source_directory = "/home/inter-iit/isrointeriit/2024/05_filtered"

# Define the destination folder where all FITS files should be merged
destination_directory = "/home/inter-iit/isrointeriit/2024/05_allfitsfiltered"

# Create the destination directory if it doesn't exist
os.makedirs(destination_directory, exist_ok=True)

# Walk through the source directory
for root, dirs, files in os.walk(source_directory):
    for file in files:
        if file.endswith(".fits"):  # Check if the file is a FITS file
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_directory, file)
            
            # If a file with the same name already exists in the destination folder, append a number to the file name
            counter = 1
            while os.path.exists(destination_path):
                name, ext = os.path.splitext(file)
                destination_path = os.path.join(destination_directory, f"{name}_{counter}{ext}")
                counter += 1
            
            # Move the FITS file to the destination directory
            shutil.move(source_path, destination_path)

print(f"All FITS files have been moved to {destination_directory}")

