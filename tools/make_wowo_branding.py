from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(r"D:/made in harness/wowo-src")
pet = Image.open(ROOT / "web/assets/pet.png").convert("RGBA")
avatar = Image.open(ROOT / "web/assets/avatar-round.png").convert("RGBA")

# web/PWA icons and legacy sizes
avatar.resize((256, 256), Image.LANCZOS).save(ROOT / "web/assets/avatar.png")
avatar.resize((64, 64), Image.LANCZOS).save(ROOT / "web/assets/tray.png")
pet.resize((560, 560), Image.LANCZOS).save(ROOT / "web/assets/pet-560.png")
for size in (192, 512):
    avatar.resize((size, size), Image.LANCZOS).save(ROOT / f"web/assets/icon-{size}.png")
    # maskable: keep a safe margin
    canvas = Image.new("RGBA", (size, size), (251, 246, 238, 255))
    inner = avatar.resize((int(size * 0.78), int(size * 0.78)), Image.LANCZOS)
    canvas.alpha_composite(inner, ((size - inner.width) // 2, (size - inner.height) // 2))
    canvas.save(ROOT / f"web/assets/maskable-{size}.png")
avatar.resize((256, 256), Image.LANCZOS).save(
    ROOT / "web/assets/app.ico",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)

# portrait source for docs / future art edits
portrait = Image.new("RGB", (1024, 1024), (251, 246, 238))
p = pet.resize((900, 900), Image.LANCZOS)
portrait.paste(p, (62, 100), p)
portrait.save(ROOT / "assets-src/portrait.jpg", quality=94)

# single Wowo hero used by README
W, H = 1600, 900
hero = Image.new("RGB", (W, H), (251, 246, 238))
d = ImageDraw.Draw(hero)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(251 - 10 * t), int(246 - 8 * t), int(238 - 4 * t)))
# soft blush circle behind the character
d.ellipse((740, 30, 1560, 850), fill=(246, 218, 215))
p = pet.resize((740, 740), Image.LANCZOS)
hero.paste(p, (760, 120), p)
try:
    title_font = ImageFont.truetype(r"C:/Windows/Fonts/msyhbd.ttc", 96)
    sub_font = ImageFont.truetype(r"C:/Windows/Fonts/msyh.ttc", 34)
    small_font = ImageFont.truetype(r"C:/Windows/Fonts/msyh.ttc", 24)
except Exception:
    title_font = sub_font = small_font = ImageFont.load_default()
d.text((120, 260), "喔喔", font=title_font, fill=(33, 30, 38))
d.text((124, 390), "住在桌面上的 ENFP 小女孩", font=sub_font, fill=(75, 69, 82))
d.text((124, 452), "我觉得，今天会发生一点好事。", font=sub_font, fill=(141, 131, 119))
d.text((124, 540), "摸摸她 · 喂她 · 带她出门 · 陪她睡觉", font=small_font, fill=(127, 145, 121))
d.rounded_rectangle((120, 620, 450, 676), radius=28, fill=(33, 30, 38))
d.text((150, 632), "Wowo · 桌面桌宠", font=small_font, fill=(251, 246, 238))
hero.save(ROOT / "docs/images/hero.png", quality=95)
print("wowo web/docs assets")
