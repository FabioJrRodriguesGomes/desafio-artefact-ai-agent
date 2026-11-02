from src.tools import buscar_produto, consultar_estoque, DADOS


def test_buscar_produto():
    resultado = buscar_produto("Yamaha")

    assert isinstance(resultado, list)
    assert len(resultado) > 0

    for produto in resultado:
        assert "name" in produto
        assert "product_id" in produto


def test_consultar_estoque():
    resultado = consultar_estoque("81")

    assert isinstance(resultado, dict)
    assert resultado["produto"] == "Yamaha C40 Nylon Natural"
    assert resultado["estoque"] == 12
    assert resultado["status"] == "active"
    assert resultado["disponivel"] is True

def test_consultar_estoque_produto_inexistente():
    resultado = consultar_estoque("999999")

    assert resultado == "Produto não encontrado."


def test_consultar_estoque_retorna_disponibilidade():
    resultado = consultar_estoque("81")

    assert resultado["disponivel"] is True
    assert resultado["estoque"] > 0

def test_consultar_estoque_zerado():
    produtos = DADOS["products"]

    sem_estoque = produtos[
        produtos["stock_quantity"] == 0
    ]

    assert not sem_estoque.empty

    product_id = sem_estoque.iloc[0]["product_id"]

    resultado = consultar_estoque(product_id)

    assert resultado["estoque"] == 0
    assert resultado["disponivel"] is False