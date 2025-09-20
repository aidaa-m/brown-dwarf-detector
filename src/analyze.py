import os
import numpy as np

def get_candidate_files(folder="results/"):
    """  Returns the files type candidates_*.txt sorted chronologically"""
    files = [f for f in os.listdir(folder) if f.startswith("candidates_") and f.endswith(".txt")]
    return sorted(files)

def load_coordinates(filepath):
    """
    Uploads coordinates RA and Dec from a  file .txt
   Returns a list of tuples (RA, Dec)
    """
    coords = []
    with open(filepath, 'r') as f:
        next(f)  # skips the header "RA(deg),Dec(deg)" - as were saved in the files .txt
        for line in f:
            parts = line.strip().split(',') # le delimiteaza la ,
            if len(parts) == 2:
                ra, dec = map(float, parts)
                coords.append((ra, dec))
    return np.array(coords)  # converts to array numpy for efficiency


def angular_separation(ra1, dec1, ra2, dec2):
    """
    Calculates the angular separation between two points on the sphere, in arcsec.
    Can calculate between a coordinate and a list of coordinates.
    """
    ra1, dec1 = np.radians(ra1), np.radians(dec1)  # transforms to radians
    ra2, dec2 = np.radians(ra2), np.radians(dec2)

    delta_ra = ra2 - ra1
    delta_dec = dec2 - dec1

    #formulă de pe net
    # **2 raising to the second power
    a = np.sin(delta_dec / 2)**2 + np.cos(dec1) * np.cos(dec2) * np.sin(delta_ra / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return np.degrees(c) * 3600  # converts from radians to arcsec
# verifying the formulas

def match_candidates(file1, file2, max_sep_arcsec=5.0):
    """
    Compares the coordinates from the two files .txt
   Returns pairs (RA1, Dec1, RA2, Dec2, distance) for points that match
    5.0 arcsec is an acceptable threshold
    """
    coords1 = load_coordinates(file1)  # uploads RA/Dec from the first file
    coords2 = load_coordinates(file2)  # uploads RA/Dec from the second file

    matches = []
    for ra1, dec1 in coords1:
        # Calculates all distances between (ra1, dec1) and all points from coords2
        dists = angular_separation(ra1, dec1, coords2[:, 0], coords2[:, 1])
        min_idx = np.argmin(dists)  # the index of the closest source
        if dists[min_idx] <= max_sep_arcsec:  # if it is sufficiently close
            ra2, dec2 = coords2[min_idx]
            matches.append((ra1, dec1, ra2, dec2, dists[min_idx]))  # adds to the list

    return matches

def analyze_motion_across_epocs(folder="results/", max_sep_arcsec=5.0):
    """
    Searches for objects that appear in more consecutive epochs and it correlates them.
    """
    files = get_candidate_files(folder)
    all_matches = []

    for i in range(len(files) - 1):
        f1 = os.path.join(folder, files[i])
        f2 = os.path.join(folder, files[i + 1])
        print(f"[INFO] Compares {files[i]}  ↔  {files[i + 1]}")
        matches = match_candidates(f1, f2, max_sep_arcsec=max_sep_arcsec)
        all_matches.append((files[i], files[i + 1], matches))

    return all_matches
