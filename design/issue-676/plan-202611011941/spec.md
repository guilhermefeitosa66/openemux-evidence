# Issue 676: theme toggle sun icon (spec)

## Widget
Unchanged: the `Gtk.Button` built by `_build_theme_button()` in the content header bar,
icon-only, tooltip `header.theme.to_light` / `header.theme.to_dark`
("Switch to the light theme" / "Switch to the dark theme"). Only the icon *names* change.

| State | Icon name | Drawing |
|---|---|---|
| App is dark (click gives light) | `openemux-sun-symbolic` | new, OpenEmux's own (MIT) |
| App is light (click gives dark) | `openemux-moon-symbolic` | byte copy of Adwaita `weather-clear-night-symbolic` (LGPL-3 / CC-BY-SA-3.0), look unchanged |

## Sun geometry (16×16 viewBox, single fill `#222222`, no strokes)
- Ring: outer radius 4, inner radius 2 (2 px band), centred at (8, 8), even-odd fill.
- Rays: 8 pills, 2 px wide × 2.5 px long, `rx` 1 (round caps), from radius 5.5 to 8,
  every 45°. Gap ring→ray: 1.5 px.
- Same 2 px stroke weight as the moon's crescent, so the pair reads as one set.
- Cardinal rays touch the viewBox edge, like Adwaita's own sun.

Reference SVG: `openemux-sun-symbolic.svg` (attached). The dev may flatten the rects to one
path; the rendering must stay identical.

## Why own names
On a host theme that ships `weather-clear-symbolic` (Numix/Numix-Circle, Papirus, ...),
the theme's drawing wins over the bundled copy. Numix draws a scalloped blob that reads as a
plain circle at 16 px: that is the bug. A name no theme ships always resolves to the bundled SVG.

## Themes / accessibility
- Symbolic recolor: the button's foreground in both themes (dark-on-light, light-on-dark).
- Contrast is the header's foreground color, unchanged.
- Tooltip is the accessible label (unchanged, translated in every locale).
- No adaptive behaviour change; HiDPI: scalable SVG.
