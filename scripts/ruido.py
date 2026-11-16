"""Adiciona ruído gaussiano leve e moderado às imagens originais."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "Imagens_originais"
SAIDA = RAIZ / "Imagens_ruido"
EXTENSOES = {".jpg", ".jpeg", ".png"}
# Intensidade do ruído em escala de pixels [0, 255].
AJUSTES = {"leve_08": 8, "moderado_18": 18}
SEMENTE = 42  # Permite reproduzir o mesmo resultado em novas execuções.


def main():
    if not ENTRADA.is_dir():
        raise SystemExit(f"Pasta não encontrada: {ENTRADA}")
    SAIDA.mkdir(parents=True, exist_ok=True)
    arquivos = sorted(
        (p for p in ENTRADA.iterdir() if p.is_file() and p.suffix.lower() in EXTENSOES),
        key=lambda p: (0, int(p.stem)) if p.stem.isdigit() else (1, p.name.lower()),
    )
    gerador = np.random.default_rng(SEMENTE)
    total = 0
    for arquivo in arquivos:
        try:
            with Image.open(arquivo) as original:
                imagem = ImageOps.exif_transpose(original).convert("RGB")
                pixels = np.asarray(imagem, dtype=np.float32)
                for nome, desvio_padrao in AJUSTES.items():
                    ruido = gerador.normal(0, desvio_padrao, pixels.shape)
                    alterados = np.clip(pixels + ruido, 0, 255).astype(np.uint8)
                    resultado = Image.fromarray(alterados, mode="RGB")
                    destino = SAIDA / f"{arquivo.stem}_ruido_{nome}{arquivo.suffix.lower()}"
                    resultado.save(destino, quality=95) if destino.suffix in {".jpg", ".jpeg"} else resultado.save(destino)
                    total += 1
        except (OSError, ValueError) as erro:
            print(f"Não foi possível processar {arquivo.name}: {erro}")
    print(f"Concluído: {total} imagens geradas em {SAIDA}")


if __name__ == "__main__":
    main()
