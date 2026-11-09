# #829 Background transfer: UI spec

**Progress view** (existing sheet and the send screen's inline view): adds a `SecondaryButton` "Continue in Background" above "Cancel Transfer", both full width, 52 dp, 10 dp apart. The note changes to "You can keep using the app, play a game, leave the app or turn off the screen. The transfer keeps going."

**Back / B while a transfer runs:** leaves the progress view; the transfer continues. It no longer asks to cancel. Cancel stays in the view, with the existing confirmation.

**Transfer chip:** same look as the label-sync toast. 48 dp tall, radius 14, `Oe.Divider` background, 24 dp shadow, centered, 12 dp above the tab bar (rail: 12 dp from the bottom, right of the rail; tabletop: bottom half). Download icon for receiving, Upload for sending, 18 dp, `Oe.AccentText`. Text "Receiving" or "Sending" SemiBold `Oe.Text`, then " · 42%" Medium `Oe.Muted`; no percent before the size is known. Tap, or A with gamepad focus, opens the progress view. Accessibility: Role.Button, description "Show transfer progress", percent read from the visible text. Hidden while a progress view is open and on games' own screens.

**Result:** unchanged card; shown over whatever screen is open when the transfer ends, or on return to the app. Notification as today.

**Narrow / rail / tabletop:** the chip has no fixed width and follows the toast's placement in each layout. Light and dark use the theme tokens.

**Waiting for the receiver's answer (sender):** unchanged, stays on the send screen because the code must be visible.
