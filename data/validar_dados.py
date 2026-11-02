
import csv
from pathlib import Path

pasta = Path(__file__).parent

def carregar(nome):
    arquivos = list(pasta.glob(f"*{nome}.csv"))

    if not arquivos:
        raise FileNotFoundError(f"Arquivo não encontrado: {nome}")

    with open(arquivos[0], encoding="utf-8-sig", newline="") as f:
        amostra = f.read(4096)
        f.seek(0)

        try:
            sep = csv.Sniffer().sniff(
                amostra, delimiters=",;|\t"
            ).delimiter
        except csv.Error:
            sep = ","

        return list(csv.DictReader(f, delimiter=sep))

# Carregar tabelas
categories = carregar("categories")
customers = carregar("customers")
products = carregar("products")
orders = carregar("orders")
promotions = carregar("promotions")

# Aceita os dois nomes possíveis
try:
    order_items = carregar("order_items")
except FileNotFoundError:
    order_items = carregar("order_itens")

def verificar(nome, origem, campo_origem, destino, campo_destino):
    ids = {linha[campo_destino] for linha in destino}

    invalidos = [
        linha[campo_origem]
        for linha in origem
        if linha[campo_origem] not in ids
    ]

    print(f"\nRelacionamento: {nome}")
    print("Referências inválidas:", invalidos if invalidos else "Nenhuma")

print("=== VALIDAÇÃO DOS RELACIONAMENTOS ===")

verificar(
    "Produtos -> Categorias",
    products, "category_id",
    categories, "category_id"
)

verificar(
    "Pedidos -> Clientes",
    orders, "customer_id",
    customers, "customer_id"
)

verificar(
    "Itens -> Pedidos",
    order_items, "order_id",
    orders, "order_id"
)

verificar(
    "Itens -> Produtos",
    order_items, "product_id",
    products, "product_id"
)

verificar(
    "Promoções -> Produtos",
    promotions, "product_id",
    products, "product_id"
)

print("\n=== VALIDAÇÃO FINALIZADA ===")
