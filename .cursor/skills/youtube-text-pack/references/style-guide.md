# Style guide (3–5 min discovery video)

## References (pace, not plagiarism)

- **Fireship** — dense beats, on-screen keywords, no fluff
- **3Blue1Brown** — one clear mental model with visual metaphors
- **Two Minute Papers** — curious hook → insight → what it enables next

## Narrative arc

1. Hook (10–15 s) — concrete curiosity gap
2. Problem — why the default choice fails in the lab
3. Mental model — 1 diagram the viewer can redraw
4. Hands-on proof sketch — protocol + the numbers from the chapter
5. Failure modes / decision table — when *not* to do X
6. CTA — site (full tutorial) → GitHub (configs/code)

## Length

- `target_duration_seconds` between **180 and 300** (3–5 minutes)
- EN voiceover roughly 450–750 words; ZH should cover the same beats (not a loose summary)

## Voiceover rules

- Plain sentences only — no markdown, bullets, or headings
- Short TTS-friendly clauses
- Blank line between beats

## Content rules

- Skip long `pip` / install laundry lists; point to the site for full steps
- Every hard number must appear in the source chapter (or be tagged `[VERIFY]`)
- End CTA must name the handbook site and the GitHub repo/path

## Storyboard visual_source

Each storyboard row should note where the picture comes from for slideshow render:

- `chapter` — real handbook figure / CSV screenshot
- `svg` — generated diagram card (metrics, pipeline)
- `ai` — xAI (Grok Imagine) mood / concept / thumbnail / CTA art
