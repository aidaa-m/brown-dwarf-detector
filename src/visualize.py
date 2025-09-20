import matplotlib.pyplot as plt
import numpy as np


def plot_trajectories(image, x_start, y_start, x_end, y_end, title="Traiectorii detectate"):
    """
    Displays an image with the trajectories from the starting to the ending points.

    :param image: the initial image (array 2D)
    :param x_start: the list of X starting coordinates
    :param y_start: the list of Y starting coordinates
    :param x_end: the list of X finishing coordinates
    :param y_end: the list of Y finishing coordinates
    :param title: the title of the chart
    """
    fig, ax = plt.subplots(figsize=(7, 7))
    valid = np.isfinite(image)
    vmin, vmax = np.percentile(image[valid], [1, 99])
    ax.imshow(image, cmap='gray', origin='lower', vmin=vmin, vmax=vmax)

    # marking the starting points
    ax.scatter(x_start, y_start, s=40, edgecolors='red', facecolors='none', linewidths=1.5, label="Start")

    # drawing lines and starting points
    for x1, y1, x2, y2 in zip(x_start, y_start, x_end, y_end):
        ax.plot([x1, x2], [y1, y2], color='red', linewidth=1)
        ax.scatter([x2], [y2], s=30, color='yellow', marker='x')

    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.show()
