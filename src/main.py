"""
Command line runner for the Music Recommender Simulation.

Loads songs from data/songs.csv and runs the recommender for four
distinct user profiles to demonstrate how scoring changes by taste.
"""

from src.recommender import load_songs, recommend_songs


PROFILES = [
    {
        "name": "High-Energy Pop Fan",
        "prefs": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.88,
            "likes_acoustic": False,
        },
    },
    {
        "name": "Chill Lofi Listener",
        "prefs": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.38,
            "likes_acoustic": True,
        },
    },
    {
        "name": "Deep Intense Rock Head",
        "prefs": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "likes_acoustic": False,
        },
    },
    {
        "name": "Edge Case — Jazz but Intense",
        "prefs": {
            "genre": "jazz",
            "mood": "intense",
            "energy": 0.75,
            "likes_acoustic": True,
        },
    },
]


def print_recommendations(profile_name: str, recs: list) -> None:
    """Print a formatted block of recommendations for one user profile."""
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"  Profile: {profile_name}")
    print(separator)
    if not recs:
        print("  No recommendations found.")
        return
    for rank, (song, score, explanation) in enumerate(recs, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {explanation}")
    print()


def main() -> None:
    """Load songs and run recommendations for each user profile."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.\n")

    for profile in PROFILES:
        recs = recommend_songs(profile["prefs"], songs, k=3)
        print_recommendations(profile["name"], recs)


if __name__ == "__main__":
    main()
