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

## Structura generală

- `main.py` – punctul de intrare în proiect
- `src/detector.py` – funcția principală de detecție a mișcării
- `src/save.py` – salvarea coordonatelor candidaților
- `src/visualize.py` – afișare grafică a traiectoriilor ? TODO
- `src/multiple_images.py` - permite lucrul cu mai multe fișiere
- `src/analyze.py` – compararea candidaților între epoci + corelarea pozițiilor pe 
                      baza mișcării ungiulare
- `results/` – fișierele de output (.txt cu coordonate și imagini salvate)

---

## Input

- Două sau mai multe fișiere `.fits` provenite din aceeași zonă cerească, dar din epoci diferite (ex: diferite `scan_id`)
- Banda W2 (4.6μm), sursa NEOWISE-R

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

## Exemplu de rezultat

```text
✦ Mișcări între epoca1.txt și epoca2.txt:
  (133.4360, -6.6533) → (133.4355, -6.6534) | Δ = 1.78"
  (133.2912, -6.6759) → (133.2910, -6.6767) | Δ = 3.05"
