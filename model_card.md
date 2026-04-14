# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0** — a rule-based, content-based music recommender.

---

## 2. Intended Use

This recommender is built for classroom exploration only. It is not
intended for real users or production deployment. Its purpose is to
demonstrate how recommendation systems turn data into ranked suggestions
and to practice identifying bias and limitations in AI systems.

It suggests up to 5 songs from a 10-song catalog based on a user's
genre preference, mood preference, energy target, and acoustic taste.

---

## 3. How the Model Works

The recommender compares each song in the catalog to the user's taste
profile using a point-based scoring system.

A song earns **2 points** if its genre matches the user's favorite genre,
**1 point** if its mood matches, and up to **1 point** based on how close
its energy level is to what the user wants (closer = more points). If the
user likes acoustic music and the song is mostly acoustic, it earns an
extra **0.5 points**.

Songs are then ranked from highest to lowest score. The top results are
returned together with a plain-English explanation of which factors
contributed to the score.

---

## 4. Data

- **Catalog size:** 10 songs
- **Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop
- **Moods represented:** happy, chill, intense, relaxed, moody, focused
- **Numeric features:** energy, tempo_bpm, valence, danceability, acousticness

The dataset was provided as part of the CodePath AI110 starter project.
No songs were added or removed. The catalog skews toward
electronic/modern genres and does not include classical, country,
hip-hop, or R&B — meaning users who prefer those genres will always
receive low-confidence recommendations.

---

## 5. Strengths

- Works well for users whose preferred genre and mood appear in the catalog.
- The energy closeness formula is fair — it rewards songs that are *close*
  to the user's target, not just songs with the highest or lowest energy.
- Every recommendation comes with a readable explanation.
- Simple scoring makes the model transparent and easy to debug.

---

## 6. Limitations and Bias

- **Genre dominance:** Genre is worth 2 points — more than any other
  factor. Users whose genre is absent from the catalog (e.g. classical)
  will receive recommendations based purely on mood and energy, which may
  feel wrong.
- **Filter bubble:** The system always returns the same songs for the
  same input. There is no diversity or serendipity mechanism.
- **Small catalog:** With only 10 songs, ties in score are common and the
  top-3 results exhaust most of the meaningful matches quickly.
- **Missing features:** Lyrics, language, tempo range preference, and
  artist familiarity are not considered.
- **Acoustic signal is weak:** The acousticness bonus (+0.5) is smaller
  than all other signals, so it rarely changes the ranking on its own.

---

## 7. Evaluation

Four user profiles were tested:

| Profile | Expected top result | Actual top result | Match? |
|---------|--------------------|--------------------|--------|
| High-Energy Pop | Sunrise City or Gym Hero | Sunrise City (score ≈ 3.94) | Yes |
| Chill Lofi | Library Rain or Midnight Coding | Library Rain (score ≈ 4.47) | Yes |
| Deep Intense Rock | Storm Runner | Storm Runner (score ≈ 3.99) | Yes |
| Jazz / Intense edge case | Low scores for all | Coffee Shop Stories (score ≈ 1.63) | Partial — genre matched but mood did not |

**Weight-shift experiment:** Energy weight was doubled (×2.0) and genre
weight was halved (×1.0). The Jazz/Intense profile changed significantly:
Coffee Shop Stories moved up because its energy (0.37) was penalized less
once genre mattered less. The High-Energy Pop profile barely changed
because Gym Hero already had both genre AND a close energy match.

---

## 8. Future Work

- Add diversity: avoid recommending two songs by the same artist in a
  single top-5 list.
- Expand the catalog to 50+ songs so edge-case profiles have more to work
  with.
- Add tempo preference to the user profile and include it as a small
  scoring signal.
- Support ranges (e.g. "energy between 0.6 and 0.8") instead of a single
  target.
- Experiment with collaborative filtering once multiple user profiles and
  their listening histories are available.

---

## 9. Personal Reflection

Building this recommender made it clear how much a single design choice —
like making genre worth 2 points instead of 1 — shapes everything the
model returns. The Jazz/Intense edge case was the most surprising result:
a jazz-loving user who wants intense music gets Coffee Shop Stories, which
is relaxed jazz, simply because nothing else in the catalog is closer. In
a real app, that would feel like a frustrating mismatch. It shows that a
model can be "correct by its own formula" while still being wrong for the
user — a reminder that metrics and human experience are not the same thing.
