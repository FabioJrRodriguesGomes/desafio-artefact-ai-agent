from src.tools import consultar_pedido, DADOS


def obter_email_do_pedido(order_id):
    pedido = DADOS["orders"].loc[
        DADOS["orders"]["order_id"].astype(str) == str(order_id)
    ].iloc[0]

    cliente = DADOS["customers"].loc[
        DADOS["customers"]["customer_id"].astype(str)
        == str(pedido["customer_id"])
    ].iloc[0]

    return cliente["email"]


def test_consultar_pedido_com_email_correto():
    email = obter_email_do_pedido("1")

    resultado = consultar_pedido("1", email)

    assert isinstance(resultado, dict)
    assert resultado["status"] == "delivered"


def test_consultar_pedido_com_email_incorreto():
    resultado = consultar_pedido(
        "1",
        "emailincorreto@teste.com"
    )

    assert resultado == "Não foi possível confirmar a identidade do cliente."

def test_consultar_pedido_inexistente():
    resultado = consultar_pedido(
        "999999",
        "cliente@teste.com"
    )

    assert resultado == "Pedido não encontrado."


def test_consultar_pedido_email_com_maiusculas_e_espacos():
    email = obter_email_do_pedido("1")

    email_formatado = f"  {email.upper()}  "

    resultado = consultar_pedido("1", email_formatado)

    assert isinstance(resultado, dict)
    assert resultado["status"] == "delivered"