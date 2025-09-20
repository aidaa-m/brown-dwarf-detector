import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
matplotlib.use('TkAgg')


def display_fits_auto_contrast(filepath, show_histogram=False):
    """
    Displays the FITS image with auto contrast (percentile 1% - 99%)

    :param filepath: the way towards the FITS file
    :param show_histogram: if True, displays the histogram of the pixels
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] The file {filepath} does not exist.")
        return

    try:
        with fits.open(filepath) as hdul:
            data = hdul[0].data

        # eliminates NaN or inf for contrast calculations
        valid_data = data[np.isfinite(data)]
        vmin = np.percentile(valid_data, 1)
        vmax = np.percentile(valid_data, 99)

        print(f"[INFO] Auto contrast: vmin={vmin:.2f}, vmax={vmax:.2f}")
        print(f"[INFO] The dimension of the image: {data.shape}")

        plt.figure(figsize=(6, 6))
        plt.imshow(data, cmap='gray', origin='lower', vmin=vmin, vmax=vmax)
        plt.colorbar(label="Intensity")
        plt.title(f" FITS image (Auto Contrast): {os.path.basename(filepath)}")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[ERROR] Display failed: {e}")

    if show_histogram:
        plt.figure(figsize=(6, 4))
        plt.hist(valid_data, bins=500, range=(vmin, vmax * 2), color='gray')
        plt.title("histogram of pixel values (auto contrast)")
        plt.xlabel("Intensity")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
