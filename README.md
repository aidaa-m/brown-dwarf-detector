# Detection of Moving Objects with WISE/NEOWISE images

We present a complete pipeline for detecting moving astronomical objects in calibrated FITS images taken across multiple epochs. The system compares successive observations, filters significant pixel differences, converts regions of interest into WCS coordinates, and matches them across time to identify consistent motion. Applications include the detection of brown dwarfs, distant stellar objects, and solar system bodies with measurable proper motion.

**Keywords**: FITS, astronomical imaging, moving object detection, coordinate matching, multi-epoch analysis, WCS, RA/Dec

---

## Purpose of the project

- Identification of objects with high proper motion
- Comparison of images of the same sky region from different epochs
- Saving the coordinates (RA, Dec) of the detected candidates
- Automatic matching of positions between epochs
- Visualization of potential trajectories

---

## General Structure

1. `main.py` – punctul de intrare în proiect
  
2. `src/detector.py` – Image Differencing and Detection
  This module contains the core function detect_moving_objects, which:
  -loads two images and aligns the second to the first using reproject:
  -substracts global backgound offset by removing image medians;
  -computates the absolute pixel-wise difference and thresholds based on Nσ (adaptive)
  -applies morphological dilation and a size filter to retain valid candidates
  -outputs a binary mask of significant changes to retain valid candidates
  -outputs a binary mask of significant changes and saves RA/Dec coordinates via WCS
  
3. `src/save.py` – WCS Coordinate Conversion
 The function save_candidate_coordinates:
  - labels connected pixel regions in the binary mask;
  - computes centroids of these regions;
  - converts image-space coordinates to celestial (RA/Dec) via the FITS WCS header;
  - writes results to candidates_*.txt files for downstream analysis;
  
4. `src/visualize.py` – Trajectory Visualization
  This module displays:
  - source starting and ending positions from cross-epoch matches;
  - connecting lines indicating direction and approximate motion vectors;
  - overlays on grayscale FITS images with adaptive contrast scaling;
  
5. `src/multiple_images.py` - Batch Processing
  Given a list of images, this module:
  - applies the detection module on all consecutive image pairs;
  - saves PNG visualisations of detected differences for each pair;
  - automates candidate deneration across entire time series;
  
6. `src/analyze.py` – Multi-Epoch Motion Analysis
  This module performs cross-matching of coordinate files:
  - computes angular separations between spurces from two epochs
  - flags pairs within a user-defined threshold (default: 5 arcseconds)
  - gathers all valid matches and prepares for trajectory plotting or filtering
  
7. `src/test_injector.py`- Synthetic Source Injection
  For validation purpose, this module:
  - adds a synthetic bright patch to a FITS image at a defined location and brightness;
  - creates test cases to ensure the detection pipeline responds appropriately

8. `src/utils.py` - FITS Display Utility
  The display_fits_auto_contrast function:
  - loads and visualizes FITS data with percentile-based contrast scaling;
  - optionally shows histograms of pixel intensity distributions;
  
- `results/` – fișierele de output (.txt cu coordonate și imagini salvate)

---

## Input

- Two or more files `.fits` from the same celestial area, but from different epochs (e.g. different `scan_id`)
- band W2 (4.6μm), source NEOWISE-R

---

## Main steps

1. **Image alignment** using `reproject_interp` on common coordinates
2. **Median subtraction** to eliminate global offset
3. **Absolute difference computation** between images
4. **Noise filtering** using an adaptive threshold (e.g. `threshold = 3σ`)
5. **Labeling pixel groups** with significant differences
6. **Conversion to RA/Dec coordinates** using WCS
7. **Saving coordinates** into a .txt file `.txt` (e.g. `candidates_<frame>.txt`)
8. **Matching positions between epochs** using the function `match_candidates`
9. **Trajectory visualization** between epochs

---

## Example of result

```text
✦ Movements between epoca1.txt and epoca2.txt:
  (133.4360, -6.6533) → (133.4355, -6.6534) | Δ = 1.78"
  (133.2912, -6.6759) → (133.2910, -6.6767) | Δ = 3.05"






