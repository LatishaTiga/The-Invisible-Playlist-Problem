# The-Invisible-Playlist-Problem
Exploratory analysis of the Spotify Million Playlist Dataset examining how playlist metadata, naming patterns, emotional signals, and audio features vary across popularity levels. Uses random and stratified downsampling and audio feature extraction from YouTube previews to compare playlist structure and track sequencing across popularity buckets.

# The Invisible Playlist Problem

This repository contains an exploratory data analysis of the Spotify Million Playlist Dataset (MPD), examining how playlist metadata, naming patterns, emotional signals, and audio features vary across playlist popularity levels.

The project combines large-scale metadata analysis with stratified downsampling and audio feature extraction from track previews to study how playlist structure and curation patterns change as playlists gain visibility.

---

## Project Structure
`The-Invisible-Playlist-Problem/
│
├── notebooks/
│ ├── 01_all_playlists_metadata.ipynb
│ ├── 02_downsampled_tracks.ipynb
│ ├── 03_stratified_playlists_vs_tracks.ipynb
│ └── 04_audio_feature_visualization.ipynb
│
├── src/
│ └── pipeline.py
│
├── data/
│ ├── processed/
│ │ ├── 1M_playlists_metadata.csv
│ │ ├── stratified_playlists.csv
│ │ └── stratified_tracks.csv
│ └── README.md
│
├── reports/
│ └── blog_post.pdf
│
├── assets/
│ └── figures/
│
├── .gitignore
└── README.md`

---

## Notebooks Overview

### 1. All Playlists Metadata (`01_all_playlists_metadata.ipynb`)

Analyzes metadata across all 1 million playlists, including:

- Playlist length distributions
- Naming patterns and keyword frequency
- Popularity bucket composition

---

### 2. Downsampled Tracks (`02_downsampled_tracks.ipynb`)

Uses random sampling to select ~1M tracks for scalable analysis.  
Documents the logic used to generate large intermediate datasets that are **not included** in the repository due to GitHub size limits.

---

### 3. Stratified Playlists vs Tracks (`03_stratified_playlists_vs_tracks.ipynb`)

Performs stratified downsampling of playlists based on popularity buckets:

- ~1,040 playlists
- ~68k associated tracks

Used to compare playlist structure and sequencing behavior across popularity levels.

---

### 4. Audio Feature Visualization (`04_audio_feature_visualization.ipynb`)

Extracts audio features from YouTube preview clips for a downsampled subset of playlists and visualizes:

- Tempo
- Energy
- Valence
- Acoustic patterns across playlist positions and popularity buckets

---

## Audio Feature Extraction Pipeline (`src/pipeline.py`)

Contains the pipeline used to:

- Search and retrieve YouTube previews for tracks
- Extract audio features from short audio segments
- Save processed feature outputs for downstream analysis

This pipeline is modular and can be reused independently of the notebooks.

---

## Data Availability

Due to GitHub file size limits, some large processed datasets are **not included** in this repository.

See `data/README.md` for details on:

- Which files are excluded
- Why they are excluded
- How to regenerate them using the provided notebooks

---

## How to Reproduce the Analysis

1. Download the Spotify Million Playlist Dataset:  
   [https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)

2. Run notebooks in order:

   - `01_all_playlists_metadata.ipynb`
   - `02_downsampled_tracks.ipynb`
   - `03_stratified_playlists_vs_tracks.ipynb`
   - `04_audio_feature_visualization.ipynb`

3. For audio analysis:

   - Configure required dependencies for `pipeline.py`
   - Run the audio extraction pipeline before executing the final notebook

---

## Dependencies

- Python 3.8+
- pandas
- numpy
- matplotlib / seaborn
- plotly
- librosa
- youtube-dl / yt-dlp

(*Exact versions documented within notebooks.*)

---

## References

- [Spotify Million Playlist Dataset](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)  
- [Spotify Audio Features Documentation](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)

---

## Notes

This repository is intended for research and analysis purposes.  
It does **not distribute copyrighted audio content**.
