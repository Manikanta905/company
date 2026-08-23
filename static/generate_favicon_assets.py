from pathlib import Path
from PIL import Image, ImageDraw

base_dir = Path(__file__).resolve().parent

img = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
d = ImageDraw.Draw(img)

# Outer white rounded-square canvas
# Main blue MK shape
mk_points = [
    (55, 360), (55, 120), (110, 120), (170, 250),
    (230, 120), (285, 120), (285, 360), (220, 360),
    (220, 210), (170, 310), (120, 210), (120, 360)
]
d.polygon(mk_points, fill=(18, 110, 214, 255))

# Gray arc/swoosh
arc_box = (55, 100, 475, 475)
d.arc(arc_box, start=220, end=70, fill=(61, 66, 72, 255), width=35)

# Blue dot accent
# d.ellipse((354, 40, 454, 140), fill=(10, 105, 216, 255))
# Better to keep the dot centered in the arc area
# Use a slightly smaller circle to stay within the final shape
for x0, y0, x1, y1, color in [
    (355, 38, 442, 125, (10, 105, 216, 255)),
]:
    d.ellipse((x0, y0, x1, y1), fill=color)

# Small pixel-style squares
pixel_boxes = [
    (155, 132, 195, 172, (31, 41, 55, 255)),
    (195, 117, 235, 157, (31, 41, 55, 255)),
    (235, 142, 275, 182, (31, 41, 55, 255)),
    (265, 172, 305, 212, (31, 41, 55, 255)),
    (250, 212, 290, 252, (10, 105, 216, 255)),
    (215, 242, 255, 282, (10, 105, 216, 255)),
    (170, 232, 210, 272, (31, 41, 55, 255)),
]
for x0, y0, x1, y1, color in pixel_boxes:
    d.rounded_rectangle((x0, y0, x1, y1), radius=8, fill=color)

# Save standard assets
img.save(base_dir / "favicon-192x192.png")
img.resize((32, 32)).save(base_dir / "favicon-32x32.png")
img.resize((180, 180)).save(base_dir / "apple-touch-icon.png")

# ICO requires multiple sizes
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
icon_images = []
for size in sizes:
    icon_images.append(img.resize(size).convert("RGBA"))
img.save(base_dir / "favicon.ico", format="ICO", sizes=sizes)

print("Created favicon assets:")
for name in [
    "favicon-192x192.png",
    "favicon-32x32.png",
    "apple-touch-icon.png",
    "favicon.ico",
]:
    print(f" - {name}")
