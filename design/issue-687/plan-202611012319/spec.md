# Issue 687 — Share nearby as a scroll-driven sequence: design spec

Design artifact: https://claude.ai/artifact/PaDn6SW4N1JaFoDYcoDp1y (artboards: Main = stage at step 2, Steps = the four
states, Reduced = reduced-motion strip, Phone = 390 px).

## Structure
- `section#share.moment` keeps its header (eyebrow "Share nearby", h2, lede) in normal flow above the stage.
- Below it, the scroll stage from issue 686's engine: a tall track (desktop 400 vh, phone 300 vh) with a
  sticky 100 vh stage. Progress 0 → 1 is split in four equal bands; band k shows step k.
- Stage content (desktop ≥ 900 px): phone (236×512 frame, 8 px black bezel, radius 34) left, a quiet
  "Wi-Fi" mark (three gold dots, label in muted) between, desktop window (720 px wide, 28 px title bar
  with three dots, radius 14) right; gap 56 px; centered. Under them: a four-segment step indicator
  (active segment 40×4 gold, done 22×4 at 25 % white, upcoming at 12 %), the caption (22 px/600) and its
  second sentence (17 px, muted). Soft violet radial glow behind, as in the opening.
- Phone width (< 900 px): desktop window on top (full width minus 2×16 px gutter), phone (176×380) below
  it, indicator, caption under the stage; shorter track.

## Steps (same game "Robot Man X" and code 506 807 on both sides)
| Step | Phone layer | Desktop layer | Caption (line 1 / line 2) |
|---|---|---|---|
| 1 | phone-1-pick | desktop-1-ready | "Pick a game on your phone." / "Your computer shows up in the list by itself." |
| 2 | phone-2-code | desktop-2-offer | "The same code shows on both screens." / "If they match, accept on the computer." |
| 3 | phone-3-progress | desktop-3-progress | "The game goes straight over your Wi-Fi." / "No account, no cloud, no cable." |
| 4 | phone-4-sent | desktop-4-received → desktop-4-library (cross-fade in the second half of band 4) | "It is in your library now." / "Pick it up where you left off." |

## Motion
- Within each device frame the step captures are stacked layers; entering a band cross-fades the next
  layer in (opacity, ~8 % of total progress) and the outgoing one out. The phone gets a 12 px upward
  settle (`translateY`) on each change; the desktop does not move. Only `transform`/`opacity`.
- Captions: each step's caption is its own element; it fades in (opacity + 8 px rise) when its band is
  reached and the previous one fades out. Revealed once per pass, no typing effect.
- No snap, no wheel/touch capture, no scroll-jacking; the page scrolls normally through the track.

## Reduced motion / no JS without CSS timelines
- Static strip (artboard "Reduced"): header, then an `<ol>` of four cards in a row (2×2 at ≤ 900 px,
  one column at ≤ 520 px). Each card: desktop capture top-right, phone capture overlapping bottom-left,
  number in gold, both caption lines. No sticky track (section height is its content).

## Accessibility
- Every capture has alt text (translated) describing the screen, naming the game and the code.
- The step captions are real text in an `<ol>` (screen readers read all four in order whatever the
  scroll); hidden steps are visually faded, not `display:none`, and the stage is not `aria-live`.
- Contrast: caption #f4f1ff and muted #a9a2c4 on #08060f both pass 4.5:1.
