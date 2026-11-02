import pandas as pd
import re

from src.data_loader import carregar_dados, carregar_politicas


# Carrega os dados uma vez quando o módulo é iniciado
DADOS = carregar_dados()
POLITICAS = carregar_politicas()


def buscar_produto(termo):
    """
    Busca produtos pelo nome ou descrição.
    """
    produtos = DADOS["products"]

    encontrados = produtos[
        produtos["name"].str.contains(
            termo, case=False, na=False, regex=False
        )
        |
        produtos["description"].str.contains(
            termo, case=False, na=False, regex=False
        )
    ]

    if encontrados.empty:
        return "Nenhum produto encontrado."

    colunas = [
        "product_id",
        "name",
        "price_brl",
        "stock_quantity",
        "status"
    ]

    return encontrados[colunas].to_dict(orient="records")


def consultar_estoque(product_id):
    """
    Consulta o estoque e a disponibilidade de um produto.
    """
    produtos = DADOS["products"]

    produto = produtos[
        produtos["product_id"].astype(str) == str(product_id)
    ]

    if produto.empty:
        return "Produto não encontrado."

    produto = produto.iloc[0]

    estoque = int(produto["stock_quantity"])
    status = str(produto["status"]).lower()

    disponivel = estoque > 0 and status == "active"

    return {
        "produto": produto["name"],
        "estoque": estoque,
        "status": status,
        "disponivel": disponivel
    }


def consultar_preco(product_id):
    """
    Consulta o preço e as promoções ativas de um produto.
    """
    produtos = DADOS["products"]
    promocoes = DADOS["promotions"]

    produto = produtos[
        produtos["product_id"].astype(str) == str(product_id)
    ]

    if produto.empty:
        return "Produto não encontrado."

    produto = produto.iloc[0]
    preco_original = float(produto["price_brl"])

    promocoes_produto = promocoes[
        (promocoes["product_id"].astype(str) == str(product_id))
        &
        (promocoes["is_active"].astype(str).str.lower().isin(
            ["1", "true", "sim", "yes"]
        ))
    ]

    resultado = {
        "produto": produto["name"],
        "preco_original": preco_original,
        "preco_promocional": preco_original,
        "economia": 0.0,
        "promocoes_ativas": []
    }

    maior_desconto = 0.0

    for _, promocao in promocoes_produto.iterrows():
        desconto = float(promocao["discount_percent"])
    
        # Ignora descontos fora do intervalo permitido.
        if desconto <= 0 or desconto > 100:
            continue
    
        resultado["promocoes_ativas"].append({
            "desconto_percentual": desconto,
            "descricao": promocao["description"]
        })
    
        if desconto > maior_desconto:
            maior_desconto = desconto
    
    if maior_desconto > 0:
        economia = preco_original * (maior_desconto / 100)
    
        resultado["economia"] = round(economia, 2)
        resultado["preco_promocional"] = round(
            preco_original - economia, 2
        )

    return resultado



def consultar_pedido(order_id, email_cliente):
    """
    Consulta um pedido somente após verificar
    o e-mail do cliente associado a ele.
    """
    pedidos = DADOS["orders"]
    clientes = DADOS["customers"]
    itens = DADOS["order_items"]
    produtos = DADOS["products"]

    pedido = pedidos[
        pedidos["order_id"].astype(str) == str(order_id)
    ]

    if pedido.empty:
        return "Pedido não encontrado."

    pedido = pedido.iloc[0]

    cliente = clientes[
        clientes["customer_id"].astype(str)
        == str(pedido["customer_id"])
    ]

    if cliente.empty:
        return "Não foi possível verificar os dados do cliente."

    email_cadastrado = str(
        cliente.iloc[0]["email"]
    ).strip().lower()

    email_informado = str(
        email_cliente
    ).strip().lower()

    if email_cadastrado != email_informado:
        return "Não foi possível confirmar a identidade do cliente."

    itens_pedido = itens[
        itens["order_id"].astype(str) == str(order_id)
    ]

    detalhes_itens = []

    for _, item in itens_pedido.iterrows():
        produto = produtos[
            produtos["product_id"].astype(str)
            == str(item["product_id"])
        ]

        if not produto.empty:
            detalhes_itens.append({
                "produto": produto.iloc[0]["name"],
                "quantidade": int(item["quantity"])
            })

    return {
        "pedido": str(pedido["order_id"]),
        "status": pedido["status"],
        "data": str(pedido["order_date"]),
        "valor_total": float(pedido["total_brl"]),
        "forma_pagamento": pedido["payment_method"],
        "codigo_rastreamento": pedido["tracking_code"],
        "previsao_entrega": pedido["estimated_delivery"],
        "itens": detalhes_itens
    }

SINONIMOS_POLITICAS = {
    "quebrado": ["avaria", "danos", "defeito"],
    "quebrada": ["avaria", "danos", "defeito"],
    "quebrou": ["avaria", "danos", "defeito"],
    "danificado": ["avaria", "danos", "defeito"],
    "danificada": ["avaria", "danos", "defeito"],

    "devolver": ["devolução", "arrependimento", "troca"],
    "devolvido": ["devolução", "arrependimento", "troca"],
    "trocar": ["troca", "defeito"],

    "parcelar": ["parcelamento", "cartão de crédito"],
    "parcelas": ["parcelamento", "cartão de crédito"],

    "entrega": ["frete", "prazo de entrega", "rastreamento"],
    "entregue": ["frete", "prazo de entrega", "rastreamento"],

    "rastrear": ["rastreamento", "código de rastreamento"],
    "rastreio": ["rastreamento", "código de rastreamento"],
}

def buscar_politica(termo):
    """
    Busca informações no manual, priorizando títulos das seções
    e expandindo a consulta com termos relacionados.
    """

    termo = termo.strip().lower()

    if not termo:
        return "Informe um assunto para consultar o manual."

    # Identifica os títulos das 10 seções principais.
    padrao = re.compile(
        r"(?m)^(?:[1-9]|10)\.\s+(?!\d)"
        r"(?!Saudação:|Entendimento:|Consulta:|Resposta:|Fechamento:).+"
    )

    titulos = list(padrao.finditer(POLITICAS))

    secoes = []

    for i, titulo in enumerate(titulos):
        inicio = titulo.start()

        if i + 1 < len(titulos):
            fim = titulos[i + 1].start()
        else:
            fim = len(POLITICAS)

        conteudo = POLITICAS[inicio:fim].strip()

        secoes.append({
            "titulo": titulo.group().strip(),
            "conteudo": conteudo
        })

    # Expande a consulta identificando palavras dentro de frases.
    termos_busca = [termo]

    palavras = re.findall(r"\w+", termo)

    for palavra in palavras:
        if palavra in SINONIMOS_POLITICAS:
            termos_busca.append(palavra)
            termos_busca.extend(SINONIMOS_POLITICAS[palavra])

    # Remove termos repetidos.
    termos_busca = list(dict.fromkeys(termos_busca))
    
    # Primeiro, procura nos títulos.
    resultados = [
        secao["conteudo"]
        for secao in secoes
        if any(
            palavra in secao["titulo"].lower()
            for palavra in termos_busca
        )
    ]

    # Se não encontrar nos títulos, procura no conteúdo.
    if not resultados:
        resultados = [
            secao["conteudo"]
            for secao in secoes
            if any(
                palavra in secao["conteudo"].lower()
                for palavra in termos_busca
            )
        ]

    if not resultados:
        return "Não encontrei informações sobre esse assunto no manual."

    return "\n\n".join(resultados)