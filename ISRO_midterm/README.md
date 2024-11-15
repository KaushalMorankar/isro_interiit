# README: Processing FITS Files for Elemental Analysis

## Overview

This guide explains how to process a folder containing numerous FITS files downloaded from a source, perform background removal, and analyze the data to extract elemental abundances and intensities.

## Folder Structure
The folder structure is as follows:
- output.csv (csv containing all the months data)   
-   ├── MultiFits/   
      *  └── abundance_intensity.py/    
      *  └── allfitsinonefolder.py/     
      *  └── background.py/   
      *  └── rmf_updated_2.npy/      
      *  └── updated_arf_v1.arf/    
-   ├── SingleFits/    
      *  └── abundance_intensity.py/     
      *  └── background.py/
      *  └── rmf_updated_2.npy/      
      *  └── updated_arf_v1.arf/       
-   ├── Plotting/     
      *  └── map_intensity.py/     
      *  └── map_abundance.py/  
      *  └── MgSiHeatmap.py/  
      *  └── AlSiHeatmap.py/   
      *  └── lunar_map.tif (tif file for plotting) 

## Process the folder containing fits files.
- ## Folder Structure and Data Preparation

    When downloading a month's data, the structure typically contains nested folders for individual days. An example structure is:
    /cla/data/calibrated/2022/02/     
    ├── 01/   
    │   └── data_files/      
    ├── 02/    
    │   └── data_files/    
    └── 03/     
        └── data_files/ .....

    ### 1. Consolidating All FITS Files

    **Objective**: Collect all FITS files from nested subdirectories into a single folder.

    #### Steps:
    1. Open the `allfitsinonefolder.py` script.
    2. Set the `source_directory` variable to the path of the main folder (e.g., `/cla/data/calibrated/2022/02/`):
        ```python
        source_directory = "/path/to/your/folder/"
        ```
    3. Specify the `destination_directory` where the consolidated FITS files will be stored.
    4. Run the script to gather all FITS files into one folder.

    ### 2. Background Removal

    **Objective**: Process the consolidated FITS files to remove background noise and classify them based on background levels.

    #### Steps:
    1. Open the `background.py` script.
    2. Set the `source_directory` to the path of the folder containing the consolidated FITS files from Step 1.
    3. Specify the `destination_directory` where the processed FITS files will be saved.
    4. Run the script to perform background removal.
    5. The script will create subfolders in the destination directory, categorizing the FITS files based on their background levels.

    ### 3. Second Consolidation

    **Objective**: Collect all background-processed FITS files into a new consolidated directory.

    #### Steps:
    1. Run the `allfitsinonefolder.py` script again, but set `source_directory` to the path of the folder created in Step 2.
    2. Change the `destination_directory` to a new location for the second round of consolidation.
    3. Execute the script to gather all processed FITS files in one directory.

    ### 4. Analyzing Elemental Abundances and Intensities

    **Objective**: Extract elemental abundances and intensities from the processed FITS files and save the data to a CSV file.

    #### Steps:
    1. Open the `abundance_intensity.py` script.
    2. Provide the path to the folder containing the final set of processed FITS files.
    3. Set the path for the output CSV file to save the results.
    4. Run the script to generate a CSV file with the elemental analysis.

    ## Summary of Script Usage

    - **`allfitsinonefolder.py`**: Consolidates all FITS files from nested directories into one folder.
    - **`background.py`**: Removes background noise and categorizes FITS files.
    - **`abundance_intensity.py`**: Analyzes processed FITS files for elemental abundances and intensities, saving results to a CSV.

    ### Final Notes

    - Ensure that all paths are set correctly before running each script.
    - Verify that required dependencies (e.g., `astropy`) are installed in your Python environment.
    - Follow the step-by-step instructions for a smooth data processing workflow.


## Process a single fits file
- ### 1. Background Removal
    **Objective**: Process the FITS file to remove background noise 

    #### Steps:
    1. Open the `background.py` script.
    2. Set the path to the fits file.
    4. Run the script to perform background removal.
    5. The script will create a fits file separating the background noise.

    ### 2. Analysing Elemental Abundances and Intensities
    **Objective**: Extract elemental abundances and intensities from the processed FITS file and save the
    data to a CSV file.
    #### Steps:
    1. Open the `abundance_intensity.py` script.
    2. Provide the path of the processed fits file created in step
    3. Run the script to get the elemental analysis, Chi squared error and intensities of the elements.


## Plotting on a Lunar Map
- ### 1. Plotting Elemental Abundances and Intensities
    **Objective**: Plot elemental abundances and intensities from the processed FITS file.
    #### Steps:
    1. Run the script `map_abundance.py` to plot the elemental abundances on lunar map for the output stored in `output.csv`{created in the steps where the folder of fits files was used}

    2. Run the script `map_intensity.py` to plot the line intensities on lunar map for the output stored in `output.csv`{created in the steps where the folder of fits files was used}

    3. Run the script `MgSiHeatmap.py` to plot the line intensity ratio of Mg and Si on lunar map for the output stored in `output.csv`{created in the steps where the folder of fits files was used}

    4. Run the script `AlSiHeatmap.py` to plot the line intensity ratio of Al and Si on lunar map for the output stored in `output.csv`{created in the steps where the folder of fits files was used}

