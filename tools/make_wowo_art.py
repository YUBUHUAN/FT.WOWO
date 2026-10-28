from PIL import Image, ImageDraw, ImageOps
import numpy as np
from pathlib import Path

ROOT = Path(r"D:/made in harness/wowo-src")
SRC_SLEEP = r"C:/Users/29107/.dsh/attachments/v1/objects/2d/2d63616559b02949845356403323d2f0b92255fb2d94b09d817c7eb5cc5a2bb4"
SRC_AWAKE = r"C:/Users/29107/.dsh/attachments/v1/objects/a0/a053e9dc46148e35b28f1a0bde7acc84556eb75189aca181b9a06b53c406eeab"


def cutout(path):
    src = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", src.size, (255, 255, 255, 255))
    bg.alpha_composite(src)
    img = bg.convert("RGB")
    magic = (255, 0, 255)
    for x in range(0, img.width, 40):
        for y in (0, img.height - 1):
            try: ImageDraw.floodfill(img, (x, y), magic, thresh=24)
            except Exception: pass
    for y in range(0, img.height, 40):
        for x in (0, img.width - 1):
            try: ImageDraw.floodfill(img, (x, y), magic, thresh=24)
            except Exception: pass
    arr = np.array(img)
    alpha = np.where((arr[:, :, 0] > 245) & (arr[:, :, 1] < 15) & (arr[:, :, 2] > 245), 0, 255).astype(np.uint8)
    # watermark boxes outside the character
    alpha[:240, :430] = 0
    alpha[1740:, 1650:] = 0
    rgba = np.dstack([np.array(bg)[:, :, :3], alpha])
    out = Image.fromarray(rgba, "RGBA")
    return out.crop(out.getbbox())


def canvas(img, height=960):
    scale = height / img.height
    w = max(1, int(img.width * scale))
    resized = img.resize((w, height), Image.LANCZOS)
    c = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    c.alpha_composite(resized, ((1000 - w) // 2, 1000 - height - 10))
    return c


sleep_src = Image.open(SRC_SLEEP).convert("RGBA")
awake_src = Image.open(SRC_AWAKE).convert("RGBA")

sleep_cut = cutout(SRC_SLEEP)
awake_cut = cutout(SRC_AWAKE)
sleep = canvas(sleep_cut)
awake = canvas(awake_cut)

for rel in ["web/assets/pet.png", "desktop-native/Assets/pet.png"]:
    awake.save(ROOT / rel)
for rel in ["web/assets/pet-sleep.png", "desktop-native/Assets/pet-sleep.png"]:
    sleep.save(ROOT / rel)

# avatar: face crop from the awake portrait, circular-safe transparent square
face = awake_src.crop((580, 300, 1480, 1200)).convert("RGBA")
# remove white background around the face crop
f = face.convert("RGB")
for x in range(0, f.width, 30):
    for y in (0, f.height - 1):
        try: ImageDraw.floodfill(f, (x, y), (255, 0, 255), thresh=22)
        except Exception: pass
for y in range(0, f.height, 30):
    for x in (0, f.width - 1):
        try: ImageDraw.floodfill(f, (x, y), (255, 0, 255), thresh=22)
        except Exception: pass
arr = np.array(f)
a = np.where((arr[:, :, 0] > 245) & (arr[:, :, 1] < 15) & (arr[:, :, 2] > 245), 0, 255).astype(np.uint8)
face = Image.fromarray(np.dstack([np.array(face)[:, :, :3], a]), "RGBA").crop(Image.fromarray(a).getbbox())
face.thumbnail((440, 440), Image.LANCZOS)
av = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
av.alpha_composite(face, ((512 - face.width) // 2, (512 - face.height) // 2))
for rel in ["web/assets/avatar-round.png", "desktop-native/Assets/avatar-round.png"]:
    av.save(ROOT / rel)

# app icon from avatar
ico = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
av_small = av.resize((256, 256), Image.LANCZOS)
ico.alpha_composite(av_small)
ico.save(ROOT / "desktop-native/Assets/app.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

print("wowo art", sleep_cut.size, awake_cut.size, "avatar", face.size)
