# Issue 891 design spec

- Actions bar of a selected single button (BUTTON or KEYPAD, not a combo, not D-pad/stick/frame action): a new first tool "Shape" (icon: rounded square outline 22dp), before Colour. Combos keep their own Shape tool.
- Shape row (existing ShapeRow, issue 842): radio group, 40dp-high cells, weight 1 each, Done (44x40, accent) at the end.
  Order for a button: Original (reset arrow icon), Circle, Pill, Rounded square, Triangle bottom left / bottom right / top left / top right.
  Order for a combo: same minus Original (a combo's own outline is the circle).
  Selected cell: Lilac 18% fill + 1.5dp Lilac border, icon Lilac.
- Strings (EN): "Original", "Rounded square" (new); "Shape", "Circle", "Pill", "Triangle, bottom left"... (existing).
- Changing a shape keeps the control's centre; a circle, square or triangle is as wide as tall, a pill 1.6 x 0.8 of the circle it was; Original brings back the skin's own outline and proportions.
- Pressed tint, in game: over the button's own drawing, 30% black on a light face (luminance > 0.5), 35% white on a dark face; only on the button's opaque pixels. Each D-pad arm has its own tint (a wedge from the centre to that side). Shown while the overlay presses the input, gone on release.
