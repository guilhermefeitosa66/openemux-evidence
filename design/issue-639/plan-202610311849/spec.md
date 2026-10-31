# Issue 639: "RetroArch menu" entry in the Android pause sheet

The dashed outline in the images only marks the new element; it is not drawn in the app.

## Component
- One `ListRow` (ui/Components.kt), reused as is: `label = "RetroArch menu"`,
  `subtitle = "Advanced settings, for this session only"`, `divider = true`, a trailing
  chevron (`Icons.Chevron`, TextDim), `minHeight` default (grows to fit the subtitle).
- Phone portrait, phone landscape and tablet side panel: third row of the existing `rest`
  group, after "Restart game", inside the same rounded `Oe.Raised` block. It stays above
  "Quit game" so the destructive button keeps its place at the foot.
- Tabletop (bottom half): a full-width row under the "Save states · Restart · Quit" row,
  `Oe.Raised`, 56 dp, radius 16, same label + subtitle + chevron.
- Same row in hardcore sessions (RetroArch enforces its own hardcore restrictions inside its menu).

## Behaviour
- Tap / A on the row: the sheet closes and RetroArch's own menu (MaterialUI) opens over the game.
  No confirmation dialog: the subtitle already says what it is, and B/BACK leaves the menu.
- Gamepad: reachable with D-pad like every other row (gamepadFocus already in ListRow).

## Strings (EN, values/strings_game.xml)
- `game_retroarch_menu` = "RetroArch menu"
- `game_retroarch_menu_note` = "Advanced settings, for this session only"

## Accessibility
- Role Button (ListRow). Text contrast: Text on Raised and TextDim on Raised, both above 4.5:1
  in light and dark.
