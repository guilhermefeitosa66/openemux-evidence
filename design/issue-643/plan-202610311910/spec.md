# Issue 643: hint bar button labels follow the connected controller (design spec)

Design artifact: https://claude.ai/artifact/7FQMERjQ4YiP4gDcfQ7pQ7 (private; this spec and the PNGs are the public copy).

## Principle
Actions stay on **positions**, as Android reports them (`BUTTON_A` = bottom face button). Only the **face** drawn in each hint-bar badge changes with the controller family. The confirm position (bottom, today's `"A"` token) keeps the accent fill (`Oe.AccentBright`, white face) in every family, so "the purple one confirms" holds everywhere.

## Token → face per family
Hint tokens used by the code today: `A`, `B`, `X`, `Y`, `L1 R1`, `L1`, `R1`, `START`, `SELECT` (and `L2`/`R2` only in the skin, out of scope).

| Token (position) | Xbox (default) | Nintendo | PlayStation |
|---|---|---|---|
| `A` (bottom) | A | B | cross (drawn) |
| `B` (right) | B | A | circle (drawn) |
| `X` (left) | X | Y | square (drawn) |
| `Y` (top) | Y | X | triangle (drawn) |
| `L1 R1` | LB RB | L R | L1 R1 |
| `L1` / `R1` | LB / RB | L / R | L1 / R1 |
| `START` | Menu icon (three lines, drawn) | + | OPTIONS |
| `SELECT` | View icon (two overlapping squares, drawn) | − (U+2212) | SHARE; CREATE on a DualSense (product 0x0CE6 / 0x0DF2) |

Any other token is drawn as its own text, unchanged.

## Badge
Unchanged geometry from `HintBar` today: height 22dp, min width 22dp, radius 11dp, `Oe.Raised` fill (`Oe.AccentBright` on the confirm position), horizontal padding 7dp when the face is text longer than one character, `Type.Tag` 11sp bold.
- Drawn faces (PlayStation shapes, Xbox Menu/View): vector, 11×11dp, stroke 1.6dp (cross 1.8dp, round caps), **stroked in the badge's text colour** (`Oe.Text`, or white on the accent). Never the coloured PlayStation glyphs, never a font glyph (font coverage of ✕○□△ varies by device).
- Two-part faces (`LB RB`, `L R`, `L1 R1`) are one badge with the text joined by a space, as `L1 R1` is today.
- Long faces (`OPTIONS`, `SHARE`, `CREATE`) rely on the existing `shrinkToFit()` row; nothing is dropped on a 390dp portrait phone (board 04).

## Accessibility
Each drawn face has a content description: "Cross", "Circle", "Square", "Triangle", "Menu", "View" (translated). Text faces are read as they are. The label next to the badge is unchanged.

## Settings → General → "Button labels"
Right after "Controller layout" (issue 642's row); without 642 merged, right after "Controls". Value shows the current choice.
- Phone: `ModalBottomSheet`, title "Button labels", lead "How the button hints name each button. The bottom button always confirms and the right one goes back.", four `RadioCard`s, hints A "Choose", B "Back". Split view: a pane with the same title, lead and cards.
- Each `RadioCard` uses its `leading` slot for a 44×44dp **face diamond**: four 15dp circles (top, left, right, bottom) with that family's faces at 8sp bold, the bottom one accent-filled. Decorative (`clearAndSetSemantics {}`); the title and description carry the meaning.
- Options (exact EN):
  - **Automatic** — "Follows the controller in use. Xbox style when it is not known." (diamond: Xbox faces)
  - **Xbox** — "A at the bottom, B on the right."
  - **Nintendo** — "B at the bottom, A on the right."
  - **PlayStation** — "Cross at the bottom, circle on the right."

## States
- Xbox / Nintendo / PlayStation pads (boards 01, 02); light theme (board 04); narrow portrait (board 04); settings sheet (board 03).
- No pad and Automatic: Xbox faces (today's look, pixel for pixel except START/SELECT, which become the Menu/View icons).
- Hint bar hidden (touch layout): nothing changes.

## Files
- 01-hint-bar-per-family.png — the library hint bar in the three families, dark.
- 02-library-landscape-nintendo.png — library, landscape, Nintendo pad (with issue 642's L/R pills).
- 03-settings-button-labels.png — the Button labels sheet, phone portrait, dark.
- 04-light-and-narrow.png — light theme, and the 390dp portrait row shrunk to fit.
