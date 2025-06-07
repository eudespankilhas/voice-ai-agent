from PIL import Image, ImageDraw, ImageFont
import os

# Criar pasta para ícones se não existir
os.makedirs('static/icons', exist_ok=True)

# Criar ícone 192x192
icon_192 = Image.new('RGBA', (192, 192), (255, 255, 255, 0))
draw = ImageDraw.Draw(icon_192)

# Desenhar um microfone simples
# Círculo externo
draw.ellipse((20, 20, 172, 172), outline=(76, 175, 80), width=4)
# Círculo interno
draw.ellipse((60, 60, 132, 132), fill=(76, 175, 80))
# Barras do microfone
for i in range(5):
    angle = i * (360/5)
    x1 = 96 + 30 * (1 + 0.5 * i) * 0.5
    y1 = 96 - 30 * (1 + 0.5 * i) * 0.5
    x2 = 96 + 30 * (1 + 0.5 * i) * 0.866
    y2 = 96 - 30 * (1 + 0.5 * i) * 0.5
    draw.line((x1, y1, x2, y2), fill=(255, 255, 255), width=2)

icon_192.save('static/icons/icon-192x192.png')

# Criar ícone 512x512 (baseado no 192x192)
icon_512 = Image.new('RGBA', (512, 512), (255, 255, 255, 0))
draw = ImageDraw.Draw(icon_512)

# Desenhar um microfone simples
# Círculo externo
draw.ellipse((40, 40, 472, 472), outline=(76, 175, 80), width=8)
# Círculo interno
draw.ellipse((120, 120, 392, 392), fill=(76, 175, 80))
# Barras do microfone
for i in range(5):
    angle = i * (360/5)
    x1 = 256 + 60 * (1 + 0.5 * i) * 0.5
    y1 = 256 - 60 * (1 + 0.5 * i) * 0.5
    x2 = 256 + 60 * (1 + 0.5 * i) * 0.866
    y2 = 256 - 60 * (1 + 0.5 * i) * 0.5
    draw.line((x1, y1, x2, y2), fill=(255, 255, 255), width=4)

icon_512.save('static/icons/icon-512x512.png')
