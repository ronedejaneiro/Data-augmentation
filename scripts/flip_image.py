from PIL import Image, ImageOps
from pathlib import Path

# Pasta que tem o data set original
pasta_entrada = Path("Imagens_originais")

# salvamento das imagens
pasta_saida = Path("Imagens_flipadas")
pasta_saida.mkdir(parents=True, exist_ok=True)

# Formatos aceitos
extensoes = {".jpg", ".jpeg", ".png"}

# Buscar imagens
imagens = [
    arquivo for arquivo in pasta_entrada.iterdir()
    if arquivo.is_file() and arquivo.suffix.lower() in extensoes
]

# Ordenar pela numeração: 1, 2, 3, 4...
imagens.sort(key=lambda x: int(x.stem))

for arquivo in imagens:
    with Image.open(arquivo) as imagem:
        # Flip horizontal
        imagem_flipada = ImageOps.mirror(imagem)
        caminho_saida = pasta_saida / arquivo.name
        imagem_flipada.save(caminho_saida)

        print(f"Salva: {caminho_saida}")

print("Todas as imagens foram flipadas!")
