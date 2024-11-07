from astropy.io import fits
import numpy as np
from scipy.optimize import minimize

def process_fits_file(file_path):
    # Load the FITS file
    with fits.open(file_path) as hdul:
        data = hdul[1].data
        channels = data[:, 0]
        counts = data[:, 1]
        data2 = hdul[2].data
        background_noise = data2[:, 0]

        # Subtract background noise from counts
        new_counts = counts - background_noise

        # Ensure no negative values after subtraction
        new_counts = np.maximum(new_counts, 0)

    # Calculate energy for each channel
    gain = 13.5  # eV/channel as given in the header
    energies = channels * gain

    # Define a dictionary of characteristic emission lines for elements of interest
    element_lines = {
        "Calcium": 7701.719,   # eV
        "Aluminium": 5139.708, # eV
        "Magnesium": 2543.688, # eV
        "Silicon": 3579.985    # eV
    }

    # Step 1: Find closest channel and calculate flux fractions
    flux_fractions = {}
    total_counts = 0

    # Calculate total counts and store counts for each element
    for element, line_energy in element_lines.items():
        closest_channel = (np.abs(energies - line_energy)).argmin()
        intensity = np.sum(new_counts[closest_channel - 5: closest_channel + 6])  # Sum over 10 channels around peak
        flux_fractions[element] = intensity
        total_counts += intensity

    # Normalize to get the flux fraction for each element
    for element in flux_fractions:
        flux_fractions[element] = flux_fractions[element] / total_counts

    # Convert flux_fractions dictionary to an array for easy comparison
    observed_flux_fraction = np.array(list(flux_fractions.values()))

    # Generate uncertainties using a relative threshold (or another method based on actual measurement uncertainties)
    uncertainties = np.sqrt(observed_flux_fraction * total_counts)

    # Step 2: Set up K_alpha and K_beta values for each element
    k_alpha = {'Ca': 3.691, 'Mg': 1.253, 'Al': 1.486, 'Si': 1.739}
    k_beta = {'Ca': 4.012, 'Mg': 1.302, 'Al': 1.557, 'Si': 1.835}

    # Objective function to minimize (chi-squared function)
    def objective_function(weights):
        predicted_flux_fraction = calculate_flux_fraction(weights)
        residuals = (observed_flux_fraction - predicted_flux_fraction) ** 2
        chi_squared = np.sum(residuals / (uncertainties**2))  # Normalized by uncertainties squared
        return chi_squared

    # Define abundance ranges for each element as bounds
    bound = [(1, 100), (1, 100), (1, 100), (1, 100)]  # Ranges for Ca, Mg, Al, Si

    # Calculate line flux for a given weight combination
    def calculate_line_flux(weights):
        ca_flux = weights[0] * (k_alpha['Ca'] + k_beta['Ca'])
        mg_flux = weights[1] * (k_alpha['Mg'] + k_beta['Mg'])
        al_flux = weights[2] * (k_alpha['Al'] + k_beta['Al'])
        si_flux = weights[3] * (k_alpha['Si'] + k_beta['Si'])
        return np.array([ca_flux, mg_flux, al_flux, si_flux])

    # Compute flux fraction for each element
    def calculate_flux_fraction(weights):
        flux = calculate_line_flux(weights)
        total_flux = np.sum(flux)
        return flux / total_flux

    # Initial guess for weights
    initial_guess = [25, 25, 25, 25]  # Example initial guess, evenly distributed

    # Use minimize to find the optimal weights
    result = minimize(objective_function, initial_guess, bounds=bound)

    # Check if optimization was successful
    if result.success:
        best_fit_weights = result.x
        best_fit_chi_squared = result.fun
        best_fit_flux_fraction = calculate_flux_fraction(best_fit_weights)
    else:
        raise ValueError("Optimization failed")

    # Return results
    return best_fit_weights, best_fit_chi_squared, best_fit_flux_fraction

# Example usage
file_path = r"C:\Users\omebh\OneDrive\Desktop\FilteredFits\filteredData_ch2_cla_l1_20200101T235955410_20200102T000003410.fits"
best_fit_weights, best_fit_chi_squared, best_fit_flux_fraction = process_fits_file(file_path)

# Print results
print("Ca Mg Al Si")
print("Best fit weights (wt%):", best_fit_weights)
print("Best fit chi-squared value:", best_fit_chi_squared)
print("Best fit flux fraction:", best_fit_flux_fraction)
