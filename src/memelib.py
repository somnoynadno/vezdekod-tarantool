import base64

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from io import BytesIO


def create_meme(img_b64: str, upper_text: str, lower_text: str) -> str:
    img = Image.open(BytesIO(base64.b64decode(img_b64)))
    w, h = img.size

    upper_font_size = round(w / len(upper_text) * 1.5)
    lower_font_size = round(w / len(lower_text) * 1.5)

    i = ImageDraw.Draw(img)
    upper_font = ImageFont.truetype('../assets/fonts/OpenSans-SemiBold.ttf', upper_font_size)
    lower_font = ImageFont.truetype('../assets/fonts/OpenSans-SemiBold.ttf', lower_font_size)

    i.text((10, upper_font_size // 4), upper_text, font=upper_font,
           fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=1)
    i.text((10, h - lower_font_size * 2), lower_text, font=lower_font,
           fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=1)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
