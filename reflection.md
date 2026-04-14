# Reflection — Music Recommender Simulation

## Profiles Tested

Four user profiles were run through the recommender:

1. **High-Energy Pop Fan** — genre: pop, mood: happy, energy: 0.88
2. **Chill Lofi Listener** — genre: lofi, mood: chill, energy: 0.38, likes acoustic
3. **Deep Intense Rock Head** — genre: rock, mood: intense, energy: 0.92
4. **Edge Case — Jazz but Intense** — genre: jazz, mood: intense, energy: 0.75, likes acoustic

---

## What Changed Between Profiles

**High-Energy Pop Fan** — The top result was "Sunrise City" with a score of 3.94,
which made sense: it matched on genre (pop), mood (happy), and had an energy
closeness of 0.94. "Gym Hero" came in at #2 with only 2.95 — a full point lower —
because it missed on mood (its mood is "intense", not "happy"). That one mismatch
dropped it significantly, showing how much the mood weight matters.

**Chill Lofi Listener** — This was the most striking result. "Library Rain" and
"Midnight Coding" scored 4.47 and 4.46 respectively — just 0.01 apart. Both are
lofi, both chill, both acoustic. The only thing that separated them was that
Library Rain's energy (0.35) was marginally closer to the target (0.38) than
Midnight Coding's (0.42). The acoustic bonus (+0.5) applied to both equally.
Without the acoustic bonus, their order would depend entirely on that tiny energy
difference — which feels almost random on such a small catalog.

"Focus Flow" landed at #3 with 3.48 even though its mood is "focused", not "chill".
It missed the mood bonus but still ranked above other songs purely because of the
lofi genre match and acoustic bonus. That felt slightly off — a "focused" lofi song
is not the same vibe as a "chill" one.

**Deep Intense Rock Head** — The clearest result of all. "Storm Runner" scored 3.99
with a near-perfect energy closeness of 0.99 (song energy: 0.91, target: 0.92).
It matched genre and mood too. The #2 result, "Gym Hero" (1.99), had no genre match
at all — it just shared the "intense" mood and high energy. The gap between #1 and
#2 was 2.0 points, which is exactly the genre weight. Genre dominates.

**Edge Case — Jazz but Intense** — The most revealing result. No song in the catalog
is both jazz AND intense. "Coffee Shop Stories" won with a score of 3.12 — but it's
a relaxed jazz song with energy 0.37, far from the target of 0.75. Its energy
closeness was only 0.62, yet genre (+2.0) and the acoustic bonus (+0.5) were enough
to push it to #1. The #2 and #3 results ("Storm Runner" and "Gym Hero", both 1.8x)
matched on mood (intense) but not genre or acoustic preference. The system had no
way to say "nothing fits well here" — it just returned the least-bad options.

---

## Profile Comparisons

**High-Energy Pop vs Chill Lofi:** Zero overlap in the top 3. Scores were similar
in range (Pop: 3.94/2.95/1.88 vs Lofi: 4.47/4.46/3.48) but the songs were
completely different. The scoring formula cleanly separated these two taste profiles.

**High-Energy Pop vs Deep Intense Rock:** The top scores were similar (3.94 vs 3.99)
but the songs diverged entirely. "Storm Runner" ranked #1 for Rock and didn't appear
in Pop's top 3 at all. Genre was the deciding factor in both cases.

**Chill Lofi vs Jazz Edge Case:** Both profiles like acoustic sound. The Lofi profile
had multiple genre matches (3 lofi songs in the catalog), so scores stayed high
across the board. The Jazz profile had only one genre match, and even that song had
bad energy alignment. The difference in catalog coverage was directly visible in the
scores: Lofi's top result scored 4.47, Jazz's top result scored only 3.12.

---

## Experiment: Weight Shift

**Change made:** What would happen if energy closeness was worth twice as much
(×2.0 of the closeness value) and genre was worth less (+1.0 instead of +2.0)?

**Predicted outcome for Jazz/Intense edge case:**
Currently, "Coffee Shop Stories" wins mainly because of the genre bonus (+2.0)
despite its poor energy match (closeness: 0.62). If energy weight doubled and
genre dropped to +1.0, the math would shift:

- Coffee Shop Stories: genre(1.0) + acoustic(0.5) + energy(0.62×2) = 2.74
- Night Drive Loop (synthwave, energy 0.75): no genre, no mood, but energy closeness
  = 1.0 - |0.75 - 0.75| = 1.0 → score would be 1.0×2 = 2.0
- Storm Runner: mood(1.0) + energy(0.84×2) = 2.68

Coffee Shop Stories would still edge ahead, but Storm Runner would be much closer.
The synthwave track (Night Drive Loop) — which actually matches the user's energy
target perfectly — would jump up the rankings. That feels more honest for a user
who said they want high-energy music.

**For High-Energy Pop Fan:** Barely any change. Sunrise City has both a genre match
AND the closest energy. Whether energy is weighted ×1.0 or ×2.0, it still wins.
When multiple signals align, reweighting individual signals doesn't move the winner.

**Conclusion:** Weights matter most at the edges — for users who don't have full
matches in the catalog. For users whose preferences are well-represented, the
recommender is robust to weight changes. For underserved users (like Jazz/Intense),
the weight choices can change the result meaningfully.

---

## Bias and Filter Bubble

**Filter bubble:** Every run with the same profile returns the exact same results.
There is no randomness, no "freshness" signal, no diversity mechanism. In a real app,
a user who listens to the same 3 songs every day would eventually stop discovering
anything new.

**Catalog representation bias:** Genres like country, classical, hip-hop, and R&B
don't exist in this dataset. A user who prefers those genres will never see a genre
match, so their maximum possible score is ≈1.9 (just mood + energy). They are
permanently disadvantaged compared to a pop fan who can score up to 4.5. This isn't
a bug in the formula — it's a bias baked into the data.

**Asymmetric bonuses:** The acoustic bonus (+0.5) rewards users who like acoustic
music but there's no equivalent bonus for users who prefer electronic or synthesized
sounds. Two users who are equally specific about sound texture get different amounts
of scoring power.

**Mood incompleteness:** The catalog only has 6 moods. If a user's preferred mood
isn't represented (e.g. "melancholic", "romantic", "aggressive"), the 1.0 mood
bonus is simply unavailable to them, even if songs in that spirit exist in the
catalog under a different label.

---

## What I Learned

The biggest takeaway is how visible the formula's choices become once you actually
run it. I knew genre was worth 2 points and mood was worth 1, but I didn't fully
expect how dramatically that plays out: the 2.0-point gap between "Storm Runner" (#1,
3.99) and "Gym Hero" (#2, 1.99) for the Rock profile is *exactly* the genre weight.
The formula's structure is readable directly in the output.

The Jazz/Intense edge case was the most educational. The system confidently returned
"Coffee Shop Stories" at rank #1 with a score of 3.12 — but that song is the
opposite of what a jazz-loving, intense-mood, high-energy user wants. A real user
would be frustrated. The model doesn't know it failed; it just found the highest
number. That gap between "highest score" and "right answer" is something to keep in
mind when thinking about any AI system — the metric can look fine while the
experience is wrong.
