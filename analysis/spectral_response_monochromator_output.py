"""
Analyse the output files from `../calibration/spectral_response_monochromator.py`.
This plots all the intermediate spectra generated by that script.

Command line arguments:
    * `folder`: folder containing monochromator intemediaries
"""

import numpy as np
from sys import argv
from spectacle import io, spectral

# Get the data folder and minimum and maximum wavelengths from the command line
folder = io.path_from_input(argv)
root = io.find_root_folder(folder)

save_folder = root/"analysis/spectral_response/"

# Get the camera metadata
camera = io.load_metadata(root)
print("Loaded metadata")

# Load the wavelength data
wavelengths = np.load(folder/"monochromator_wavelengths.npy")

# Load and plot the raw response curves
raw_mean = np.load(folder/"monochromator_raw_means.npy")
raw_stds = np.load(folder/"monochromator_raw_stds.npy")

spectral.plot_monochromator_curves(wavelengths, raw_mean, raw_stds, title=f"{camera.device.name}: Raw spectral curves", saveto=save_folder/"monochromator_raw_spectra.pdf")
print("Saved raw spectrum plot")

# Load and plot the calibrated response curves
calibrated_mean = np.load(folder/"monochromator_calibrated_means.npy")
calibrated_stds = np.load(folder/"monochromator_calibrated_stds.npy")

spectral.plot_monochromator_curves(wavelengths, calibrated_mean, calibrated_stds, title=f"{camera.device.name}: Calibrated spectral curves", saveto=save_folder/"monochromator_calibrated_spectra.pdf")
print("Saved calibrated spectrum plot")

# Load and plot the normalised response curves
normalised_mean = np.load(folder/"monochromator_normalised_means.npy")
normalised_stds = np.load(folder/"monochromator_normalised_stds.npy")

spectral.plot_monochromator_curves(wavelengths, normalised_mean, normalised_stds, title=f"{camera.device.name}: Normalised spectral curves", saveto=save_folder/"monochromator_normalised_spectra.pdf")
print("Saved normalised spectrum plot")

# Load and plot the final resulting spectral response curves
final_curves = np.load(folder/"monochromator_curve.npy")
# Arrays in [] so they can be looped over (a bit of a hacky solution)
final_mean = [final_curves[1:5].T]
final_stds = [final_curves[5:].T]

spectral.plot_monochromator_curves(wavelengths, final_mean, final_stds, title=f"{camera.device.name}: Combined spectral curves", unit="normalised", saveto=save_folder/"monochromator_final_spectrum.pdf")
print("Saved final spectrum plot")
