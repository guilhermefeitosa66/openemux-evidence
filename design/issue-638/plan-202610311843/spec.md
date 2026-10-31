# Issue 638 — Android slow-motion toggle: UI spec

Design artifact: https://claude.ai/artifact/8P9ZULmEYkEdRQosQ5LpGu (private)

## Glyph (24 x 24 grid, stroked like the turbo bolt: 1.8/24 stroke, round joins and caps)
A play triangle inside a dashed ring (8 dashes):

    M13.17 3.08A9 9 0 0 1 17.48 4.86M19.14 6.52A9 9 0 0 1 20.92 10.83M20.92 13.17A9 9 0 0 1 19.14 17.48M17.48 19.14A9 9 0 0 1 13.17 20.92M10.83 20.92A9 9 0 0 1 6.52 19.14M4.86 17.48A9 9 0 0 1 3.08 13.17M3.08 10.83A9 9 0 0 1 4.86 6.52M6.52 4.86A9 9 0 0 1 10.83 3.08M10 8.5v7l5.5-3.5z

Add it as `Icons.SlowMotion` (Components.kt) and use the same string for the skin strip. In Compose it is drawn stroked (not `filled`).

## Skin strip (SkinRenderer.strip)
- Order: save_state, load_state, turbo_fire_toggle, **toggle_slowmotion**, toggle_fast_forward, then "screens" on NDS.
- Even slots; portrait 390 dp: 5 slots of 78 dp (NDS 6 x 65). Landscape strip under the picture: slot = width / count; the lit pill keeps the existing rule `min(46, slot - 8)` x 30, radius 10, ring 1.5.
- Lit: accent pill (#7C3AED) with light inner ring (#D4C4FF), glyph white, via `_lit_by = slow_motion` (`OverlayWriter.LIT_BY`).
- Hardcore: glyph at 0x73 alpha (45%), no touch desc, no lit pill (same as fast forward).
- Accessibility: the overlay draws no text (as today).

## Pause sheet (PauseSheet tile row)
- Order: Fast forward, **Slow motion**, Screenshot, Shader, (Screens on NDS), Audio.
- Tile = existing `ActionTile`: 60 dp square, radius 18, on = AccentSoft + 1.5 dp AccentBright border + AccentOnSoft glyph; off = Surface2 + Text glyph. Label "Slow motion" (Caption, medium).
- Hardcore: tile disabled (`enabled = false`, 45% alpha, not focusable), never shown on.
- Width: when the row cannot hold every tile at 68 dp (60 + 4 padding on each side), the tiles wrap into rows of equal columns (6 tiles → 3 + 3, 5 → 3 + 2) instead of shrinking; gamepad focus moves across rows (D-pad up/down/left/right). Wide windows keep one row.
- Toast on tap: on → "Slow motion on resume" (`game_toast_slow_motion_on`); off → the existing "Normal speed" (`game_toast_fast_forward_off`, reused as-is).
- Turning slow motion on in the sheet turns the Fast forward tile off at once (and vice versa), mirroring the engine.

## Strings (strings_game.xml, every locale: en, de, es, fr, ja, pt-rBR, ta, zh-rCN)
- `game_slow_motion` = "Slow motion"
- `game_toast_slow_motion_on` = "Slow motion on resume"

## States shown in the artifact
Default; slow motion on; turbo + slow motion on; hardcore; narrowest landscape strip with NDS screens; pause sheet dark (on), light (default), hardcore, NDS at 360 dp (wrapped).
