# Reflection — Music Recommender Simulation

## Profiles Tested

Four user profiles were run through the recommender:

1. **High-Energy Pop Fan** — genre: pop, mood: happy, energy: 0.88
2. **Chill Lofi Listener** — genre: lofi, mood: chill, energy: 0.38, likes acoustic
3. **Deep Intense Rock Head** — genre: rock, mood: intense, energy: 0.92
4. **Edge Case — Jazz but Intense** — genre: jazz, mood: intense, energy: 0.75, likes acoustic

---

## What Changed Between Profiles

The High-Energy Pop and Deep Rock profiles returned results that felt
intuitive almost immediately. Both profiles have genres and moods that
appear in the catalog, so the top results were clear winners.

The Chill Lofi profile was interesting because the acousticness bonus
(+0.5) visibly pushed "Library Rain" above "Midnight Coding" — two
otherwise very similar lofi songs. Without that bonus, the order would
have been reversed.

The Jazz/Intense profile was the most surprising. No song in the catalog
has genre=jazz AND mood=intense. The top result was "Coffee Shop Stories",
which matched genre (jazz) but not mood (relaxed vs intense). The system
gave it a partial score and it still won, which shows a real limitation:
the model cannot express "nothing is a good fit here."

---

## Profile Comparisons

**High-Energy Pop vs Chill Lofi:** These two profiles returned completely
different songs with no overlap in the top 3. The scoring formula
effectively separates high-energy pop songs from low-energy lofi ones.

**High-Energy Pop vs Deep Intense Rock:** Surprising amount of overlap in
the score range (≈3.9–4.0), but the songs themselves were different —
genre was the decisive factor. "Storm Runner" ranked #1 for Rock but near
the bottom for Pop.

**Chill Lofi vs Jazz Edge Case:** Both profiles like acoustic sound, but
their genre preferences differ. The Chill Lofi profile scored its
catalog songs 0.3–0.5 higher on average because lofi has multiple
matching songs. The Jazz profile only had one genre match, making
everything else fall back on mood+energy closeness.

---

## Experiment: Weight Shift

**Change made:** Doubled the energy similarity contribution (multiplied
the energy closeness result by 2.0 instead of 1.0) and halved the genre
weight (from +2.0 to +1.0).

**What changed:** The Jazz/Intense edge case showed the biggest shift.
Coffee Shop Stories dropped slightly and "Night Drive Loop" (synthwave,
energy 0.75) moved up because its energy was closest to the user's
target of 0.75. This felt more reasonable — the user wanted moderate-high
energy, and the synthwave track delivered that even though the genre was
wrong.

For the High-Energy Pop profile, the results barely changed. "Sunrise City"
still scored highest because it had both the genre match AND the closest
energy. This confirms that when multiple signals align, changing one
weight has little effect on the winner.

**Conclusion:** Energy weight matters most for edge-case users who have
no catalog matches for their genre. For "mainstream" profiles with full
matches, genre weight is the dominant driver regardless.

---

## Bias and Filter Bubble

This system has a clear filter bubble problem. If a user always enters
the same preferences, they will receive the same recommendations every
single time. Real apps break this with randomness, freshness signals, or
diversity constraints.

The system also has genre bias: if a genre is missing from the catalog,
those users are permanently disadvantaged. A user who loves country music
will never see a score above ≈1.9 (just mood + energy) no matter what.
That is a form of representation bias built directly into the data.

Finally, the acoustic bonus only helps users who set `likes_acoustic:
True`. Users who prefer electronic sounds get no equivalent bonus — an
asymmetry that could feel unfair.

---

## What I Learned

The most important insight is that recommendation systems do not discover
truth — they execute a formula. Every weight, every feature we chose to
include, and every feature we left out is a design decision that shapes
who benefits and who does not. Real systems like Spotify or YouTube make
thousands of these decisions, and each one can quietly favor one group of
users over another. Building even a toy recommender makes this concrete
and impossible to ignore.
