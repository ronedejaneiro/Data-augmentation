"""Gera duas versões de contraste de cada imagem original."""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "Imagens_originais"
SAIDA = RAIZ / "Imagens_contraste"
EXTENSOES = {".jpg", ".jpeg", ".png"}
# Fator 1.0 = original; menor reduz; maior aumenta o contraste.
AJUSTES = {"baixo_080": 0.80, "alto_120": 1.20}


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
                for nome, fator in AJUSTES.items():
                    resultado = ImageEnhance.Contrast(imagem).enhance(fator)
                    destino = SAIDA / f"{arquivo.stem}_contraste_{nome}{arquivo.suffix.lower()}"
                    resultado.save(destino, quality=95) if destino.suffix in {".jpg", ".jpeg"} else resultado.save(destino)
                    total += 1
        except (OSError, ValueError) as erro:
            print(f"Não foi possível processar {arquivo.name}: {erro}")
    print(f"Concluído: {total} imagens geradas em {SAIDA}")


if __name__ == "__main__":
    main()
