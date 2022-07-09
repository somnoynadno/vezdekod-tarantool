import base64

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from collections import Counter
from random import choice
from io import BytesIO

VK_COLORS = ['#0077ff', '#00eaff', '#811ac7', '#ff3971', '#17d685', '#c2b8ad']


def create_meme(img_b64: str, upper_text: str, lower_text: str) -> str:
    img = Image.open(BytesIO(base64.b64decode(img_b64)))
    w, h = img.size

    upper_font_size = round(w / len(upper_text) * 1.5)
    lower_font_size = round(w / len(lower_text) * 1.5)

    i = ImageDraw.Draw(img)
    upper_font = ImageFont.truetype('../assets/fonts/OpenSans-SemiBold.ttf', upper_font_size)
    lower_font = ImageFont.truetype('../assets/fonts/OpenSans-SemiBold.ttf', lower_font_size)

    i.text((10, upper_font_size // 4), upper_text, font=upper_font,
           fill=(250, 250, 250), stroke_fill=(0, 0, 0), stroke_width=1)
    i.text((10, h - lower_font_size * 2), lower_text, font=lower_font,
           fill=(250, 250, 250), stroke_fill=(0, 0, 0), stroke_width=1)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def get_most_frequent_color(img_b64: str) -> (int, int, int):
    img = Image.open(BytesIO(base64.b64decode(img_b64)))
    w, h = img.size

    c = Counter()
    for y in range(h):
        for x in range(w):
            p = img.getpixel((x, y))
            c[p] += 1

    return c.most_common(1)[0][0]


def replace_color_with_vk_color(img_b64: str, color: (int, int, int)) -> str:
    img = Image.open(BytesIO(base64.b64decode(img_b64)))
    w, h = img.size

    vk_color = choice(VK_COLORS).lstrip('#')  # hex -> rgb
    vk_color = tuple(int(vk_color[i:i+2], 16) for i in (0, 2, 4))

    for y in range(h):
        for x in range(w):
            if img.getpixel((x, y)) == color:
                img.putpixel((x, y), vk_color)

    buffered = BytesIO()
    img.save(buffered, format="PNG")

    return base64.b64encode(buffered.getvalue()).decode("utf-8")
