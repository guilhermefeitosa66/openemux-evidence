# Install section (issue 689), design spec

Palette and tokens are the site's own (--bg, --bg-2, --panel, --line, --violet, --violet-deep, --gold, --text, --muted, --radius). Dark only, like the rest of the page.

## Structure
1. Eyebrow "Get started", h2 "Installing", lede (unchanged strings).
2. Platform tablist (aria-label "Platform"): "Linux", "Windows" + BETA badge, "Android". Pill track on --bg-2; selected tab uses the primary button gradient. 44 px min height. At <= 560 px the three tabs share the width equally (grid of 3); the BETA badge drops under "Windows".
3. Tab panel: a .card (no hover lift). Linux and Windows panels start with a second tablist (aria-label "Linux package" / "Windows build"): Flatpak, AppImage, .deb, .rpm / Installer, Portable. Selected format chip is gold (like .step-n), others ghost.
4. Format panel: h3 + one muted line, the primary download button (btn-primary with a download glyph; full width under 560 px), then an <ol> of 2-3 steps with gold number squares (the existing .step-n look). Commands sit in the existing <pre><code> box with a "Copy" button top right (pre gets right padding so text never runs under it; on phones the code wraps).
5. "Copy" state: icon + "Copy" → "Copied" with a check, mint background (#c7f0d8, dark text) for 2 s; announced through an aria-live region. Fallback when the Clipboard API is missing or refused: the command text is selected and the button reads "Press Ctrl+C" (Cmd+C on Mac).
6. "Verify your download": <details> on --bg-2 with a shield glyph in gold; closed by default. Content = today's text and both commands, each with a copy button.
7. "All files on the Releases page →" link, then the build-from-source line (unchanged).

## Behaviour
- Pre-selection: Android user agent → Android; Windows → Windows; anything else → Linux. Linux format: Ubuntu/Debian in the UA → .deb, Fedora → .rpm, otherwise Flatpak.
- Keyboard: roving tabindex; Left/Right move and activate, Home/End jump; focus ring 2 px gold, offset 3 px.
- Without JavaScript: no tabs, every panel stacked and visible (today's layout), buttons point at the releases page.

## Strings (EN)
Platform, Linux package, Windows build, Copy, Copied, Press Ctrl+C, Download the .flatpak, Download the AppImage, Download the .deb, Download the .rpm, Download the installer, Download the .zip, Download the APK, step texts as in the mockups, All files on the Releases page →.
