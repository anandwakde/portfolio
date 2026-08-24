from PIL import Image, ImageDraw, ImageFont

INK = (22, 26, 29, 255)
PAPER = (233, 237, 236, 255)
PAPER_DEEP = (19, 26, 29, 255)
LINE = (185, 196, 195, 255)
STAMP = (189, 58, 30, 255)

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

SCALE = 8  # render big, downsample for crisp anti-aliased edges


def mark(size):
    """Circular monogram mark: dark disc, thin stamp-red ring, 'AW' in paper."""
    s = size * SCALE
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.ellipse([0, 0, s - 1, s - 1], fill=INK)

    ring_inset = int(s * 0.09)
    ring_width = max(int(s * 0.018), 2)
    d.ellipse(
        [ring_inset, ring_inset, s - 1 - ring_inset, s - 1 - ring_inset],
        outline=STAMP,
        width=ring_width,
    )

    font = ImageFont.truetype(FONT_BOLD, int(s * 0.40))
    text = "AW"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(
        (s / 2 - tw / 2 - bbox[0], s / 2 - th / 2 - bbox[1]),
        text,
        font=font,
        fill=PAPER,
    )

    return img.resize((size, size), Image.LANCZOS)


def save_ico(path, base_size=256):
    img = mark(base_size)
    img.save(path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])


def wrap_text(d, text, font, max_width):
    words = text.split(" ")
    lines, line = [], ""
    for w in words:
        trial = (line + " " + w).strip()
        if d.textbbox((0, 0), trial, font=font)[2] <= max_width or not line:
            line = trial
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def og_image(path):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    grid = LINE
    d.line([(0, 0), (W, 0)], fill=grid, width=2)
    d.line([(0, H - 1), (W, H - 1)], fill=grid, width=2)
    d.line([(0, 0), (0, H)], fill=grid, width=2)
    d.line([(W - 1, 0), (W - 1, H)], fill=grid, width=2)

    pad = 80
    text_max_width = 740  # keeps every line clear of the mark in the corner

    m = mark(150)
    img.paste(m, (W - pad - 150, pad - 10), m)

    eyebrow_font = ImageFont.truetype(FONT_BOLD, 24)
    d.text((pad, 78), "BUILD LOG", font=eyebrow_font, fill=(90, 100, 98))

    name_font = ImageFont.truetype(FONT_BLACK, 88)
    d.text((pad, 128), "Anand Wakde", font=name_font, fill=INK)

    role_font = ImageFont.truetype(FONT_BOLD, 28)
    role_lines = wrap_text(
        d,
        "Senior Product Owner — Payments Modernization & Compliance",
        role_font,
        text_max_width,
    )
    y = 258
    for line in role_lines:
        d.text((pad, y), line, font=role_font, fill=(70, 78, 76))
        y += 40

    tag_font = ImageFont.truetype(FONT_BOLD, 24)
    d.text(
        (pad, y + 20),
        "A manifest of shipped products and projects.",
        font=tag_font,
        fill=(70, 78, 76),
    )

    img.save(path, format="PNG")


assets = "/Users/anand/portfolio/assets"

mark(512).save(f"{assets}/favicon-512.png")
mark(180).save(f"{assets}/apple-touch-icon.png")
mark(32).save(f"{assets}/favicon-32.png")
mark(16).save(f"{assets}/favicon-16.png")
save_ico(f"{assets}/favicon.ico")
og_image(f"{assets}/og-image.png")

print("done")
