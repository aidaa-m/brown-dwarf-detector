# Detectare de Obiecte în Mișcare cu Imagini WISE/NEOWISE

Acest proiect permite **detectarea automată a obiectelor cerești în mișcare** (precum piticii bruni) folosind imagini FITS provenite de la satelitul **WISE / NEOWISE-R**, achiziționate în epoci diferite.

---

## Scopul proiectului

- Identificarea obiectelor cu mișcare proprie mare
- Compararea imaginii aceleiași zone din cer în epoci diferite
- Salvarea coordonatelor (RA, Dec) ale candidaților
- Corelarea automată a pozițiilor între epoci
- Vizualizarea traiectoriilor potențiale

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
  -labels connected pixel regions in the binary mask;
  -computes centroids of these regions;
  -converts image-space coordinates to celestial (RA/Dec) via the FITS WCS header;
  -writes results to candidates_*.txt files for downstream analysis;
  
4. `src/visualize.py` – Trajectory Visualization
  This module displays:
  -source starting and ending positions from cross-epoch matches;
  -connecting lines indicating direction and approximate motion vectors;
  -overlays on grayscale FITS images with adaptive contrast scaling;
  
5. `src/multiple_images.py` - Batch Processing
  Given a list of images, this module:
  -applies the detection module on all consecutive image pairs;
  -saves PNG visualisations of detected differences for each pair;
  -automates candidate deneration across entire time series;
  
6. `src/analyze.py` – Multi-Epoch Motion Analysis
  This module performs cross-matching of coordinate files:
  -computes angular separations between spurces from two epochs
  -flags pairs within a user-defined threshold (default: 5 arcseconds)
  -gathers all valid matches and prepares for trajectory plotting or filtering
  
7. `src/test_injector.py`- Synthetic Source Injection
  For validation purpose, this module:
  -adds a synthetic bright patch to a FITS image at a defined location and brightness;
  -creates test cases to ensure the detection pipeline responds appropriately

8. `src/utils.py` - FITS Display Utility
  The display_fits_auto_contrast function:
  -loads and visualizes FITS data with percentile-based contrast scaling;
  -optionally shows histograms of pixel intensity distributions;
  
- `results/` – fișierele de output (.txt cu coordonate și imagini salvate)

---

## Input

- Two or more files `.fits` from the same celestial area, but from different epochs (ex: different `scan_id`)
- band W2 (4.6μm), source NEOWISE-R

---

## Pașii principali

1. **Alinierea imaginilor** cu `reproject_interp` pe coordonate comune
2. **Scăderea medianei** pentru eliminarea offset-ului global
3. **Calculul diferenței absolute** între imagini
4. **Filtrarea zgomotului** prin prag adaptiv (ex: `threshold = 3σ`)
5. **Etichetarea grupurilor de pixeli** cu diferență semnificativă
6. **Conversia în coordonate RA/Dec** folosind WCS
7. **Salvarea coordonatelor** într-un fișier `.txt` (ex: `candidates_<frame>.txt`)
8. **Compararea pozițiilor între epoci** cu funcția `match_candidates`
9. **Vizualizarea traiectoriilor** între epoci

---

## Example of result

```text
✦ Movements between epoca1.txt and epoca2.txt:
  (133.4360, -6.6533) → (133.4355, -6.6534) | Δ = 1.78"
  (133.2912, -6.6759) → (133.2910, -6.6767) | Δ = 3.05"

