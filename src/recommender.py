from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """OOP wrapper around the scoring logic; required by tests/test_recommender.py."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song_oop(self, user: "UserProfile", song: Song) -> Tuple[float, List[str]]:
        """Translate Song/UserProfile objects to dicts and delegate to score_song."""
        user_prefs = {
            "genre":          user.favorite_genre,
            "mood":           user.favorite_mood,
            "energy":         user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "id":           song.id,
            "title":        song.title,
            "artist":       song.artist,
            "genre":        song.genre,
            "mood":         song.mood,
            "energy":       song.energy,
            "tempo_bpm":    song.tempo_bpm,
            "valence":      song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        return score_song(user_prefs, song_dict)

    def recommend(self, user: "UserProfile", k: int = 5) -> List[Song]:
        """Return the top k songs sorted by descending score."""
        scored = [(song, self._score_song_oop(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: "UserProfile", song: Song) -> str:
        """Return a human-readable explanation of why this song was recommended."""
        _, reasons = self._score_song_oop(user, song)
        return " | ".join(reasons) if reasons else "No specific match found."

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; returns (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match: strongest signal
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append(f"Matches your favorite genre ({song['genre']})")

    # Mood match: second strongest
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append(f"Matches your preferred mood ({song['mood']})")

    # Energy closeness: songs near the target score highest
    target_energy = user_prefs.get("energy", 0.5)
    energy_closeness = 1.0 - abs(target_energy - song["energy"])
    score += energy_closeness
    reasons.append(f"Energy closeness score: {energy_closeness:.2f} (target {target_energy}, song {song['energy']})")

    # Acoustic bonus: optional soft signal
    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append(f"Has the acoustic sound you prefer (acousticness: {song['acousticness']:.2f})")

    return score, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"].strip().lower(),
                "mood":         row["mood"].strip().lower(),
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Score all songs, rank from highest to lowest, and return the top k results
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
