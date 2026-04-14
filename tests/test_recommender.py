from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


from src.recommender import score_song

def test_score_song_genre_and_mood_match():
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    song = {
        "id": 1, "title": "Sunrise City", "artist": "Neon Echo",
        "genre": "pop", "mood": "happy", "energy": 0.82,
        "tempo_bpm": 118.0, "valence": 0.84, "danceability": 0.79, "acousticness": 0.18,
    }
    score, reasons = score_song(user_prefs, song)
    # genre (+2.0) + mood (+1.0) + energy closeness (1 - |0.8 - 0.82| = 0.98)
    assert score >= 3.9
    assert any("genre" in r.lower() for r in reasons)
    assert any("mood" in r.lower() for r in reasons)
    assert any("energy" in r.lower() for r in reasons)


def test_score_song_no_match():
    user_prefs = {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False}
    song = {
        "id": 2, "title": "Midnight Coding", "artist": "LoRoom",
        "genre": "lofi", "mood": "chill", "energy": 0.42,
        "tempo_bpm": 78.0, "valence": 0.56, "danceability": 0.62, "acousticness": 0.71,
    }
    score, reasons = score_song(user_prefs, song)
    # no genre/mood match; energy closeness = 1 - |0.9 - 0.42| = 0.52
    assert score < 1.0
    assert isinstance(reasons, list)
