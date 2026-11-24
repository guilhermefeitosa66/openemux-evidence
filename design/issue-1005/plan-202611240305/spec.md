# Issue 1005: Game files on the Android detail screen

Design artifact: https://claude.ai/artifact/K7S6UNAnzSgu7x6X8fLhTo

## Placement
A section "GAME FILES" (Type.SectionCaps header, as the Backup screen's section headers) and a Card of ListRows between the game's settings card and "Remove from library", on every style (Phone, Pane, Landscape, TwoColumns). In tabletop the same card goes above the Remove card, full width.

## Rows (in this order)
1. **Export game file**: value = the size ("16 MB"); a multi-file game: "3 files · 512 MB". Always shown.
2. **Export game save**: value = when the save was written ("Today, 14:02" / date). Only when the game has a save.
3. **Import game save**: subtitle "From another emulator or a backup". Always shown, except for consoles whose cores keep saves outside the game's name (GameCube, PSP).
4. **Restore previous save**: subtitle "The save replaced on <date>". Only while a replaced save is kept.

While an export/import runs, the row's value reads "Exporting…" and the rows are disabled; a long ROM export shows progress in the row value ("128 MB of 512 MB") and keeps the screen on. Results are toasts: "Exported “<name>”", "Save imported", "Previous save restored", and the failures ("Could not export the file", "Could not import the save", "Close the game first: it is running").

## Import confirmation (OeConfirmDialog)
- Title: "Replace this game's save?" (no current save: "Use this file as the game's save?")
- Text: "“<file>” becomes the save of <game>. The current save is kept, and “Restore previous save” brings it back." (no current save: only the first sentence)
- Warning lines, when they apply: size mismatch ("This file is 64 KB; <console> saves of this game are 128 KB. It may not be a save of this game."), unknown extension ("“.xyz” is not a usual save file extension.").
- Always: "Saves from other emulators usually work, but not always." When a suspended game (auto state) exists: "Start the game with Restart: Continue resumes the suspended game with its old progress."
- Buttons: Cancel / Replace (or "Import" when there is no current save).

## Refusals (toast, no dialog)
Game running, empty file, file larger than 32 MB, a save state or ROM picked.

## Restore
Confirm dialog "Restore the previous save?" / "The save in use now is kept in its place, so you can switch back." / Restore · Cancel.

## Gamepad and TalkBack
Rows are ListRows (gamepadFocus + one focus stop each, A activates, B backs out as today). TalkBack reads label, value/subtitle. Dialogs are OeConfirmDialog (pad-aware).
