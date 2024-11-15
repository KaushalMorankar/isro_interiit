#
#====================================================================================
#                   XRF Elemental Abundance (Weight %) Calculation
#
# This package calculates elemental weight percentages from X-ray fluorescence (XRF)
# data using spectral fitting, Gaussian peak identification, and model optimization.
# It fits Gaussian curves to observed XRF line intensities, calculates flux fractions,
# and minimizes chi-squared values to determine the optimal elemental abundances.
#
# Methods:
#    - Gaussian Peak Fitting: Fits Gaussian functions to each peak to estimate line 
#      intensities for elements of interest.
#    - Model Optimization: Uses chi-squared minimization to match observed fluxes with
#      theoretical predictions based on atomic parameters from xraylib.
#    - RMF/ARF Application: Adjusts for instrument response using Response Matrix (RMF) 
#      and Ancillary Response (ARF) data to improve accuracy.
#
# Dependencies:
#    - xraylib:  Atomic library for XRF (install via conda: `conda install xraylib`)
#    - numpy:    Numerical computing (`conda install numpy`)
#    - astropy:  FITS file handling (`conda install astropy`)
#    - scipy:    Optimization methods (`conda install scipy`)
#
#====================================================================================
#

import numpy as np
from scipy.optimize import minimize, curve_fit
from astropy.io import fits
import warnings
import xraylib
import csv

# Suppress warnings from curve_fit
warnings.simplefilter('ignore', np.RankWarning)

#------------------------------------Define a Gaussian function for peak fitting--------------------------------------------
def gaussian(x, a, b, sigma):
    """Define a Gaussian function."""
    return a * np.exp(-((x - b) ** 2) / (2 * sigma ** 2))

#----------------------------- Function to estimate sigma based on detector resolution--------------------------------------
def get_sigma(energy_eV):
    # Estimate sigma (in eV) based on detector resolution
    E_keV = energy_eV / 1000.0  # Convert energy to keV
    a = 20  # eV per keV
    b = 100   # Baseline resolution in eV
    fwhm_eV = a * E_keV + b  # FWHM in eV
    sigma_eV = fwhm_eV / 2.355
    return sigma_eV


#------------------------------ Function to fit a Gaussian in a specified energy window-------------------------------------
def fit_gaussian_in_window(energies, counts, line_energy):
    """Fit a Gaussian in a specified energy window based on ±3σ."""
    sigma_estimated = get_sigma(line_energy)  # Get sigma in eV for the line energy
    window_size = 3*sigma_estimated  # Use ±3σ for the window size

    # Define the energy window around the line energy
    window_mask = (energies >= line_energy - window_size) & (energies <= line_energy + window_size)
    energy_window = energies[window_mask]
    count_window = counts[window_mask]

    # Check if the window has enough data points
    if count_window.size < 5:
        # print(f"Insufficient data within the window for line energy {line_energy} eV")
        return 0, 1  # Return intensity=0 and uncertainty=1

    # Improved initial guesses
    amplitude_guess = np.max(count_window) - np.min(count_window)
    mean_guess = energy_window[np.argmax(count_window)]
    sigma_guess = sigma_estimated

    # Set bounds for the parameters to ensure physical meaningfulness
    amplitude_bound = (0, np.inf)
    mean_bound = (line_energy - window_size, line_energy + window_size)
    sigma_bound = (sigma_estimated * 0.5, sigma_estimated * 2)

    bounds = (amplitude_bound, mean_bound, sigma_bound)
    initial_guess = [amplitude_guess, mean_guess, sigma_guess]

    try:
        # Fit the Gaussian to the data in the window with bounds
        popt, pcov = curve_fit(
            gaussian,
            energy_window,
            count_window,
            p0=initial_guess,
            bounds=([b[0] for b in bounds], [b[1] for b in bounds])
        )
        amplitude = popt[0]
        amplitude_uncertainty = np.sqrt(np.diag(pcov))[0]  # Uncertainty in amplitude
        return amplitude, amplitude_uncertainty
    except (RuntimeError, ValueError):
        # print(f"Gaussian fit did not converge for line energy {line_energy} eV")
        # Alternative approach: fit using least squares minimization
        def residuals(params):
            a, b, sigma = params
            return count_window - gaussian(energy_window, a, b, sigma)

        # Use initial guesses and bounds
        result = minimize(
            lambda params: np.sum(residuals(params) ** 2),
            initial_guess,
            bounds=bounds,
            method='L-BFGS-B'
        )

        if result.success:
            a_opt, b_opt, sigma_opt = result.x
            # Estimate uncertainty as standard deviation of residuals
            residual_std = np.std(residuals(result.x))
            amplitude_uncertainty = residual_std / np.sqrt(len(count_window))
            return a_opt, amplitude_uncertainty
        else:
            print(f"Alternative fitting method failed for line energy {line_energy} eV")
            # As a last resort, estimate intensity from the area under the curve
            intensity = np.trapz(count_window, energy_window)
            uncertainty = np.sqrt(intensity) if intensity > 0 else 1
            return intensity, uncertainty
        



#------------------------ Main function to process the FITS file and perform abundance calculation-------------------------



def process_fits_file(file_path,rmf_file,u_arf_file):

    bkg = fits.open(file_path)[2].data.reshape((2048,))
    spectrum = fits.open(file_path)[1].data[:, 1]
    channels = fits.open(file_path)[1].data[:, 0]

    #Using ARF and RMF matrices to calibrate the data
    def RMF_ARF():
        rmfdata = np.load(rmf_file)
        modified_spectrum = np.matmul(rmfdata, spectrum)
        modified_bkg = np.matmul(rmfdata, bkg)
        arfData = np.load(u_arf_file)

        modified_spectrum = (modified_spectrum*arfData)
        modified_bkg = (modified_bkg*arfData)

        return modified_bkg[70:1100],modified_spectrum[70:1100]
    
    # Compressing from 2048 to 1024 channels by summing adjacent pairs
    modified_bkg,modified_spectrum = RMF_ARF()
    modified_bkg = modified_bkg.reshape(-1, 2).sum(axis=1)
    modified_spectrum = modified_spectrum.reshape(-1, 2).sum(axis=1)

    # Subtract background noise from counts
    net_counts = modified_spectrum - modified_bkg  # Ensure no negative values
    net_counts=np.maximum(net_counts,0)


    # Calculate energy for each channel
    gain = 13.5  # eV/channel as given in the header
    energies = channels * gain
    energies=energies[70:1100]
    energies = energies.reshape(-1, 2).mean(axis=1)
    # Define characteristic emission lines (in eV) for elements of interest
    elements = ["Ca", "Mg", "Al", "Si", "Fe"]
    atomic_numbers = [xraylib.SymbolToAtomicNumber(el) for el in elements]

    # Retrieve line energies
    element_lines = {}
    for el, Z in zip(elements, atomic_numbers):
        kalpha_energy = xraylib.LineEnergy(Z, xraylib.KA1_LINE) * 1000  # Convert from keV to eV
        if kalpha_energy == 0:
            kalpha_energy = xraylib.LineEnergy(Z, xraylib.KA_LINE) * 1000  # Fallback in case KA1_LINE is unavailable
        element_lines[el] = kalpha_energy
    # Relative intensities (weights) of K-alpha and K-beta lines
    # These values should be replaced with accurate data from a reliable source

    # Step 1: Fit Gaussians to each peak to extract intensities
    observed_intensities = []
    intensity_uncertainties = []
    # Set minimum detectable intensity based on instrument's sensitivity
      # Adjust based on instrument sensitivity

    for element, k_alpha_energy in element_lines.items():
        min_detectable_intensity = 3*get_sigma(k_alpha_energy)
        # Fit Gaussian to K-alpha line with a dynamic window size
        amplitude, amplitude_uncertainty = fit_gaussian_in_window(
            energies, net_counts, k_alpha_energy
        )
        
        # Ensure minimum detectable intensity for observed values
        if amplitude < min_detectable_intensity:
            amplitude = min_detectable_intensity
            amplitude_uncertainty = np.sqrt(min_detectable_intensity)
        
        # Append observed intensity and its uncertainty
        observed_intensities.append(amplitude)
        intensity_uncertainties.append(amplitude_uncertainty)

    # Convert lists to arrays for further processing
    observed_intensities = np.array(observed_intensities)
    intensity_uncertainties = np.array(intensity_uncertainties)


    # Normalize observed intensities to get flux fractions
    total_intensity = np.sum(observed_intensities)
    if total_intensity == 0:
        raise ValueError("Total observed intensity is zero. Check the input data.")

    observed_flux_fraction = observed_intensities / total_intensity

    # Handle zero or infinite uncertainties
    intensity_uncertainties = np.where(intensity_uncertainties == 0, 1, intensity_uncertainties)
    intensity_uncertainties = np.where(np.isinf(intensity_uncertainties), np.max(intensity_uncertainties[np.isfinite(intensity_uncertainties)]), intensity_uncertainties)

    #------------------- Define the theoretical model to calculate predicted flux fractions-------------------------------

    def calculate_flux_fraction(weights):
        predicted_intensities = []

        for idx, element in enumerate(elements):
            Z = atomic_numbers[idx]
            weight = weights[idx]

            # Get fluorescence yield, jump factor, and radiative rates from xraylib
            fy = xraylib.FluorYield(Z, xraylib.K_SHELL)
            jf = xraylib.JumpFactor(Z, xraylib.K_SHELL)

            k_edge_energy = xraylib.EdgeEnergy(Z, xraylib.K_SHELL)  # in keV

            rr_kalpha = xraylib.RadRate(Z, xraylib.KA_LINE)
            try:
                rr_kbeta = xraylib.RadRate(Z, xraylib.KB_LINE)
            except ValueError:
                rr_kbeta = 0.0  # Set K-beta rate to 0 if not available

           
            l_edge_energy = xraylib.EdgeEnergy(Z, xraylib.L1_SHELL) if hasattr(xraylib, 'L1_SHELL') else 0.0

            total_edge_energy = l_edge_energy + k_edge_energy
            Edge_energy = 1 / total_edge_energy if total_edge_energy > 0 else 1  # Higher for lighter elements

            rr_total = rr_kalpha + rr_kbeta

            #Just for safety never occurs
            if  rr_total ==0 or fy == 0 or jf == 0:
                print(1)
                fy = 1e-10
                jf = 1e-10
            
            # Calculate predicted intensity using physical parameters
            pred_intensity = weight * (1 - 1 / jf) * rr_total * fy * Edge_energy
            predicted_intensities.append(pred_intensity)

            
        
        predicted_intensities = np.array(predicted_intensities)
        

        # Normalize predicted intensities to ensure they sum to 1 (if desired)
        total_predicted_intensity = np.sum(predicted_intensities)
        if total_predicted_intensity > 0:
            predicted_flux_fraction = predicted_intensities / total_predicted_intensity
        else:
            predicted_flux_fraction = predicted_intensities  # Avoid division by zero in edge cases
        
        return predicted_flux_fraction


    # Objective function to minimize (chi-squared function)
    def objective_function(weights):
        predicted_flux_fraction = calculate_flux_fraction(weights)
        residuals = observed_flux_fraction - predicted_flux_fraction
        chi_squared = np.sum((residuals / (intensity_uncertainties / total_intensity)) ** 2)
        return chi_squared
    

    max_bound=40
    # Constraints and bounds
    bounds = [(0, max_bound)] * len(element_lines)  # Concentrations between 0% and 100%
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - max_bound}  # Sum of weights equals 100%

    # Initial guess for weights (even distribution)
    initial_guess =  [1,19,15,20,5] #[max_bound / len(element_lines)] * len(element_lines)

    # Perform optimization
    result = minimize(
        objective_function,
        initial_guess,
        bounds=bounds,
        constraints=constraints,
        method='SLSQP'  # Sequential Least Squares Programming
    )

    # Check if optimization was successful
    if result.success:
        best_fit_weights = result.x
        best_fit_chi_squared = result.fun
        best_fit_flux_fraction = calculate_flux_fraction(best_fit_weights)
    else:
        raise ValueError("Optimization failed: " + result.message)

    # Return results
    return best_fit_weights, best_fit_chi_squared, best_fit_flux_fraction, list(element_lines.keys())



#-----------------------------------------Main Code------------------------------------------------------------


file_path = r"C:\Users\omebh\OneDrive\Desktop\data_set_filtered_1.fits"
rmf_file = r"C:\Users\omebh\OneDrive\Desktop\rmf_updated_1.npy"  # Replace with your RMF file path
# arf_file = 'test/class_arf_v1.arf'
u_arf_file = r"C:\Users\omebh\OneDrive\Desktop\arf_update_1.npy"
best_fit_weights, best_fit_chi_squared, best_fit_flux_fraction, elements = process_fits_file(file_path,rmf_file,u_arf_file)

print("Elemental Abundances (wt%):")
for element, weight in zip(elements, best_fit_weights):
    print(f"{element}: {weight:.2f}%")
print(f"Best fit chi-squared value: {best_fit_chi_squared:.2f}")
print("Best fit flux fractions:")
for element, flux_frac in zip(elements, best_fit_flux_fraction):
    print(f"{element}: {flux_frac:.4f}")


#--------------------------------------------End------------------------------------------------------------------

