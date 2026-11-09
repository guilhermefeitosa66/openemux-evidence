# Restart confirmation (issue 831)

In-window modal over the pause sheet: scrim (0x8C08080A), centred card 320dp wide (max: window minus 48dp), padding 24dp, corner 28dp, Oe.Sheet.
Title "Restart game?" (Type.Title, 20sp). Body "Your progress since the last save will be lost." (Type.Small).
Actions right-aligned: "Cancel" (Type.Section), "Restart" (Type.Section, Oe.Danger). 44dp minimum height.
Gamepad: focus lands on Cancel, left/right moves, up/down stays, A chooses, B cancels. A tap on the scrim cancels.
Tabletop: the card sits in the half below the fold.
