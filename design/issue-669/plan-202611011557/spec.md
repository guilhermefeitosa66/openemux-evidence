# Issue 669 · Landscape game list: single top row (design spec)

Scope: `LandscapeLibrary` in `ui/LibraryScreens.kt` (the `layout.short && !tabletop && mode != List` branch).
Portrait, tabletop, tablets (never `short`) and List mode are unchanged.

## Row

One `Row`, height 44dp (pad layout: the targets grow as they do today through `padSize` / `gamepadFocus`),
`padding(start = 20.dp, end = 20.dp, top = FocusOutset)`, `verticalAlignment = CenterVertically`, 8dp between groups.

Order (start → end, mirrored in RTL):

1. **Back**: `RoundIconButton(Icons.Back, "Shelf")`, icon only (the "Shelf" text label goes). Same action: `popBackStack(Routes.SHELF, false)`.
2. **Filter pager** (`weight(1f)`, 4dp gaps):
   - **Previous**: 40dp round, transparent. Touch: `Icons.Back` chevron 20dp. Pad layout (`InputMode.padLayout`): the shoulder face for `"L1"` as a pill (same look as `ShoulderPill` / `PadBadge`, 22dp high, `Oe.Raised`). Disabled (alpha 0.38, not clickable) on the first filter.
   - **Label** (a button, 40dp high, 12dp corner, 10dp horizontal padding, 8dp gaps): icon + name + count + caret.
     - Icon 20dp: `ConsoleIcon(console, 20.dp)` for a console; `Icons.Star` filled in `Oe.Star` for Favorites; none for All.
     - Name: `FitText`, `Type.Title` at 18sp SemiBold, `Oe.Text`. "All games" / "Favorites" / `console.displayName` (same strings as today's title).
     - Count: the bare number, locale-formatted (`NumberFormat.getIntegerInstance()`), `Type.Small` 13sp `Oe.Muted`; no string resource. "24 games" would not fit.
     - Caret: 14dp chevron down (`Oe.Muted`), up while the menu is open. Hidden in the pad layout.
   - **Next**: like Previous, chevron right / `"R1"` face; disabled on the last filter.
3. **Search**: `RoundIconButton(Search | Close)`, unchanged.
4. **Sort**: `RoundIconButton(Sort)`, unchanged.
5. **View toggle**: `ViewToggle`, unchanged, 4dp start padding.

## Width bands (pure function, row width = the Row's own max width in dp)

| Row width | Prev/Next | Icon | Name | Count | Caret |
|---|---|---|---|---|---|
| ≥ 680dp | yes | yes | displayName | yes | yes (touch) |
| 480–679dp | yes | yes | displayName | no | no |
| < 480dp | no | no | `console.short` | no | yes (touch) |

640×360dp phone with the 80dp rail → 560dp content → 520dp row: the middle band. 800×360 → 680dp row: the full band.

## Filter menu

Tapping the label (or A on it) opens a Material3 `DropdownMenu` anchored under the label, wrapped in
`CompositionLocalProvider(LocalPadScope provides …)` as the detail screen's menu does, so D-pad/A/B work in it.
Items, 40dp each: All games, Favorites, then each console with games in `orderedConsoles(meta.consoleOrder)`;
each with its icon (none for All), name (`displayName`), and the count right-aligned (`Type.Small`, `Oe.Muted`).
The current one is highlighted (`Oe.AccentSoft` background, `Oe.AccentOnSoft` text). Picking one sets the filter
and clears `focusedRom` like `chip()`.

## Search open

The pager is replaced by `SearchField` (same widget, `weight(1f)`, no top padding inside the row). The Search button
becomes Close. Placeholder: "Search in %1$s" with the filter name for a console/Favorites, "Search all games" for All
(new strings). Closing clears the query, as today, and brings the pager back. L1/R1 still switch the filter while
searching (unchanged behaviour); the placeholder follows.

## Gamepad

- The "L1 R1 → Console" hint leaves the hint bar while this row is shown (the row shows the shoulders itself).
- Every control is a `gamepadFocus` target: up from the games reaches the row, left/right walks it.
- The label's focus ring follows `gamepadFocus(corner = 12.dp)`.

## Accessibility

- Back: "Shelf". Previous: "Previous filter: %1$s"; Next: "Next filter: %1$s" (the neighbour's name); disabled ones
  report disabled.
- Label: "Filter: %1$s, %2$s. Change filter" with the full name and the games count (plural), role Button,
  regardless of the band (so the short name and the hidden count are still read).
- Menu items: role menu item, selected state on the current one.
- Contrast: `Oe.Muted` on `Oe.Bg` passes 4.5:1 in both themes (existing tokens).

## Heights (360dp tall phone, 80dp rail)

| | Before | After |
|---|---|---|
| Bands above the games | 56 + 44 (+54 with search) | 56 |
| Cartridge height (`itemH`) | 176dp | 220dp |
| Same, with the hint bar | 136dp | 180dp |

## Strings (EN)

- `library_previous_filter` "Previous filter: %1$s"
- `library_next_filter` "Next filter: %1$s"
- `library_filter_label` "Filter: %1$s, %2$s. Change filter"
- `library_search_in` "Search in %1$s"
- `library_search_all` "Search all games"
