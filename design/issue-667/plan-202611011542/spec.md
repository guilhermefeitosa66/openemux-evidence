# Issue 667 — Import BIOS files: UI spec

## Settings → BIOS page (`OpenEmuxPreferences._build_bios_page`)

- `Adw.PreferencesGroup` "BIOS" stays. Description changes to `bios.instructions`:
  "Import BIOS files and OpenEmux copies each one into its console's folder. File names must match the ones listed below."
- Header suffix (`Gtk.Box`, horizontal, spacing 6):
  1. `Gtk.Button` "Import BIOS…" — `suggested-action` class, `valign CENTER`, child `Adw.ButtonContent`
     (icon `document-open-symbolic`, label `bios.import.button`, `use_underline`). Tooltip none (label says it).
  2. Existing reload button (`view-refresh-symbolic`, flat, tooltip "Reload BIOS status") kept.
  - The "Open ROMs folder" header button is removed.
- Per-console `Adw.ExpanderRow` ("ID — Name", subtitle "present/total", console icon prefix):
  - the folder suffix button is removed from the collapsed row;
  - a last child row `Adw.ActionRow` "Show folder" (`bios.show_folder`), `activatable`, prefix icon
    `folder-symbolic`, suffix icon `adw-external-link-symbolic`; activating it calls
    `win._open_console_bios_folder(console_id)` (unchanged behaviour, quieter placement).
- Narrow window (≤ 400 px): `Adw.PreferencesGroup` header wraps naturally; the button keeps its label.
  If the header suffix does not fit, it is acceptable for the description to wrap above it (libadwaita does this).

## Import flow

- Click → `Gtk.FileDialog` titled `bios.import.dialog_title` ("Import BIOS Files"), modal,
  `open_multiple`. No file filter (BIOS extensions vary: .bin .rom .img .pce .gg .sms .nes .ic1);
  an "All files" filter is the default.
- Dismissed → nothing happens. Chosen → copy runs on a worker thread (files are small, but the
  portal path can be slow); the button is insensitive while it runs.
- When done: `_reload_bios()` (rows rebuilt, no toast) and the summary dialog.

## Summary dialog (`Adw.AlertDialog`)

- Heading:
  - all imported: `bios.import.heading_all` — "{count} BIOS files imported" (singular "BIOS file imported" via a separate key `bios.import.heading_one`)
  - some: `bios.import.heading_some` — "{imported} of {total} files imported"
  - none: `bios.import.heading_none` — "No files imported"
- Body: `bios.import.body` — "File names must match exactly. Settings → BIOS lists the expected names under each console."
  Shown only when at least one file was rejected.
- Extra child: `Gtk.ScrolledWindow` (propagate natural height, max-content-height 320, hscroll never)
  holding a `Gtk.ListBox` with `boxed-list` class, selection none:
  - section label rows (`Gtk.Label`, `heading` + `dim-label`, not selectable/activatable): "Imported" (`bios.import.section_imported`), "Not imported" (`bios.import.section_rejected`); a section is omitted when empty;
  - imported row: `Adw.ActionRow` title = file name (`use_markup` false), subtitle = "ID — Console name",
    or `bios.import.replaced` "{console} · replaced the existing file" when it overwrote one;
    prefix `emblem-ok-symbolic` with `success` class;
  - rejected row: title = file name, subtitle = reason; prefix `dialog-warning-symbolic` with `warning` class.
    Reasons: `bios.import.reason_unknown` "Not a BIOS name OpenEmux knows";
    `bios.import.reason_error` "Could not copy: {error}".
- One response "OK" (`bios.import.ok`), default and close response.
- Accessibility: icons carry accessible labels ("Imported" / "Not imported"); row titles are the file names;
  focus starts on OK; Esc closes.

## States shown in the design

1. BIOS page, light, PS expanded with "Show folder".
2. Summary, mixed batch (3 imported incl. one replaced, 2 rejected: unknown name, copy error), light.
3. BIOS page at 360 px, dark.
4. Summary, nothing imported, dark.

## New strings (EN)

| key | text |
|---|---|
| bios.instructions (edited) | Import BIOS files and OpenEmux copies each one into its console's folder. File names must match the ones listed below. |
| bios.import.button | _Import BIOS… |
| bios.import.dialog_title | Import BIOS Files |
| bios.import.heading_one | BIOS file imported |
| bios.import.heading_all | {count} BIOS files imported |
| bios.import.heading_some | {imported} of {total} files imported |
| bios.import.heading_none | No files imported |
| bios.import.body | File names must match exactly. Settings → BIOS lists the expected names under each console. |
| bios.import.section_imported | Imported |
| bios.import.section_rejected | Not imported |
| bios.import.replaced | {console} · replaced the existing file |
| bios.import.reason_unknown | Not a BIOS name OpenEmux knows |
| bios.import.reason_error | Could not copy: {error} |
| bios.import.ok | OK |
| bios.import.running | Importing BIOS files… |
| bios.show_folder | Show folder |

Retired: `bios.open_roms_folder`, `bios.open_console_folder` (remove from every locale once unused).
