from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(r"D:/made in harness/wowo-src")
pet = Image.open(ROOT / "web/assets/pet.png").convert("RGBA")
out = ROOT / "test"
out.mkdir(exist_ok=True)

BG = (250, 244, 237, 255)
PINK = (246, 219, 216, 255)
BLUSH = (243, 195, 195, 255)
INK = (45, 40, 50, 255)

# source crops
full = pet
bust = pet.crop((140, 40, 860, 760))
head = pet.crop((210, 0, 790, 620))


def icon(name, src, scale, bg=BG, circle=PINK):
    size = 512
    im = Image.new("RGBA", (size, size), bg)
    d = ImageDraw.Draw(im)
    d.ellipse((40, 40, 472, 472), fill=circle)
    # tiny decorative stars, barely visible at small sizes
    d.ellipse((98, 92, 112, 106), fill=(238, 222, 170, 210))
    d.ellipse((418, 386, 430, 398), fill=(238, 222, 170, 210))
    w = int(src.width * scale)
    h = int(src.height * scale)
    art = src.resize((w, h), Image.LANCZOS)
    im.alpha_composite(art, ((size - w) // 2, (size - h) // 2 + 8))
    # rounded outer border preview
    d.rounded_rectangle((1, 1, size - 2, size - 2), radius=112, outline=(255, 255, 255, 220), width=3)
    im.save(out / f"icon-{name}.png")
    return im


a = icon("a-full", full, 0.43)
b = icon("b-bust", bust, 0.63)
c = icon("c-head", head, 0.67)

# preview sheet: large + real small sizes
W, H = 1500, 760
sheet = Image.new("RGB", (W, H), (246, 240, 233))
d = ImageDraw.Draw(sheet)
try:
    f_title = ImageFont.truetype(r"C:/Windows/Fonts/msyhbd.ttc", 30)
    f = ImageFont.truetype(r"C:/Windows/Fonts/msyh.ttc", 24)
    f_small = ImageFont.truetype(r"C:/Windows/Fonts/msyh.ttc", 18)
except Exception:
    f_title = f = f_small = ImageFont.load_default()
d.text((70, 35), "喔喔 · 手机图标候选", font=f_title, fill=INK)
d.text((70, 78), "先确认，再把选中的替换到安装包里", font=f_small, fill=(120, 110, 105))

items = [("A 全身", a), ("B 半身", b), ("C 完整头部", c)]
for i, (label, img) in enumerate(items):
    x = 70 + i * 480
    sheet.paste(img.convert("RGB").resize((400, 400), Image.LANCZOS), (x, 130))
    d.rounded_rectangle((x, 130, x + 400, 530), radius=88, outline=(80, 74, 86), width=2)
    d.text((x, 548), label, font=f, fill=INK)
    small = img.resize((96, 96), Image.LANCZOS).convert("RGB")
    sheet.paste(small, (x, 590))
    d.text((x + 112, 600), "实际小图标 96px", font=f_small, fill=(120, 110, 105))
    tiny = img.resize((56, 56), Image.LANCZOS).convert("RGB")
    sheet.paste(tiny, (x + 112, 636))
    d.text((x + 180, 646), "56px", font=f_small, fill=(120, 110, 105))
sheet.save(out / "icon-candidates.png")
print("icons ready")
