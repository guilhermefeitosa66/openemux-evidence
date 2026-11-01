# Issue 670 — Android landscape game detail (spec)

Window: a phone on its side, e.g. 800×360dp (worst case 732×360dp), the 80dp phone rail on the left
(it already shows on the detail route). All sizes in dp. Colours are the existing `Oe` tokens.

## Layout
Row filling the window under the status bar (`statusBarsPadding`), end-side `displayCutout`/nav-bar
insets respected.

### Left column — 42% of the content width
- Header row (40dp buttons, 8dp gap): Back (`RoundIconButton(Icons.Back)`), spacer, Favourite, More
  options (same composables as today's `favoriteButton` / `menuButton`). Padding 6dp top, 16dp start, 12dp end.
- Cartridge: centred, sized by height — the space left after the header and the title block, capped
  at the column width; `Cartridge(...)` with `aspectRatio(cartAspect, matchHeightConstraintsFirst = true)`.
  Violet `Glow` behind it, as in portrait. Shadow ellipse kept.
- Title: `Type.Title` at 19sp, **1 line, ellipsis**, centred, 8dp above.
- Info line: `"{console} · {core} · {time played}"`, `Type.Small`, 1 line, ellipsis, 2dp above.
- Bottom padding 10dp + `hintBarInset`.

### Right column — the rest
Scrolls vertically (`verticalScroll`), padding 12dp top, 12dp start, 20dp end.
1. Play buttons: `playButtons(48.dp, 112.dp)` — Continue (primary, weight 1) + Restart; hardcore or no
   auto state: Play alone. 
2. 14dp · **Save states** header + "See all (N)" link; one row of 3 `StateThumb` at 50dp thumbs
   (`statesSection(3, 50.dp)`); empty: "None yet. Save from the in-game menu."
3. 14dp · **Cartridge color** header with the current colour name (+ " · default"), then
   `ColorSwatches` (already a horizontally scrolling `FocusRow`) with a 56dp fade on the end edge
   while it can scroll further. Only for consoles with cartridge frames (as today).
4. 14dp · **Settings for this game** (`detail_settings_for_game`, existing string) + `settingsCard`.
5. Bottom spacer 28dp + `hintBarInset`.
- A 44dp fade at the bottom of the column (above the hint bar) while it can scroll down
  (`scrollState.canScrollForward`).

## Height budget (360dp window, 24dp status bar, 40dp hint bar → 296dp)
12 + 48 (buttons) + 14 + 98 (states) + 14 + 72 (colour) = 258dp ≤ 296dp → Continue, Restart and the
swatches are visible without scrolling; the settings card starts under them, half visible, with the fade.

## States shown
- default (dark, touch) · gamepad hint bar + focus ring on Continue · hardcore (Play only, no states)
  · light theme · narrow 732×360dp with the hint bar.

## Gamepad
Initial focus on Continue/Play (`restorableFocus("play")`, as today). Traversal: Back → Favourite →
Menu (left header), Right from there or from the cartridge enters the right column at the play
buttons, then down: states row, See all, swatches row, settings rows. Left from the right column
goes back to the header. Hints unchanged (A Continue/Play, X Favourite, Y Menu, B Back, L1/R1 siblings).

## Accessibility
Same content descriptions as today; cartridge is decorative-with-label as now; swatches keep
`Role.RadioButton` + colour names. Contrast uses the existing tokens.

## Strings
No new strings: every text already exists in `strings_game.xml`.
