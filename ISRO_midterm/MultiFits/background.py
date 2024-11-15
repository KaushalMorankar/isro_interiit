import numpy as np
from astropy.io import fits
from tqdm import tqdm
import os

class io():
    def __init__(self, filename:str):
        self.name = filename
    
    def readFile(self):
        return fits.open(self.name)
    
    def getData(self):
        '''
        Returns:
            A 2-D Array containing channels and counts in a FITS file
        '''
        with self.readFile() as hdu:
            data = hdu[1].data
            channels = data['CHANNEL']
            counts = data['COUNTS']
            return np.column_stack((channels, counts)).astype(np.float64)
    
    def backgroundNoise(self):
        '''
        Returns: 
            True if the satellite is in the darkside of the moon
            otherwise False
        '''
        with self.readFile() as hdu:
            return hdu[1].header['SOLARANG']>90
        

def background_process(input_folder: str, output_folder: str, reverse:True):
    files = sorted(os.listdir(input_folder), reverse=reverse)  # Reverse order for background-first processing
    background = np.zeros((2048, 1))
    background_detection = False
    iters = 0
    folder_count = 0  # Folder counter for clusters of files sharing the same background

    for file in tqdm(files):
        path = os.path.join(input_folder, file)
        data = io(path)
        hdr = data.readFile()
        is_background = data.backgroundNoise()  # Detect if it's a background file
        
        if is_background:
            # Start or continue background accumulation
            if not background_detection:
                background_detection = True
                background = np.zeros((2048, 1))
                iters = 0  # Reset counter for a new background cluster
            
            # Accumulate background counts
            counts = data.getData()[:, 1].reshape((2048, 1))
            background += counts
            iters += 1
            
        else:
            # Process XRF data only if background was detected previously
            if background_detection and iters > 0:
                # Compute average background once the cluster ends
                background /= iters
                background_detection = False  # Reset background detection for next cluster
                folder_count += 1  # Update folder count for the next background cluster
            
            # Now process the XRF signal with computed background
            if iters==0:
                continue

            XRF_signal = data.getData()
            header = hdr[1].header
            
            # Prepare HDUs for output FITS file
            hdu1 = fits.ImageHDU(XRF_signal, name='XRFSignal')
            hdu2 = fits.ImageHDU(background, name='BackgroundNoise')
            hdul = fits.HDUList([fits.PrimaryHDU(header=header), hdu1, hdu2])
            folder_path = f"{output_folder}/{folder_count}"
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            # Save FITS file to the current background folder
            output_path = os.path.join(folder_path, f'filteredData_{file}')
            hdul.writeto(output_path, overwrite=True)
background_process('/home/inter-iit/isrointeriit/2024/05_data','/home/inter-iit/isrointeriit/2024/05_filtered',False)
