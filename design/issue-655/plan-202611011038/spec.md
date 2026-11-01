# Issue 655 — "All" card next to "Favorites" on the Android shelf

## Placement
- First shelf entries, before the consoles: **All**, then **Favorites**.
- **One column** (phone portrait, `shelfColumns(...) == 1`): one full-span grid item holding a `Row`
  (`Arrangement.spacedBy(spec.gap.dp)`) of two **compact** cards, `Modifier.weight(1f)` each,
  `IntrinsicSize.Min` height so both share the taller one. Min height = `spec.cardHeight` (104dp), so
  the pair takes no more height than today's single Favorites card.
- **Two or more columns** (landscape, tablets): All and Favorites are ordinary `ShelfCard`s, one
  column each, exactly like Favorites today (full icon tile, eyebrow, name, count).
- **No favorites:** All alone. In one column it is the regular full-width card (icon tile left);
  in more columns it is one ordinary card. Favorites stays hidden, as today.
- **Empty library:** neither card shows; the existing empty shelf is unchanged.

## Compact card (one column only)
- Same shape as the shelf cards: corner 22dp, padding 12dp vertical / 14dp horizontal,
  `gamepadFocus(corner = 22.dp, scale = 1.02f)`, `clickable(role = Role.Button)`.
- Layout: a `Column` with `SpaceBetween`.
  - Top row: eyebrow (Type.Tag, 11sp, letterSpacing 1sp, ink 72%, 1 line, ellipsis) at start;
    icon 30dp at end (Grid for All, filled Star for Favorites).
  - Bottom: name (Type.Title 18sp, ink, 1 line, ellipsis) and count (Type.Small, ink 78%, 1 line).
- Large font scale: the card grows (heightIn min), nothing clips.

## Look
| | Dark | Light |
|---|---|---|
| All background | linear gradient `#2F5D8A` → `#1E3A5A` | `#D3E3F5` → `#BCD3EE` |
| All ink / icon | White | `#12304F` |
| Favorites | unchanged (`#5B3FA8`→`#3A2A6E` / `#DDD3F8`→`#C6B8F0`, star `Oe.Star`) | unchanged |
- All icon: the existing `Icons.Grid` path, tinted with the card's ink. Full card: `card.star` size
  (42dp phone, 62dp tablet), like the star.

## Copy (EN)
- Eyebrow All: **LIBRARY** (new `library_all_eyebrow`).
- Name: compact card **All** (`library_chip_all`); full card **All games** (`library_all_games`).
- Count: `library_games_count` plural (existing).
- Favorites: unchanged strings.

## Gamepad and accessibility
- Both cards focusable; restorable focus keys `"ALL"` and `"FAV"`; initial focus = first shelf (All).
- D-pad left/right moves between them (Row order); down goes to the first console.
- Not consoles: no drag reorder, no move up/down actions, the Y menu does nothing on them.
- TalkBack: each card reads its name and count (merged semantics), role Button.
