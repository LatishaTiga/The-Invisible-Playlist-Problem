import os
import time
import yt_dlp
import librosa
import numpy as np
import pandas as pd
from difflib import SequenceMatcher
from tqdm import tqdm

tqdm.pandas()

# -----------------------
# CONFIG
# -----------------------
AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

BATCH_SIZE = 100          # safe on YouTube
SLEEP_BETWEEN = 2         # seconds
MIN_DURATION = 60
MAX_DURATION = 600

# -----------------------
# yt-dlp options
# -----------------------
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": f"{AUDIO_DIR}/%(id)s.%(ext)s",
    "quiet": True,
    "noplaylist": True,
    "sleep_interval": 2,
    "max_sleep_interval": 5,
    "retries": 3,
    "fragment_retries": 3,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "wav",
    }],
}

# -----------------------
# Helpers
# -----------------------
downloaded_ids = set()

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def build_query(row):
    return f"{row['artist_name']} - {row['track_name']} official audio"

def select_best_entry(entries, artist, track, min_score=0.5):
    scored = []
    for e in entries:
        title = e.get("title", "")
        score = (
            0.6 * similarity(title, track)
            + 0.4 * similarity(title, artist)
        )
        scored.append((score, e))

    scored.sort(reverse=True, key=lambda x: x[0])
    if scored and scored[0][0] >= min_score:
        return scored[0][1]
    return None

def download_audio(query, artist, track):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                f"ytsearch2:{query}",
                download=False
            )

            entries = result.get("entries", [])
            if not entries:
                return None

            entry = select_best_entry(entries, artist, track)
            if entry is None:
                return None

            audio_path = os.path.join(AUDIO_DIR, f"{entry['id']}.wav")

            # Skip download if already processed
            if entry["id"] in downloaded_ids and os.path.exists(audio_path):
                return audio_path

            ydl.download([entry["webpage_url"]])
            downloaded_ids.add(entry["id"])

            return audio_path

    except Exception:
        return None


def validate_audio(path):
    try:
        y, sr = librosa.load(path, sr=None, mono=True)
        duration = librosa.get_duration(y=y, sr=sr)
        rms = np.mean(librosa.feature.rms(y=y))

        return (
            MIN_DURATION <= duration <= MAX_DURATION
            and rms > 0.001
        )
    except Exception:
        return False

def extract_features(path):
    try:
        y, sr = librosa.load(path, sr=22050, mono=True)

        feats = {
            "tempo": float(librosa.beat.tempo(y=y, sr=sr)[0]),
            "rms_mean": float(np.mean(librosa.feature.rms(y=y))),
            "spectral_centroid_mean": float(
                np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            ),
            "zcr_mean": float(
                np.mean(librosa.feature.zero_crossing_rate(y))
            ),
        }

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=5)
        for i in range(5):
            feats[f"mfcc_{i+1}_mean"] = float(np.mean(mfcc[i]))

        return feats
    except Exception:
        return None

# -----------------------
# MAIN
# -----------------------
def process_batch(tracks, start):
    batch = tracks.iloc[start:start + BATCH_SIZE].copy()

    audio_paths = []
    features = []

    for _, row in tqdm(batch.iterrows(), total=len(batch)):
        query = build_query(row)
        path = download_audio(query, row["artist_name"], row["track_name"])
        time.sleep(SLEEP_BETWEEN)

        if path and validate_audio(path):
            audio_paths.append(path)
            features.append(extract_features(path))
        else:
            audio_paths.append(None)
            features.append(None)

    batch["audio_path"] = audio_paths
    batch["features"] = features

    out = batch.dropna(subset=["features"])
    out = pd.concat(
        [out.drop(columns=["features"]), out["features"].apply(pd.Series)],
        axis=1
    )

    out.to_csv(f"results_batch_{start}.csv", index=False)
    print(f"Saved batch starting at row {start}")

# -----------------------
# ENTRY POINT
# -----------------------
if __name__ == "__main__":
    tracks = pd.read_csv("filtered_df.csv")

    for start in range(0, len(tracks), BATCH_SIZE):
        process_batch(tracks, start)

    # -----------------------
    # FINAL MERGE (✅ correct place)
    # -----------------------
    import glob

    batch_files = sorted(glob.glob("results_batch_*.csv"))

    if not batch_files:
        raise RuntimeError("No batch files found — nothing to merge")

    final_df = pd.concat(
        (pd.read_csv(f) for f in batch_files),
        ignore_index=True
    )

    final_df.to_csv("audio_features_filtered_tracks.csv", index=False)
    print("Merged results saved to audio_features_filtered_tracks.csv")
