from PIL import Image
from pathlib import Path
import subprocess

uploads = Path("/home/ubuntu/.cursor/projects/workspace/uploads")
out = Path(__file__).resolve().parent.parent / "assets"
out.mkdir(parents=True, exist_ok=True)


def save_pair(src_path, base_name, sizes):
    im = Image.open(src_path)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
    for w, suffix in sizes:
        ratio = w / im.width
        h = int(im.height * ratio)
        resized = im.resize((w, h), Image.Resampling.LANCZOS)
        png_path = out / f"{base_name}{suffix}.png"
        resized.save(png_path, optimize=True)
        webp_path = out / f"{base_name}{suffix}.webp"
        subprocess.run(["cwebp", "-q", "82", str(png_path), "-o", str(webp_path)], check=True)


icon = Image.open(uploads / "regime-icon-1024_d4c4.png")
for size, name in [(512, "icon-512"), (192, "icon-192"), (180, "apple-touch-icon"), (32, "favicon-32")]:
    r = icon.resize((size, size), Image.Resampling.LANCZOS)
    p = out / f"{name}.png"
    r.save(p, optimize=True)
    subprocess.run(["cwebp", "-q", "90", str(p), "-o", str(out / f"{name}.webp")], check=True)

s1 = Image.open(uploads / "screenshot-01-chain_2daa.png")
target_w, target_h = 1200, 630
w, h = s1.size
scale = max(target_w / w, target_h / h)
nw, nh = int(w * scale), int(h * scale)
s1s = s1.resize((nw, nh), Image.Resampling.LANCZOS)
left = (nw - target_w) // 2
top = int(nh * 0.08)
og = s1s.crop((left, top, left + target_w, top + target_h))
if og.mode == "RGBA":
    og = og.convert("RGB")
og.save(out / "og-image.png", optimize=True)
subprocess.run(["cwebp", "-q", "82", str(out / "og-image.png"), "-o", str(out / "og-image.webp")], check=True)

shots = [
    ("screenshot-01-chain_2daa.png", "screenshot-01-chain"),
    ("screenshot-02-progress_952f.png", "screenshot-02-progress"),
    ("screenshot-04-day-complete_d21c.png", "screenshot-04-day-complete"),
]
for fname, base in shots:
    save_pair(uploads / fname, base, [(390, ""), (780, "@2x")])

print("ok", len(list(out.iterdir())), "files")
