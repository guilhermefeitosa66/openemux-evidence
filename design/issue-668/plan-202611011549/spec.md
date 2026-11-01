# Issue 668 — Android per-console BIOS import: UI spec

Design artifact: https://claude.ai/artifact/DKC3QYBQW7RCd6r4VjMXZj (private; the PNGs here mirror it).

Colours are the app's `Oe` tokens (`ui/Theme.kt`); type is the app's `Type` scale. Nothing new in the theme.

## BIOS screen (`BiosScreen`, `ui/SettingsScreens.kt`)

Top to bottom (phone; the tablet detail pane is the same column, `embedded = true`):

1. `BackLink("Settings")` (not when embedded), `Text("BIOS", Type.Display)`.
2. Intro paragraph, unchanged: `settings_bios_intro`.
3. **New** second paragraph, same style (`Type.Small`, 14 sp / 20 sp), replaces the old import card:
   `settings_bios_import_help` = "Use Import on a console and pick its files. Each file must have the name that console expects."
   The old surface card with the big "Import from device" `PrimaryButton`, the "Checking the files..." spinner row, `settings_bios_pick_help` and the green/amber result banner are **removed**.
4. `SectionHeader("Consoles with BIOS", "N of M ready")` — unchanged.
5. One `Card` per console (unchanged order and rows). The **header row** changes:
   - leading `ConsoleIcon(c)`; label `c.fullName`; **the "x of y" count moves under the name as the subtitle** (`settings_count_of`), so the trailing slot is free;
   - trailing: a compact **Import** button — new small variant of `SecondaryButton`: height 40 dp, horizontal padding 14 dp, radius 14 dp, `Oe.Surface2` background, `Oe.Text` label 14 sp semibold, 16 dp download icon (stroke 2.2) then 6 dp gap then "Import" (`settings_bios_import`). Row min height stays 60 dp, so the touch target is 48 dp+ including the row padding. `gamepadFocus(corner = 14.dp)` on the button; content description "Import BIOS for <console>" (`settings_bios_import_a11y`).
   - While that console's import runs: the button shows a 16 dp `CircularProgressIndicator` in place of the icon and is disabled (alpha `DISABLED_ALPHA`); other consoles' buttons stay usable but a second import while one runs is ignored (one import at a time screen-wide).
   - File rows below the header: unchanged (state icon, "One of these" + names, Required/Optional tag).
6. Footer `settings_bios_footer` — unchanged.

Gamepad: the hint bar on this screen keeps "A Import" / "B Back" (`settings_hint_import`, `settings_hint_back`); A on a focused Import button opens the picker. Focus moves down the Import buttons and the file rows as today (file rows are not focusable; only the buttons are), so D-pad up/down jumps console to console.

## Picker

`ActivityResultContracts.OpenMultipleDocuments()` launched with `arrayOf("*/*")` (BIOS extensions vary: .bin .rom .img .pce .gg .sms .nes .ic1; a MIME filter would hide exactly the oddly named file the summary should explain). Cancelling the picker does nothing (no sheet).

## Summary sheet (`OeSheet`, new `BiosImportSheet` composable)

Opens when the import ends, fully expanded, pad-navigable (that is what `OeSheet` gives).

- Header row: `ConsoleIcon(console)` 40 dp + column: title (20 sp semibold) and the console's full name (`Type.Small`).
- Title by outcome:
  - all imported: `settings_bios_result_all` plural — "%d file imported" / "%d files imported";
  - some: `settings_bios_result_some` — "%1$d of %2$d files imported";
  - none: `settings_bios_result_none` — "No files imported".
- Section "Imported" (`settings_bios_section_imported`), only when non-empty: a `Card` of rows, each: green check 18 dp (`Oe.Ok`, contentDescription "Imported"), title = the picked file's display name; subtitle, joined with " · ", only when there is something to say:
  - "Saved as %s" (`settings_bios_saved_as`) when the name on disk differs from the picked name (case fix or MD5 match);
  - "Recognized by its content" (`settings_bios_by_content`) when matched by MD5, not by name;
  - "Replaced the file that was there" (`settings_bios_replaced`) when a file with that name existed with different bytes.
- Section "Not imported" (`settings_bios_section_rejected`), only when non-empty: rows with the amber alert icon (`Oe.Warn`, contentDescription "Not imported"), title = picked name, subtitle in `Oe.WarnText`, one of:
  - "Not a name this console expects" (`settings_bios_reason_name`);
  - "Could not be read or saved" (`settings_bios_reason_io`);
  - "Too large to be a BIOS" (`settings_bios_reason_size`).
- "<Console> expects" (`settings_bios_expects`, `%s` = full name) as a small heading, then every file name of that console's entries joined with " · " (`Type.Small`, wraps). Always shown, so a rejected player knows what to rename to.
- `PrimaryButton("Done")` full width at the bottom (`settings_bios_done`); first pad focus lands on it; B / back / scrim tap also close.

States drawn: mixed batch (dark), nothing imported (light). The all-imported state is the mixed one without the "Not imported" section.

## Refresh

When the sheet opens, the console card already shows the new state (rows flip to the green check and the subtitle count changes) — the refresh happens on import end, not on sheet close.

## Accessibility

- Import button: role Button, label "Import BIOS for Sony PlayStation".
- State icons carry contentDescription; colour is never the only signal (sections are labelled).
- Contrast: `Oe.WarnText` on `Oe.Sheet` passes 4.5:1 in both themes (same pair the old result banner used on `WarnBg`; verify in dev with the existing palette test if any).

## Adaptive

- Phone portrait: as drawn (390 dp).
- Tablet list + detail (`splitSettings`): the BIOS screen is the detail pane (`embedded = true`); same column, max width as today. The sheet opens over the whole window, as other `OeSheet`s do.
- Landscape: `OeSheet` scrolls its content; Done stays reachable.
