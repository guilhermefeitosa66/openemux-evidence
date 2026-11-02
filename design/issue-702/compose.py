import sys
from PIL import Image, ImageOps
frame_path, label_path, out, scale = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
fr = Image.open(frame_path).convert("RGBA").resize((177*scale, 200*scale), Image.LANCZOS)
lab = Image.open(label_path).convert("RGBA")
bx, by, bw, bh = 24.137932, 59.874607, 128, 110
box = (round(bw*scale), round(bh*scale))
lab = ImageOps.fit(lab, box, Image.LANCZOS)
canvas = Image.new("RGBA", fr.size, (0,0,0,0))
canvas.paste(lab, (round(bx*scale), round(by*scale)))
canvas.alpha_composite(fr)
bg = Image.new("RGBA", (fr.width+40, fr.height+40), (36,36,40,255))
bg.alpha_composite(canvas, (20,20))
bg.convert("RGB").save(out)
