
from src.tools import (
    DADOS,
    buscar_produto,
    consultar_estoque,
    consultar_preco,
    consultar_pedido,
    buscar_politica,
)

print("===== TESTE 1: BUSCAR PRODUTO =====")
print(buscar_produto("Yamaha"))

print("\n===== TESTE 2: CONSULTAR ESTOQUE =====")
print(consultar_estoque("81"))

print("\n===== TESTE 3: CONSULTAR PREÇO =====")
print(consultar_preco("81"))

print("\n===== TESTE 4: CONSULTAR PEDIDO =====")

pedido = DADOS["orders"][
    DADOS["orders"]["order_id"].astype(str) == "1"
].iloc[0]

cliente = DADOS["customers"][
    DADOS["customers"]["customer_id"].astype(str)
    == str(pedido["customer_id"])
].iloc[0]

email_teste = cliente["email"]

print(consultar_pedido("1", email_teste))

print("\n===== TESTE 5: BUSCAR POLÍTICA =====")
print(buscar_politica("parcelamento"))

print("\n===== TESTE 6: VERIFICAÇÃO DE IDENTIDADE =====")
print(consultar_pedido("1", "emailincorreto@teste.com"))