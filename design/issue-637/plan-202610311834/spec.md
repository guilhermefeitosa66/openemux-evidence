# Issue 637: in-game controls with a gamepad, and collapse/restore

Everything here is drawn into the RetroArch overlay bitmaps by `SkinRenderer` (no Android View). It uses the drawn skin's existing palette, not the app theme: the skin is always dark, so light/dark theme does not apply. Sizes are in skin units (`SkinGeometry.unit`). The px values below are for a 390 dp wide phone; they scale with `unit` like every other key.

## Tokens (existing skin values)
- Rail / strip body: the skin's body colour (`#1d1d22` on the default dark skin, the console colour on coloured skins)
- Round key (menu, hide): fill `#2a2a31`, icon `#c9c9d3`
- Strip icon: `#8e8e9a`, same glyphs as today (save ↓, load ↑, bolt, ▶▶)
- Lit state (turbo/FF on): unchanged from the `litPill` look (accent `#7c3aed` pill, light ring, white icon)
- Hardcore FF: icon at 0.45 alpha, no desc (unchanged)
- Restore key: round key at 50% alpha (fill and icon), the "eye" glyph

## New glyphs
- **Hide controls**: eye with a slash (stroke, same weight as the bolt)
- **Show controls**: eye
Both drawn with the same `Path` stroke style as the bolt in `SkinRenderer`.

## Layouts

### Gamepad, phone landscape (01)
- Two side rails, each 88 dp wide (≈ 1.4 × the round key), full height, skin body colour.
- Left rail: Menu (round key, top), then Save and Load near the bottom (thumb reach).
- Right rail: Turbo and Fast forward near the top, Hide (round key) at the bottom.
- NDS: the "screens" key goes on the right rail, under Fast forward.
- Picture: aspect fit into the screen minus both rails, centred. On a 20:9 phone a 4:3 game uses the full height (the rails sit in what was pillarbox).

### Gamepad, phone portrait (05)
- One bottom strip, 96 dp high, with the bottom safe inset below it.
- Six evenly spaced cells: Menu, Save, Load, Turbo, Fast forward, Hide (NDS: a seventh cell, Screens, before Hide).
- Picture: full width, centred vertically in the space above the strip.

### Gamepad, tablet (07)
- Same as the phone in each orientation, scaled by `unit` (rails ≈ 104 dp, keys 60 dp).

### Gamepad, tabletop / foldable half-open (08)
- Picture in the upper half (as today's tabletop).
- Lower half: the six keys in one centred row (the portrait strip, larger). No virtual buttons.

### Touch, any layout (03)
- Unchanged, plus one round **Hide** key right beside the Menu key, same size and style.
- Imported package skins (.deltaskin/.manicskin) do not get a Hide key: their art is the skin author's. With a gamepad they use the drawn gamepad layout above.

### Collapsed (02, 04, 06)
- All app controls go: Menu, Hide, Save, Load, Turbo, Fast forward, Screens, keypad pill, lit pills.
- One **Show controls** key stays, at 50% alpha, exactly where the Menu key is in the expanded layout of the same page.
- Touch collapsed: the virtual game buttons and the picture rect are unchanged (the game must not jump); the strip area is left as plain body colour.
- Gamepad collapsed: no rails or strip; the picture is fit to the whole screen (safe insets respected), so a wide game grows.
- Tapping Show controls returns to the same layout, expanded.

## Behaviour
- Pad connected → gamepad layout; disconnected → touch layout; no restart. Collapsed/expanded is kept across that switch and across rotation, tabletop and window resizes.
- Every game starts expanded (state is not persisted across sessions).
- Fast-forward lit and the hardcore dimming look the same in every layout.

## Accessibility
- Touch targets ≥ 48 dp in every layout (the restore key too).
- Contrast: key icons ≥ 4.5:1 against the body (unchanged palette). The restore key is deliberately faint (50%) like the desktop's show button; it stays ≥ 48 dp so it is easy to hit.
- No text labels in the overlay (as today); the pause sheet stays the accessible way to reach every action.

## Strings
None are drawn in the overlay. No new strings are needed (see the plan).
