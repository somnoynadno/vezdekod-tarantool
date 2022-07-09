from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

img = Image.open('../assets/img/example.png')
w, h = img.size

upper_text = "Прибыл мем"
lower_text = "Было очень весело его делать..."

upper_font_size = round(w / len(upper_text) * 1.5)
lower_font_size = round(w / len(lower_text) * 1.5)

I1 = ImageDraw.Draw(img)
upper_font = ImageFont.truetype('../assets/fonts/OpenSans-SemiBold.ttf', upper_font_size)
lower_font = ImageFont.truetype('../assets/fonts/OpenSans-SemiBold.ttf', lower_font_size)

I1.text((10, upper_font_size // 4), upper_text, font=upper_font, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=1)
I1.text((10, h - lower_font_size * 2), lower_text, font=lower_font, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=1)

img.save("../assets/img/meme.png")
