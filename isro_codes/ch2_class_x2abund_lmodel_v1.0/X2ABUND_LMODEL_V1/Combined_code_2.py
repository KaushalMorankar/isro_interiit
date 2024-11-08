import numpy as np
import xraylib
from astropy.io import fits
from common_modules import *
from get_xrf_lines_V1 import get_xrf_lines
from get_constants_xrf_new_V2 import get_constants_xrf
from xrf_comp_new_V2 import xrf_comp

# Define atomic numbers for elements of interest
atomic_numbers = [26, 22, 20, 14, 13, 12, 11, 8]  # Fe, Ti, Ca, Si, Al, Mg, Na, O (Example elements)



hdul = fits.open(r"C:\Users\omebh\OneDrive\Desktop\data_set_6.fits")

# Input Parameters
incident_angle = 113.147  # Solar angle between surface normal and sun vector (example from SOLARANG)
emission_angle = 5.1430132e-9  # Emission angle from EMISNANG
gain = 13.5  # eV/channel, given in the header

spectrum_data = hdul[1].data
channels = spectrum_data['CHANNEL']
counts = spectrum_data['COUNTS']

# Convert channels to energies using gain
energies = channels * gain

# Initialize the weights (assumed example values)
weights = [5, 1, 9, 21, 14, 5, 0.5, 45]  # Example weights in wt%

# Define emission lines using xraylib for primary and secondary
k_lines = np.array([xraylib.KL1_LINE, xraylib.KL2_LINE, xraylib.KL3_LINE, xraylib.KM1_LINE, xraylib.KM2_LINE, xraylib.KM3_LINE, xraylib.KM4_LINE, xraylib.KM5_LINE])
l1_lines = np.array([xraylib.L1L2_LINE, xraylib.L1L3_LINE, xraylib.L1M1_LINE, xraylib.L1M2_LINE, xraylib.L1M3_LINE, xraylib.L1M4_LINE, xraylib.L1M5_LINE, xraylib.L1N1_LINE])
l2_lines = np.array([xraylib.L2L3_LINE, xraylib.L2M1_LINE, xraylib.L2M2_LINE, xraylib.L2M3_LINE, xraylib.L2M4_LINE, xraylib.L2M5_LINE, xraylib.L2N1_LINE])
l3_lines = [xraylib.L3M1_LINE, xraylib.L3M2_LINE, xraylib.L3M3_LINE, xraylib.L3M4_LINE, xraylib.L3M5_LINE, xraylib.L3N1_LINE]

# Generate XRF lines
xrf_lines = get_xrf_lines(atomic_numbers, xraylib.K_SHELL, k_lines, xraylib.L1_SHELL, l1_lines, xraylib.L2_SHELL, l2_lines, xraylib.L3_SHELL, l3_lines)

# Generate constants for XRF
const_xrf = get_constants_xrf(energies, atomic_numbers, weights, xrf_lines)

# Calculate primary and secondary XRF intensities
xrf_struc = xrf_comp(energies, counts, incident_angle, emission_angle, atomic_numbers, weights, xrf_lines, const_xrf)

# Retrieve primary, secondary, and total XRF intensities
primary_xrf_intensity = xrf_struc.primary_xrf
secondary_xrf_intensity = xrf_struc.secondary_xrf
total_xrf_intensity = xrf_struc.total_xrf  # This is the sum of primary and secondary XRF intensities

# Display Results
print("Primary XRF Intensity:\n", primary_xrf_intensity)
print("Secondary XRF Intensity:\n", secondary_xrf_intensity)
print("Total XRF Intensity:\n", total_xrf_intensity)
