import numpy as np
import os
from astropy.wcs import WCS
from astropy.io import fits
from scipy.ndimage import label


def save_candidate_coordinates(mask, header, output_path="results/candidates.txt"):
    """
    Receives a binary mask and the FITS header; saves a single point RA/Dec per group of connected pixels.

    :param mask: boolean matrix (True = candidate)
    :param header: header FITS of the image
    :param output_path: entry file
    """
    # Tagging the connected regions
    labeled_mask, num_features = label(mask)
    print(f"[INFO] Number of detected groups: {num_features}")

    # WCS for converting coordinates
    wcs = WCS(header)
    ras, decs = [], []

    for i in range(1, num_features + 1):
        yx = np.argwhere(labeled_mask == i)
        y_mean, x_mean = np.mean(yx, axis=0)  # center mass
        ra, dec = wcs.all_pix2world([[x_mean, y_mean]], 0)[0]
        ras.append(ra)
        decs.append(dec)

    # In the file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write("RA(deg),Dec(deg)\n")
        for ra, dec in zip(ras, decs):
            f.write(f"{ra:.6f},{dec:.6f}\n")

    print(f"[INFO] Candidates' coordinates (1 per group) saved in {output_path}")
