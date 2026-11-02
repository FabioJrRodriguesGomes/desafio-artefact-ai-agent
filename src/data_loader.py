
from pathlib import Path
try:
    import pandas as pd
except ImportError as exc:
    raise ImportError(
        "pandas is required to load CSV data. Install it in the active Python environment with: python -m pip install pandas"
    ) from exc

# Identifica a pasta principal do projeto
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Caminho da pasta com os dados
DATA_DIR = PROJECT_DIR / "data"


def localizar_csv(nome):
    """
    Localiza um CSV pelo nome, mesmo que ele tenha
    um prefixo no nome do arquivo.
    """
    arquivos = list(DATA_DIR.glob(f"*{nome}.csv"))

    if not arquivos:
        raise FileNotFoundError(
            f"Arquivo {nome}.csv não encontrado em {DATA_DIR}"
        )

    if len(arquivos) > 1:
        raise ValueError(
            f"Mais de um arquivo encontrado para {nome}: {arquivos}"
        )

    return arquivos[0]


def carregar_dados():
    """
    Carrega os seis arquivos CSV em DataFrames.
    """
    nomes = [
        "categories",
        "customers",
        "order_items",
        "orders",
        "products",
        "promotions"
    ]

    dados = {}

    for nome in nomes:
        caminho = localizar_csv(nome)

        dados[nome] = pd.read_csv(
            caminho,
            encoding="utf-8-sig"
        )

    return dados


def carregar_politicas():
    """
    Lê o manual de políticas da loja.
    """
    caminho = DATA_DIR / "politicas_loja.md"

    if not caminho.exists():
        raise FileNotFoundError(
            "Arquivo politicas_loja.md não encontrado."
        )

    return caminho.read_text(encoding="utf-8")
