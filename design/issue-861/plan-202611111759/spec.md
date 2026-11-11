# Issue 861: pause sheet Audio tile
- Tile size unchanged (60dp box, 18dp corner, 22dp icon, caption label).
- Sound on: icon Icons.Audio, label "Mute", background Oe.Surface2, no border, icon Oe.Text.
- Muted: icon Icons.Mute, label "Unmute", background Oe.DangerBg, 1.5dp border Oe.Danger, icon Oe.Danger. Label stays Oe.Text.
- Updates on tap while the sheet is open; reopened sheet shows the engine's state.
- Gamepad focus ring unchanged. TalkBack reads the label (the action a tap does).
