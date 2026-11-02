"""Procedural relief render of the Game Boy (Color) cartridge frame.

Builds a height map of the cartridge front in the frame's own 177x200 unit
space (same layout as the current GBC.svg, label window included), lights it
with a directional light, casts real shadows across the height field and adds
ambient occlusion. The label window stays transparent; the lip's shadow onto
the label is baked in as a translucent dark overlay.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 12                      # render pixels per frame unit (supersampled)
OUT = int(sys.argv[1]) if len(sys.argv) > 1 else 4   # output pixels per unit
W, H = 177, 200
PW, PH = W * S, H * S
FONT_DIR = "/usr/share/fonts/truetype/noto/"


def P(v):
    return int(round(v * S))


def canvas():
    return Image.new("L", (PW, PH), 0)


def arr(img):
    return np.asarray(img, dtype=np.float32) / 255.0


def box_blur(a, r, axis):
    if r < 1:
        return a
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r + 1, r)
    c = np.cumsum(np.pad(a, pad, mode="edge"), axis=axis)
    n = a.shape[axis]
    hi = np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    return (hi - lo) / (2 * r + 1)


def blur(a, sigma_units):
    """Approximate gaussian (3 box passes) with sigma in frame units."""
    sigma = sigma_units * S
    r = max(1, int(round(np.sqrt(12 * sigma * sigma / 3 + 1) / 2)))
    for _ in range(3):
        a = box_blur(a, r, 0)
        a = box_blur(a, r, 1)
    return a


# ---------------------------------------------------------------- shapes
def body_mask():
    im = canvas()
    d = ImageDraw.Draw(im)
    # Main shell, top-right step (the lock notch) as in the current frame.
    d.rounded_rectangle([P(3), P(3), P(172), P(196.5)], radius=P(2.2), fill=255)
    d.rectangle([P(157.5), 0, PW, P(13)], fill=0)
    d.rounded_rectangle([P(158), P(13), P(172), P(30)], radius=P(1.6), fill=255)
    d.rectangle([P(158), P(20), P(172), P(40)], fill=255)
    return arr(im)


def plate_mask():
    im = canvas()
    ImageDraw.Draw(im).rounded_rectangle(
        [P(22.5), P(13.5), P(152.5), P(50.5)], radius=P(17), fill=255)
    return arr(im)


def grooves_mask():
    im = canvas()
    d = ImageDraw.Draw(im)
    for y in (19.6, 25.6, 31.6, 37.6, 43.6):
        d.rectangle([P(2), P(y), P(20.5), P(y + 1.5)], fill=255)
        d.rectangle([P(154.5), P(y), P(175), P(y + 1.5)], fill=255)
    return arr(im)


def recess_mask():
    im = canvas()
    ImageDraw.Draw(im).rounded_rectangle(
        [P(22.5), P(56), P(153), P(173.5)], radius=P(3.2), fill=255)
    return arr(im)


def window_mask():
    im = canvas()
    ImageDraw.Draw(im).rounded_rectangle(
        [P(25.8), P(60), P(150), P(170.2)], radius=P(2.6), fill=255)
    return arr(im)


def side_steps_mask():
    im = canvas()
    d = ImageDraw.Draw(im)
    d.rectangle([0, P(84), P(6.2), PH], fill=255)
    d.rectangle([P(168.8), P(84), PW, PH], fill=255)
    return arr(im)


def arrow_mask():
    im = canvas()
    d = ImageDraw.Draw(im)
    d.polygon([(P(77), P(177.5)), (P(100), P(177.5)), (P(88.5), P(190.5))], fill=255)
    inner = canvas()
    ImageDraw.Draw(inner).polygon(
        [(P(80.6), P(179.3)), (P(96.4), P(179.3)), (P(88.5), P(188.0))], fill=255)
    return np.clip(arr(im) - arr(inner), 0, 1)


def text_mask():
    im = canvas()
    d = ImageDraw.Draw(im)
    f_nin = ImageFont.truetype(FONT_DIR + "NotoSans-Black.ttf", P(7.6))
    f_gb = ImageFont.truetype(FONT_DIR + "NotoSansDisplay-SemiCondensedBlackItalic.ttf", P(12.6))
    f_tm = ImageFont.truetype(FONT_DIR + "NotoSans-Bold.ttf", P(3.2))
    base = P(38.2)
    nin, gb = "Nintendo", "GAME BOY"
    w_nin = d.textlength(nin, font=f_nin)
    w_gb = d.textlength(gb, font=f_gb)
    gap = P(2.2)
    w_tm = d.textlength("TM", font=f_tm)
    total = w_nin + gap + w_gb + P(0.8) + w_tm
    x0 = P(87.5) - total / 2
    d.text((x0, base), nin, font=f_nin, fill=255, anchor="ls")
    d.text((x0 + w_nin + gap, base), gb, font=f_gb, fill=255, anchor="ls")
    d.text((x0 + w_nin + gap + w_gb + P(0.8), base), "TM", font=f_tm, fill=255, anchor="ls")
    return arr(im)


# ---------------------------------------------------------------- height
def build():
    body = body_mask()
    win = window_mask()
    soft = lambda m, s: blur(m, s)

    h = np.zeros((PH, PW), np.float32)
    h += 2.4 * soft(body, 0.85)                     # shell with rounded rim
    h -= 0.55 * soft(side_steps_mask(), 0.25)       # lower side steps
    h -= 0.75 * soft(plate_mask(), 0.45)            # recessed logo plate
    h += 0.50 * soft(text_mask(), 0.10)             # embossed lettering
    h -= 0.55 * soft(grooves_mask(), 0.35)          # grip grooves
    h -= 0.60 * soft(recess_mask(), 0.40)           # label recess
    h -= 0.55 * soft(arrow_mask(), 0.12)            # engraved arrow
    label_floor = h - 0.9 * soft(win, 0.12)         # the label sits below the lip
    h = np.where(win > 0.5, label_floor, h)

    # Fine plastic grain, very low amplitude.
    rng = np.random.default_rng(7)
    grain = blur(rng.standard_normal((PH, PW)).astype(np.float32), 0.10)
    h += 0.0035 * grain / (grain.std() + 1e-6)
    return h, body, win


def shade(h, body, win):
    hu = h  # heights are in frame units
    gy, gx = np.gradient(hu, 1.0 / S)
    n = np.dstack([-gx, -gy, np.ones_like(hu)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)

    el = np.deg2rad(32)
    L = np.array([-np.cos(el) * 0.70710678, -np.cos(el) * 0.70710678, np.sin(el)])
    ndl = np.clip((n * L).sum(2), 0, 1)

    # Cast shadows: march toward the light across the height field.
    dirx, diry = L[0], L[1]
    norm_xy = np.hypot(dirx, diry)
    dirx, diry = dirx / norm_xy, diry / norm_xy
    slope = np.tan(el)
    occ = np.zeros_like(hu)
    step = 0.25                 # units
    for k in range(1, 28):
        t = k * step
        dx, dy = int(round(-dirx * t * S)), int(round(-diry * t * S))
        # sample h at p + t*dir_to_light (light comes from -x,-y screen)
        shifted = np.roll(np.roll(hu, dx, axis=1), dy, axis=0)
        occ = np.maximum(occ, shifted - hu - t * slope)
    shadow = 1 - np.clip(occ / 0.18, 0, 1)
    shadow = 0.25 + 0.75 * blur(shadow, 0.15)        # soft penumbra

    # Ambient occlusion from the local height deficit.
    ao = 1 - np.clip((blur(hu, 1.6) - hu) * 0.55, 0, 0.45)
    ao *= 1 - np.clip((blur(hu, 0.5) - hu) * 0.6, 0, 0.25)

    # Specular (satin plastic).
    V = np.array([0, 0, 1.0])
    Hh = (L + V) / np.linalg.norm(L + V)
    spec = np.clip((n * Hh).sum(2), 0, 1) ** 28 * 0.22 * shadow

    albedo = np.array([0.80, 0.80, 0.815])
    ambient = 0.50
    light = ambient * ao + 0.80 * ndl * shadow
    rgb = albedo[None, None, :] * light[..., None] + spec[..., None]
    # Gentle top-to-bottom falloff so it does not read flat.
    yy = np.linspace(1.03, 0.95, PH)[:, None, None]
    rgb = np.clip(rgb * yy, 0, 1)

    alpha = np.clip(body, 0, 1)
    # Inside the window: only the lip's shadow and occlusion, over the label.
    dark = np.clip(1 - shadow * ao, 0, 1)
    win_a = np.clip(dark * 1.25, 0, 0.75)
    alpha = np.where(win > 0.5, win_a * win, alpha)
    rgb = np.where(win[..., None] > 0.5, 0.05, rgb)
    return rgb, alpha


def main():
    h, body, win = build()
    rgb, alpha = shade(h, body, win)
    rgba = np.dstack([rgb, alpha])
    img = Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), "RGBA")
    big = img.resize((W * OUT, H * OUT), Image.LANCZOS)
    big.save(f"gbc_frame_{OUT}x.png")
    print("saved", big.size)


if __name__ == "__main__":
    main()
