# Issue 656: Game Boy Color shelf icon (Android)

## Asset
- File: `pkg/android/openemux/src/main/res/drawable-nodpi/console_gbc.png`, 32×32 RGBA, same canvas, outline and drop shadow as `console_gb.png` (it is a recolour of it, pixel for pixel).
- Regions (from `console_gb.png`) and their new colours, each a luminance ramp so the original shading survives:
  - Body (grey, low saturation): yellow ramp `#966E0A` (shadow) to `#FFE250` (highlight). Mid body lands around `#F0C838`.
  - Screen bezel (lavender): blue ramp `#162C78` to `#5080DC`.
  - A/B buttons (magenta): the same blue ramp.
  - Screen (brown): dark slate ramp `#1A2226` to `#3A4A4E` (a GBC screen, switched off).
  - Unchanged: D-pad and other dark details, red power LED, transparent pixels and the semi-transparent outline/shadow.
- No Pikachu figure: at 32×32 it would be 2–3 pixels and read as noise; the yellow/blue pair is what identifies the edition.

## Mapping
- `Console.kt` icon map: `"GBC" to R.drawable.console_gbc` (GB keeps `console_gb`).

## Where it shows (all through `ConsoleIcon`)
- Shelf card (64dp phone, 96dp tablet), settings console lists (40dp), and every other `ConsoleIcon` use. Integer scaling with `FilterQuality.None` is already in place.

## Legibility
- Dark theme card `#5A3A6B`, light theme card `#DCC3EA` (derived by `Console.shelf()`): the yellow body and the dark outline keep the silhouette clear on both; the blue bezel separates the screen.

## Images
- `compare_x4.png`: GB and GBC on the GBC card, dark then light, at 4×.
- `gbc_x10_dark.png`, `gbc_x10_light.png`: the new icon at 10× on each card colour.
- `console_gbc.png`: the prototype asset at 1×.
