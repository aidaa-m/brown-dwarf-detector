from src.detector import detect_moving_objects  # or direct import if it is in the same file


def detect_on_multiple_images(paths):
    """
    Compares each pair of successive images from a list and applies the detection of the moving objects.

    :param paths: list of paths towards FITS files (minim 2)
    """
    if len(paths) < 2:
        print("[ERROR] At least two images needed for detection.")
        return

    for i in range(len(paths) - 1):
        path1 = paths[i]
        path2 = paths[i + 1]
        output_name = f"results/diff_pair_{i + 1}.png"

        print(f"[INFO] Compares the epoch  {i + 1} și {i + 2}: {path1} ↔ {path2}")
        detect_moving_objects(path1, path2, save_path=output_name)
