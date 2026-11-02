from src.agent import tratar_erro_api

def test_erro_429():
    resultado = tratar_erro_api(
        Exception("429 RESOURCE_EXHAUSTED")
    )

    assert "Limite" in resultado


def test_erro_503():
    resultado = tratar_erro_api(
        Exception("503 UNAVAILABLE")
    )

    assert "indisponível" in resultado


def test_erro_generico():
    resultado = tratar_erro_api(
        Exception("Erro desconhecido")
    )

    assert "Erro desconhecido" in resultado