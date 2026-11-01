# Issue 658 — console group label (Android library) — design spec

Design artifact: https://claude.ai/artifact/3d5PbfhGjTeDFpNy8GBVxv

## Components (Compose, existing)
- Icon: `ConsoleIcon(console, size)` from `ui/Components.kt` (pixel art, unsmoothed; falls back to `ConsoleChip` for a console with no icon).
- Text styles: `Type.Caption` (Inter Medium 12sp, `Oe.Muted`) for the landscape label; `Type.Section` 17sp for the portrait header (as today).

## Caption text
- `"<short> – <displayName>"` with an EN DASH and spaces, via a new string resource `library_group_caption` = `%1$s – %2$s` (every locale; the dash is kept, translators may change the spacing).
- Game count keeps `R.plurals.library_games_count`.

## Landscape single row (window height Compact, Carts/Covers view)
- No header item in the `LazyRow`: tiles of consecutive consoles follow with the normal 24dp gap.
- Label row: height 18dp, drawn at the top of the row area (top = 8dp), over the room the row already leaves above the tiles. The tiles keep their size (`itemH` unchanged).
- Content: `ConsoleIcon` 16dp, 6dp gap, caption in `Type.Caption` (`Oe.Muted`), then `· 12 games` in `Type.Caption` with `Oe.Faint`. One line, no wrap; ellipsis if it would pass the next group's label.
- Position: each group's label starts at its first tile's left edge (x = tile offset); while that tile has scrolled past the row's start (contentPadding 32dp), the label sticks at x = 32dp. When the next group's first tile approaches, the next label pushes the current one out: current x = min(32dp, nextLabelX − 12dp − currentLabelWidth).
- RTL: mirror (start edge is the right).
- Not focusable; the label is drawn under the row (z-order), so the focus ring of a scaled tile is never covered.

## Portrait / tablet / list mode (`GroupHeader`, full-width line)
- `ConsoleIcon` 24dp (replaces the 40dp `ConsoleChip` square), 10dp gap, caption `"<short> – <name>"` in `Type.Section` 17sp, one line with ellipsis, count at the end in `Type.Caption`. Top padding 10dp as today.

## Accessibility
- The label and the header are headings (`semantics { heading() }`) and read "SNES – Super Nintendo, 9 games"; the icon has no content description (decorative).
- Contrast: `Oe.Muted` on `Oe.Bg` is ≥ 4.5:1 in both themes (#A3A3B2 on #121216, #5C5C6B on #F6F5F9).

## States
1. Landscape dark: first group label at the start.
2. Landscape dark: SNES group arriving, NES label pushed out.
3. Landscape light.
4. Portrait header, dark and light.
- Single console page (no groups): no label, no header — unchanged.
- Empty / no results: unchanged (no label).
