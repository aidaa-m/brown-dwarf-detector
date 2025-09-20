import warnings
from astropy.wcs import FITSFixedWarning
from src.multiple_images import detect_on_multiple_images
from src.analyze import analyze_motion_across_epocs

warnings.simplefilter('ignore', FITSFixedWarning)

from src.utils import display_fits_auto_contrast
from src.test_injector import inject_artificial_object

from src.detector import detect_moving_objects

file1 = "data/raw/81487a025-w2-int-1b.fits"
file2 = "data/raw/92517a025-w2-int-1b.fits"
file3 = "data/raw/04915r025-w2-int-1b.fits"

# The images have to be introduced in chronological order.
image_list = [
    file1,
    file2,
    file3
]

detect_on_multiple_images(image_list)
results = analyze_motion_across_epocs()
for file1, file2, pairs in results:
    print(f"\n✦ Shifts between {file1} and {file2}:")
    for ra1, dec1, ra2, dec2, sep in pairs:
        print(f"\"  ({ra1:.4f}, {dec1:.4f}) → ({ra2:.4f}, {dec2:.4f}) | Δ = {sep:.2f}\"")
print("Δ > 1-2 is a strong signal | Δ < 1 is a signal of uncertainty")

