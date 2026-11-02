import pytest
import pandas as pd

from src import tools
from src.tools import consultar_preco

def test_consultar_preco():
    resultado = consultar_preco("81")

    assert isinstance(resultado, dict)
    assert resultado["produto"] == "Yamaha C40 Nylon Natural"
    assert resultado["preco_original"] == pytest.approx(599.90)
    assert resultado["promocoes_ativas"] == []

def test_consultar_preco_com_promocao_ativa():
    resultado = consultar_preco("121")

    assert resultado["produto"] == "Ohana CK-20 Concert Natural"
    assert resultado["preco_original"] == pytest.approx(549.00)
    assert len(resultado["promocoes_ativas"]) == 1
    assert resultado["promocoes_ativas"][0]["desconto_percentual"] == pytest.approx(20.0)
    assert resultado["promocoes_ativas"][0]["descricao"] == "Desconto Exclusivo"
    assert resultado["preco_promocional"] == pytest.approx(439.20)
    assert resultado["economia"] == pytest.approx(109.80)

def test_consultar_preco_produto_inexistente():
    resultado = consultar_preco("999999")

    assert resultado == "Produto não encontrado."

@pytest.mark.parametrize("desconto", [150, -10])
def test_consultar_preco_ignora_descontos_invalidos(monkeypatch, desconto):
    promocoes_falsas = pd.DataFrame([
        {
            "product_id": "121",
            "discount_percent": desconto,
            "description": "Promoção inválida",
            "is_active": "1"
        }
    ])

    monkeypatch.setitem(
        tools.DADOS,
        "promotions",
        promocoes_falsas
    )

    resultado = consultar_preco("121")

    assert resultado["preco_original"] == pytest.approx(549.00)
    assert resultado["preco_promocional"] == pytest.approx(549.00)
    assert resultado["economia"] == 0.0
    assert resultado["promocoes_ativas"] == []