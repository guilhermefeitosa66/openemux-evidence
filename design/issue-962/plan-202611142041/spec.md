# Issue 962 - Big Picture console chips with icons (spec)

Sizes at Big Picture scale 1.0 (1080p); everything else scales with the theme.

- Every chip in the console row (`bp-chip`, games page) gets an icon at the left of its name.
- Console chip: the console's pixel-art PNG (`console_texture()`, the shelf's art), 32 px native.
  Drawn at the largest whole multiple of 32 px that fits the icon slot (1x at 1080p), with
  nearest-neighbour scaling; when the slot is smaller than 32 px (720p, scale ~0.67) it is drawn at
  the slot size with the smooth (trilinear) filter, since nearest-neighbour downscaling drops pixel rows.
- Console with no PNG asset: its symbolic system icon (`get_icon_name()`), the sidebar's fallback.
- All: `view-grid-symbolic`; Favorites: `starred-symbolic`; playlists: `user-bookmarks-symbolic`
  (the shelf cards' icons), 24 px, in the chip's text colour so they follow current/focus states.
- Icon slot 32 px (`chip_icon`), symbolic glyph 24 px (`chip_glyph`), 10 px between icon and name.
- Chip height stays `chip_h` (56 px); horizontal padding unchanged.
- States unchanged: default `surface2`, current white `#F3F3F6`, focus `#3B2A6B`, focused current
  `#4E3A8C`. The pixel art keeps its own colours on every background.
- Filter chips (Favorites · N, Has save state · N, Missing artwork · N) are not touched.
- No new strings.
