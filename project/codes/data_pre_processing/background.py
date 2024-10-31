import numpy as np
from numba import njit
from astropy.io import fits
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
                


def background_process(input_folder:str, output_folder:str):
    """
    Processes X-ray fluorescence (XRF) data files in the specified folder, calculates 
    background noise if detected, and saves the processed data as FITS files.

    Parameters:
    -----------
    input_folder : str
        Path to the folder containing the input data files
    output_folder : str
        Path to the folder where processed FITS files will be saved

    Workflow:
    ---------
    1. Reads files from `input_folder` in reverse order(To prioritize background data before processing XRF data).
    2. Checks each file for background noise. If background noise is detected:
       - Accumulates the counts to calculate an average background signal.
    3. For non-background files:
       - If background noise has been detected in previous files, it averages 
         the accumulated background.
       - Writes the XRF signal and background noise to a FITS file with the original header.
       - Saves the output FITS file in `output_folder` with a name format `filteredData_<filename>`.
    4. The saved FITS files are structured as follows:
        - Header of raw data in the header of Primary HDU
        - XRF_Signal contains channels and counts
        - background contains background noise calculated

    Returns:
    --------
    None
    """
    files = [file for file in os.listdir(input_folder)][::-1]

    background_detection = False
    background = np.zeros((2048, 1))
    iters = 0

    @njit
    def background_numba(counts, is_background, background_detection, background, iters):
        '''
        Accelerates mathematical operations using Numba for improved algorithm performance.

        Returns:
            signal_detection: True if XRF is being recorded with pre-calculated background noise data, otherwise False
            background: background noise data
            iters: tracks the frequency of background noise examined
            background_detection: True if background is being detected, otherwise False

        '''
        signal_detection = False
        if is_background:
                iters += 1
                if not background_detection:
                    background_detection = True
                    background = np.zeros((2048, 1))
                background += counts
            
        else:
            if background_detection:
                background_detection = False
                # Doesnt process the XRF data without getting background noise
                if iters == 0:
                    return signal_detection, background, iters, background_detection
                background /= iters
                iters = 0
                signal_detection = True
        
        return signal_detection, background, iters, background_detection
    
    for file in files:
        path = f"{input_folder}/{file}"
        data = io(path)
        hdr = data.readFile()
        signal = data.getData()[:, 1].reshape((2048, 1))
        is_background = data.backgroundNoise()

        signal_detection, background, iters, background_detection = background_numba(signal, is_background, background_detection, background, iters)
        
        if signal_detection:
            header = hdr[1].header
            # XRF_Signal contains both background noise and XRF data
            XRF_signal = data.getData()
            hdu1 = fits.ImageHDU(XRF_signal, name='XRFSignal')
            hdu2 = fits.ImageHDU(background, name='BackgroundNoise')

            hdul = fits.HDUList([fits.PrimaryHDU(header=header), hdu1, hdu2])
            output_path = f"{output_folder}/filteredData_{file}"
            hdul.writeto(output_path, overwrite=True)