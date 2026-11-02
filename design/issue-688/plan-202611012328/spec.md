# #688 Cartridge and skin galleries — spec

Design artifact: https://claude.ai/artifact/JDrbiLtHczLEFUj9gxKQGW

## Gallery component (shared by both)
- `div.gal[role=region][aria-roledescription=carousel][aria-label]` > `ul.gal-track[tabindex=0]` (native `overflow-x: auto`, `scroll-snap-type: x mandatory`, scrollbar hidden, `overscroll-behavior-x: contain`) > `li.gal-slide[role=group][aria-roledescription=slide][aria-label=<console>]` (`scroll-snap-align: center`).
- Controls under the track: Previous (44 px round, disabled at the first slide), dots (one 28×44 button per slide, aria-label = console, `aria-current=true` on the active one; active pill 22×8 gold, others 8×8 at 32 % text), Next (disabled at the last). Gap 18 px desktop / 8 px phone.
- Keyboard: Tab reaches the track and every control; ←/→ on the focused track go to the previous/next slide, Home/End to the ends. Focus ring: 3 px `--gold`, offset 3 px.
- Smooth scrolling between slides; `prefers-reduced-motion: reduce` → instant jumps, no transitions.
- Active slide tracked from scroll position (rAF-throttled `scroll` + `scrollend`); no autoplay, no wrap-around.

## Cartridges (desktop)
- Six slides: Super Nintendo, Nintendo (NES), Game Boy Advance, Nintendo 64, Mega Drive, PlayStation (captures `docs/assets/desktop/cart-*.png`, 2640×1756).
- One slide per view at every width. The capture **is** the window: `border-radius: 12px` (10 px ≤ 520 px), `box-shadow: 0 0 0 1px rgba(255,255,255,.08), 0 30px 80px rgba(0,0,0,.55)`. **No title bar, no traffic lights, no drawn chrome** (the capture already has the libadwaita header bar and its own window buttons).
- Console name under the window (19 px / 600), as `figcaption`.

## Skins (phone)
- Six slides: Super Nintendo, Game Boy Advance, Nintendo 64, Mega Drive, PlayStation, Nintendo DS (`docs/assets/android/game-*-portrait.png`, 1080×2238). GBA and NDS slides also hold the landscape capture beside the portrait (stacked under it at ≤ 700 px).
- Phone frame = two rounded rectangles. Body `box-sizing: border-box`, `padding: var(--bezel)`, `display: grid; place-items: center`; screen = body − 2 × bezel, `radius = body radius − bezel` (concentric).
  - ≥ 700 px: portrait body 236×472 r34, bezel 8 → screen 220×456 r26; landscape body 472×236 r34 → screen 456×220 r26.
  - < 700 px: portrait body 176×352 r26, bezel 6 → screen 164×340 r20; landscape body 324×163 r26 → screen 312×151 r20.
- Several slides per view on desktop (gap 48 px), one per view on a phone. Console name under each slide (17 px / 600).

## Page
- No horizontal page scroll at 360 px: the gallery scrolls inside itself only, never the page; no snap on the page.
- Images through the `<picture>` helper (AVIF/WebP + PNG fallback, explicit size, lazy).
