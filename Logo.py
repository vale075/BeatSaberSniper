import requests
from PIL import Image
from io import BytesIO
from base64 import b64encode

cross = Image.open("CrossHair.png")
print(cross.format, cross.size, cross.mode)

cross = 

avatar = Image.open(BytesIO(requests.get("https://new.scoresaber.com/api/static/avatars/76561198141584046.jpg").content))
avatar.putalpha(254)
print(avatar.format, avatar.size, avatar.mode)

new_img = Image.alpha_composite(avatar, cross)
buffer = BytesIO()
new_img.convert("RGB").save(buffer, format="JPEG")

img_byte = buffer.getvalue()
img_str = "data:image/png;base64," + b64encode(img_byte).decode()
print(img_str)
