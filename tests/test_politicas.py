from src.tools import buscar_politica

def test_buscar_politica_parcelamento():
    resultado = buscar_politica("parcelamento")

    assert isinstance(resultado, str)
    assert len(resultado) > 0
    assert "parcelamento" in resultado.lower()


def test_buscar_politica_assunto_inexistente():
    resultado = buscar_politica("assunto_que_nao_existe")

    assert resultado == "Não encontrei informações sobre esse assunto no manual."

def test_buscar_politica_garantia():
    resultado = buscar_politica("garantia")

    assert isinstance(resultado, str)
    assert len(resultado) > 0
    assert "90" in resultado
    assert "noventa" in resultado.lower()

def test_buscar_politica_frete():
    resultado = buscar_politica("frete")

    assert isinstance(resultado, str)
    assert len(resultado) > 0
    assert "R$ 35,00" in resultado
    assert "R$ 500,00" in resultado

def test_buscar_politica_sinonimo_quebrado():
    resultado = buscar_politica("quebrado")

    assert "4. Política de Trocas e Devoluções" in resultado
    assert "5. Política de Frete e Entregas" in resultado
    assert "8. Garantia" in resultado


def test_buscar_politica_sinonimo_parcelar():
    resultado = buscar_politica("parcelar")

    assert "3. Formas de Pagamento" in resultado
    assert "3.1 Regras de Parcelamento" in resultado

def test_buscar_politica_frase_completa():
    resultado = buscar_politica("Minha guitarra chegou quebrada")

    assert "4. Política de Trocas e Devoluções" in resultado
    assert "5. Política de Frete e Entregas" in resultado
    assert "8. Garantia" in resultado