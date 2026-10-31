# Issue 642 — Android gamepad layout: design spec

Design artifact (private): https://claude.ai/artifact/F9coYr1VEENnivK3q7txD7

The gamepad layout is the current screens with the gamepad look held on while a controller is
connected (or the setting says Always). No new screen and no new component: existing `gamepadFocus`
ring, `HintBar`, `GamepadButtons` hints, `RadioCard`, `ListRow`, theme tokens (`Oe.*`, `Type.*`).

## States

| State | Focus ring | Hint bar | L1/R1 pills by the chips | Focus target sizes |
|---|---|---|---|---|
| Touch layout (no pad, or setting Never and the last input was touch) | hidden | hidden | hidden | today's |
| Gamepad layout (pad connected + Automatic, or Always) | always on one item | always shown | shown | the larger ones below |
| Mixed (gamepad layout, user taps) | moves to the tapped item, stays visible | stays | stays | larger |

Never: the layout is the touch one, and pad presses still navigate with today's "last input" look
(ring and hints appear on a press, go away on a touch), as before this issue.

## Screens (artboards)

1. **Gamepad layout, library, landscape** (`01`): rail 72dp; header "Library" + console chips
   flanked by `L1` and `R1` pills (Tag style, 11sp bold, `Oe.Raised` background, 11dp radius,
   3×8dp padding); focused cartridge scaled 1.08, ring 3dp `Oe.AccentText` 3dp outside, 6dp halo
   `Oe.AccentBright` at 28%; unfocused titles at 60% opacity (today's behaviour); hint bar 40dp at the
   bottom, never hidden. Library hints: A "Details", X "Favorite", Y "Options", "L1 R1" "Console",
   START "Select", B "Shelf".
2. **Touch layout** (`02`): today's library, unchanged (no ring, no hint bar, no L1/R1 pills, chips 30–36dp).
3. **Mixed** (`03`): with a pad connected, a tap on a game moves focus (and the ring) to it; the
   hint bar stays. The next D-pad press moves from the tapped item on the first try.
4. **Settings → Controller layout** (`04`): a `ListRow` "Controller layout" in General, right after
   "Controls", value = the current choice. Opens a `ModalBottomSheet` (phone) / pane (split), titled
   "Controller layout", with three `RadioCard`s:
   - **Automatic** — "The controller layout while a controller is connected." (default)
   - **Always** — "For handhelds with built-in controls."
   - **Never** — "The touch layout, even with a controller connected."
   Hints: A "Choose", B "Back".
5. **Light theme** (`05`): same as 1 with light tokens (ring `#6D28D9`, accent `#7C3AED`).
6. **Portrait** (`06`): same rules; bottom tab bar sits above the 40dp hint bar; chips row scrolls with L1/R1 pills at its ends.

## Larger focus targets (gamepad layout only)

Minimum 44dp tall for anything focusable; specifically:
- library console chips 36dp → 40dp; `ViewToggle` 40×32dp → 44×40dp;
- `ColorSwatches` 38dp → 44dp; RA sign-out pill and `PolicyChip` 36dp → 40dp;
- text links (`settings_see_which`, `ra_see_progress`, "See all", import "go to shelf", shelf section links):
  min height 44dp with horizontal padding so the ring has a real target;
- rail buttons keep 52dp.
Touch layout keeps today's sizes so the touch design does not change.

## D-pad paths and shoulders

- Up/Down/Left/Right follow the visual grid; the existing holds (`holdFocusAtEnd`) keep focus at list ends.
- L1/R1 on every screen with sections: library (console chips, already), shelf and recent (main tabs,
  already), Settings (main tabs, already); **new**: sub-routes reached from Settings (console settings,
  BIOS, achievements, backup, about, share) switch the main tab too, through the global handler,
  instead of doing nothing; the detail in Pane style keeps falling through to the console chips.
- Every screen's hints include "L1 R1" when the shoulders do something there.

## Accessibility

- Hint text 12sp `Oe.Muted` on `Oe.Bg` at 94% (passes 4.5:1 in both themes, as today).
- Ring contrast unchanged. The setting sheet is a normal radio group (`RadioCard` with `selected` semantics).
- Every new string translated (de, es, fr, ja, pt-rBR, ta, zh-rCN).

## Adaptive

- Phone landscape (primary, controller grip): rail + 40dp hint bar; content keeps `hintBarInset` padding so the
  last focused item is never under the bar.
- Phone portrait: bottom bar + hint bar under it (today's arrangement).
- Tablet / split: hint bar spans the content pane, as today.
- Tabletop (foldable): hint bar on the bottom half, as today.
