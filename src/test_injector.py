from astropy.io import fits
import numpy as np
import os

def inject_artificial_object(input_path, output_path, brightness=50, position=(150, 150), size=5):
    """
    Creates a modified copy of a FITS image, with an artificial spot of light added.

    :param input_path: the way towards the original FITS image FITS
    :param output_path: where the artificial image will be saved
    :param brightness: the added intensity
    :param position: the central coordinates (y, x)
    :param size: the dimension of the artificial square (in pixels)
    """
    with fits.open(input_path) as hdu:
        img = hdu[0].data.copy()
        y, x = position
        half = size // 2

        # Adds an artificial shiny square
        img[y:y+half, x:x+half] += brightness

        # Saves the new image
        hdu[0].data = img
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        hdu.writeto(output_path, overwrite=True)

        print(f"[✅] The modified image saved in: {output_path}")
