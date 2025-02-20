from PIL import Image
import json
import os
import sys

# Caminho da imagem
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root)

IMAGE_PATH = os.path.join(root, "assets", "fonts", "title-font.png")
OUTPUT_JSON = "font_positions.json"

image = Image.open(IMAGE_PATH).convert("RGB")

# Definições corrigidas da varredura
START_X, START_Y = 0, 1  # Ponto inicial
END_X, END_Y = 160, 81  # 10 colunas * 16px, 5 linhas * 16px
LETTER_WIDTH, LETTER_HEIGHT = 16, 16  # Agora corrigido para 16x16
TRANSPARENT_COLOR = image.getpixel((0, 0))  # Pega a cor do primeiro pixel
COLOR_TOLERANCE = 30  # Tolerância de cor para evitar ruídos
MIN_PIXEL_COUNT = 5  # Mínimo de pixels diferentes do fundo para ser considerado uma letra

NUM_COLUMNS = (END_X - START_X) // LETTER_WIDTH
NUM_LINES = (END_Y - START_Y) // LETTER_HEIGHT

print(f"🔍 Varrendo imagem de {NUM_COLUMNS} colunas e {NUM_LINES} linhas...")

positions = []
index = 0

def is_transparent(color, ref_color, tolerance=5):
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color, ref_color))

# Percorrer a imagem em blocos de 16x16 pixels
for y in range(START_Y, END_Y, LETTER_HEIGHT):
    for x in range(START_X, END_X, LETTER_WIDTH):
        pixel_count = 0

        # Contar quantos pixels são diferentes da cor transparente
        for i in range(LETTER_WIDTH):
            for j in range(LETTER_HEIGHT):
                if x + i < image.width and y + j < image.height:
                    color = image.getpixel((x + i, y + j))
                    
                    if not is_transparent(color, TRANSPARENT_COLOR):
                        pixel_count += 1
                        if pixel_count >= MIN_PIXEL_COUNT:
                            break
            if pixel_count >= MIN_PIXEL_COUNT:
                break

        # Se encontrou uma letra válida, adiciona ao JSON
        if pixel_count >= MIN_PIXEL_COUNT:
            positions.append({
                "name": f"letter_{index}",
                "x": x,
                "y": y,
                "width": LETTER_WIDTH,
                "height": LETTER_HEIGHT
            })
            index += 1
            print(f"✅ Letra detectada em ({x}, {y})")  # Debug para validar coordenadas

# Salvar como JSON
with open(OUTPUT_JSON, "w") as f:
    json.dump(positions, f, indent=4)

print(f"✅ JSON gerado com {len(positions)} letras detectadas!")