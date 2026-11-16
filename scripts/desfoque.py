"""Gera duas versões com desfoque gaussiano de cada imagem original."""
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "Imagens_originais"
SAIDA = RAIZ / "Imagens_desfoque"
EXTENSOES = {".jpg", ".jpeg", ".png"}
# Raio em pixels; valores maiores deixam a imagem mais desfocada.
AJUSTES = {"leve_1": 1.0, "moderado_2": 2.0}


def main():
    if not ENTRADA.is_dir():
        raise SystemExit(f"Pasta não encontrada: {ENTRADA}")
    SAIDA.mkdir(parents=True, exist_ok=True)
    arquivos = sorted(
        (p for p in ENTRADA.iterdir() if p.is_file() and p.suffix.lower() in EXTENSOES),
        key=lambda p: (0, int(p.stem)) if p.stem.isdigit() else (1, p.name.lower()),
    )
    total = 0
    for arquivo in arquivos:
        try:
            with Image.open(arquivo) as original:
                imagem = ImageOps.exif_transpose(original).convert("RGB")
                for nome, raio in AJUSTES.items():
                    resultado = imagem.filter(ImageFilter.GaussianBlur(radius=raio))
                    destino = SAIDA / f"{arquivo.stem}_desfoque_{nome}{arquivo.suffix.lower()}"
                    resultado.save(destino, quality=95) if destino.suffix in {".jpg", ".jpeg"} else resultado.save(destino)
                    total += 1
        except (OSError, ValueError) as erro:
            print(f"Não foi possível processar {arquivo.name}: {erro}")
    print(f"Concluído: {total} imagens geradas em {SAIDA}")


if __name__ == "__main__":
    main()
