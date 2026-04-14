# Music Recommender Simulation

## Project Summary

This project builds a small content-based music recommender in Python.
It loads a catalog of 10 songs, compares each song's attributes to a
user's taste profile, and ranks the songs by a weighted score. The
system also explains, in plain language, why each song was recommended.

---

## How Recommendation Systems Work

Real-world music apps like Spotify and Apple Music use two main approaches:

- **Content-based filtering** — recommends songs that are *similar* to
  what you already like, based on measurable features like genre, tempo,
  or energy. No data from other users is needed.

- **Collaborative filtering** — recommends songs that *other people with
  similar taste* enjoyed. It finds users who like the same things you do
  and suggests what they listened to next.

This project uses **content-based filtering** because we only have song
features and a single user profile — no listening history from multiple users.

---

## How This System Works

### Song features used

Each song in `data/songs.csv` has these columns:

| Feature | Type | Used for |
|---------|------|----------|
| `genre` | category | Exact match against user preference |
| `mood` | category | Exact match against user preference |
| `energy` | 0–1 float | Closeness to user's target energy |
| `acousticness` | 0–1 float | Bonus if user prefers acoustic sound |
| `tempo_bpm`, `valence`, `danceability` | numeric | Stored but not scored (future use) |

### User profile fields

```python
{
    "genre":          "pop",    # favorite genre string
    "mood":           "happy",  # preferred listening mood
    "energy":         0.85,     # target energy level (0–1)
    "likes_acoustic": False,    # True = boost acoustic songs
}
```

### Scoring algorithm

```
score = 0.0

if song.genre == user.genre:   score += 2.0   # strongest signal
if song.mood  == user.mood:    score += 1.0   # second signal
score += 1.0 - |user.energy - song.energy|    # closeness (0–1)
if user.likes_acoustic and song.acousticness > 0.6:
    score += 0.5                               # soft bonus

Maximum possible score: 4.5
```

Songs are ranked from highest to lowest score. The top `k` are returned
along with a plain-English explanation of which factors contributed.

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### Run the recommender

```bash
python -m src.main
```

### Run tests

```bash
pytest
```

---

## Experiments

### Weight shift: increased energy importance

In one experiment, the energy weight was doubled (multiplied by 2.0)
and the genre weight was halved (1.0). The recommender shifted toward
songs with the closest energy level regardless of genre. The Jazz/Intense
edge-case profile benefited most since it had no genre match anyway.
See `model_card.md` and `reflection.md` for full notes.

---

## Limitations and Risks

- Only 10 songs in the catalog — results are easy to exhaust.
- Genre is the dominant signal; genres not in the catalog (e.g., classical,
  country) will never win even if all other features match perfectly.
- The system has no memory — it treats every query independently.
- No collaborative signal: two users with identical preferences get
  identical recommendations forever (filter bubble).

---

## Screenshots

<!-- Insert terminal output screenshots here for the assignment submission -->

---

## Reflection

See [model_card.md](model_card.md) and [reflection.md](reflection.md)
for full analysis.

**Key learning:** Even a simple scoring rule creates meaningful
differences across user profiles. Changing one weight visibly reshapes
the ranked list, which shows just how much these design choices matter
in a real product.
