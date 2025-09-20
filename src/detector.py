from src.save import save_candidate_coordinates as save_coord
from scipy.ndimage import binary_dilation, label
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from reproject import reproject_interp
from src.visualize import plot_trajectories

import os


def filter_mask(mask, min_size=2, max_size=100, border=5):
    """
    Eliminates groups that are too small (noise), too large (artifacts) or close to the borders.

    :param mask: initial binary mask
    :param min_size: the least accepted number of pixels
    :param max_size: the largest accepted number of pixels
    :param border: how many pixels from the border are excluded
    :return: filtered mask
    """
    labeled, num = label(mask) # tags each group of pixels with a number (1,2,3 etc. )
    output = np.zeros_like(mask, dtype=bool)
    h, w = mask.shape # height and width

    for i in range(1, num + 1):
        coords = np.argwhere(labeled == i) #choses only the ones tagged with i, and saves them in pairs (y,x)
        size = coords.shape[0]
        y_coords, x_coords = coords[:, 0], coords[:, 1] #takes each element from line 0 (the one with y), and then 1 (the one with x)

        # print(
        #    f"[DEBUG] Objects {i}: size={size}, x=({x_coords.min()},{x_coords.max()}), y=({y_coords.min()},{y_coords.max()})")

        if size < min_size or size > max_size:
            continue
        if (x_coords.min() < border or x_coords.max() > w - border or
                y_coords.min() < border or y_coords.max() > h - border):
            continue

        output[coords[:, 0], coords[:, 1]] = True

    return output


def detect_moving_objects(path1, path2, save_path="results/diff_detected.png", threshold_multiple=3):
    """
    Compares the two FITS images (aligned) and marks the zones with significant differences (possibly moving objects).

    :param path1: the first FITS image
    :param path2: the second FITS image
    :param threshold: the minimum difference between the pixels
    :param save_path: where the result is saved
    :param threshold_multiple: 3x ~ accuracy 99.3% good for the start, more to filter
                               5x ~ accuracy 99.999% detects objects very confidently
    """
    # Reads the images
    with fits.open(path1) as h1:
        img1 = h1[0].data.astype(np.float32)
        hdr1 = h1[0].header

    with fits.open(path2) as h2:
        img2 = h2[0].data.astype(np.float32)
        hdr2 = h2[0].header

    # Aligns img2 to the coordinate system of img1
    img2_aligned, _ = reproject_interp((img2, hdr2), hdr1)
    #


    # Normalizes (subtracts the median to eliminate the global offset)
    img1 -= np.nanmedian(img1)
    img2_aligned -= np.nanmedian(img2_aligned)

    valid = np.isfinite(img1) & np.isfinite(img2_aligned)

    # To verify the centering of the two images
    diff = img2_aligned - img1
    diff_valid = diff[valid]

    plt.figure(figsize=(8, 6))
    plt.hist(diff_valid.flatten(), bins=100, color='gray')
    plt.title(f"differentiated histogram  {path2} - {path1}")
    plt.xlabel("difference of intensity")
    plt.ylabel("pixels number")
    plt.grid(True)
    plt.show()

    print(f"[INFO] The average difference on valid pixels: {np.mean(diff_valid):.3f}")
    print(f"[INFO] The average difference of pixels < 0.5 ~ very good, without global offset")
    print(f"[INFO] standard deviation: {np.std(diff_valid):.3f}")

    ys, xs = np.where(valid)

    # the central common zone (bounding box)
    ymin, ymax = ys.min(), ys.max()
    xmin, xmax = xs.min(), xs.max()

    sigma = np.nanstd(img1)
    threshold = threshold_multiple * sigma
    print(f"[INFO] Prag adaptiv: threshold = {threshold:.2f} ({threshold_multiple}σ)")

    # Calculates the absolute difference
    diff = np.abs(img2_aligned - img1)

    # Creates a mask with significant differences
    mask = diff > threshold
    mask = binary_dilation(mask, iterations=1)

    filtered_mask = filter_mask(mask)

    # Saves with a unique name based on the compared images
    pair_name = os.path.splitext(os.path.basename(path1))[0] + "_vs_" + os.path.splitext(os.path.basename(path2))[0]
    coord_path = f"results/candidates_{pair_name}.txt"
    save_coord(filtered_mask, header=hdr1, output_path=coord_path)

    # Output
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(img2_aligned[ymin:ymax + 1, xmin:xmax + 1], cmap='gray', origin='lower', interpolation='none',
              vmin=np.percentile(img2_aligned[valid], 1),
              vmax=np.percentile(img2_aligned[valid], 99))

    ax.contourf(filtered_mask[ymin:ymax + 1, xmin:xmax + 1], levels=[0.5, 1], colors='red', alpha=0.6)

    ax.set_title("Moving objects (red zones = difference)")
    plt.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.show()
    print(f"[INFO] The result was saved in {save_path}")
