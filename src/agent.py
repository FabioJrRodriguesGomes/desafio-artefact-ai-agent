
import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from numpy import rint

from src.tools import (
    buscar_produto as consultar_produtos,
    consultar_estoque as consultar_estoque_python,
    consultar_preco as consultar_preco_python,
    consultar_pedido as consultar_pedido_python,
    buscar_politica as consultar_politica_python
)


# ==========================================
# 1. CONFIGURAÇÃO DA API
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chave GEMINI_API_KEY não encontrada.")

client = genai.Client(api_key=api_key)


# ==========================================
# 2. FERRAMENTAS DISPONIBILIZADAS AO GEMINI
# ==========================================

def buscar_produto(termo: str) -> str:
    """Busca produtos no catálogo pelo nome ou descrição.

    Args:
        termo: Nome, marca ou descrição do instrumento.
    """
    resultado = consultar_produtos(termo)
    return json.dumps(resultado, ensure_ascii=False, default=str)


def consultar_estoque(product_id: str) -> str:
    """Consulta a quantidade disponível e o status de um produto.

    Args:
        product_id: Identificador do produto no catálogo.
    """
    resultado = consultar_estoque_python(product_id)
    return json.dumps(resultado, ensure_ascii=False, default=str)


def consultar_preco(product_id: str) -> str:
    """Consulta o preço e as promoções ativas de um produto.

    Args:
        product_id: Identificador do produto no catálogo.
    """
    resultado = consultar_preco_python(product_id)
    return json.dumps(resultado, ensure_ascii=False, default=str)


def consultar_pedido(order_id: str, email_cliente: str) -> str:
    """Consulta um pedido após verificar o e-mail do cliente.

    Args:
        order_id: Identificador do pedido.
        email_cliente: E-mail informado pelo cliente para verificação.
    """
    resultado = consultar_pedido_python(order_id, email_cliente)
    return json.dumps(resultado, ensure_ascii=False, default=str)


def buscar_politica(termo: str) -> str:
    """Busca informações no manual de políticas da loja.

    Args:
        termo: Assunto ou palavra-chave para pesquisar no manual.
    """
    return consultar_politica_python(termo)


# ==========================================
# 3. INSTRUÇÕES DO AGENTE
# ==========================================

INSTRUCOES = """
Você é o assistente virtual do Empório da Música.

Sua função é atender clientes de maneira acolhedora,
profissional e informal, como alguém que entende de música.

REGRAS GERAIS:

1. Responda sempre em português brasileiro.
2. Seja claro, educado e objetivo.
3. Não invente preços, estoques, promoções ou prazos.
4. Utilize as ferramentas Python para consultar informações comerciais.
5. A base de dados é estática e representa os dados fornecidos
   para este protótipo. Não afirme que são informações em tempo real.
6. A loja comercializa instrumentos musicais, não acessórios.
   Não ofereça acessórios que a loja não vende.

PRODUTOS:

- Utilize buscar_produto para localizar instrumentos.
- Utilize consultar_estoque para verificar disponibilidade.
- Utilize consultar_preco para verificar preços e promoções.
- Para responder sobre um produto, consulte os dados necessários.
- Considere o produto disponível somente se o status for active
  e a quantidade em estoque for maior que zero.
- Se não encontrar o produto, informe isso sem inventar alternativas.

PREÇOS E PROMOÇÕES:

- Sempre utilize consultar_preco antes de informar o preço de um produto.
- O campo preco_original representa o preço normal de tabela.
- O campo preco_promocional representa o preço final após
  a aplicação da promoção ativa.
- O campo economia representa o valor economizado pelo cliente.
- Se houver promoção ativa, informe o preço original,
  o percentual de desconto e o preço promocional.
- Se não houver promoção ativa, informe apenas o preço original.
- Nunca calcule ou altere os valores retornados pela ferramenta.
- As promoções não são cumulativas.
- O desconto de 5% no PIX não se aplica a produtos que
  já estejam com preço promocional.
- Se o cliente perguntar sobre formas de pagamento ou
  parcelamento, consulte buscar_politica antes de responder.

PEDIDOS:

- Antes de consultar um pedido, solicite o número do pedido
  e o e-mail cadastrado.
- Só utilize consultar_pedido quando possuir as duas informações.
- Nunca invente um e-mail ou tente adivinhar os dados do cliente.
- Nunca revele o e-mail cadastrado.
- Se a verificação falhar, informe educadamente que não foi
  possível confirmar a identidade.

POLÍTICAS:

- Utilize buscar_politica para consultar o manual.
- Não invente regras que não estejam no manual.
- Se não encontrar uma informação, informe que precisa
  confirmar com a equipe responsável.

IMPORTANTE:
Você deve utilizar as ferramentas disponíveis sempre que
a pergunta depender dos dados comerciais ou das políticas.
Nunca finja ter consultado uma ferramenta.
"""


# ==========================================
# 4. CRIAÇÃO DA SESSÃO DE CONVERSA
# ==========================================

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction=INSTRUCOES,
        tools=[
            buscar_produto,
            consultar_estoque,
            consultar_preco,
            consultar_pedido,
            buscar_politica
        ],
        thinking_config=types.ThinkingConfig(
            thinking_level="low"
        )
    )
)


# ==========================================
# 5. INTERFACE NO TERMINAL
# ==========================================

def iniciar_agente():
    print("=" * 55)
    print("EMPÓRIO DA MÚSICA - ASSISTENTE VIRTUAL")
    print("Digite 'sair' para encerrar.")
    print("=" * 55)

    while True:
        mensagem = input("\nVocê: ").strip()

        if mensagem.lower() in ["sair", "exit", "quit"]:
            print("\nAtendimento encerrado.")
            break

        if not mensagem:
            continue

        try:
            inicio = time.perf_counter()
            resposta = chat.send_message(mensagem)
            duracao = time.perf_counter() - inicio
            print("\nAssistente:", resposta.text)
            print(f"\nTempo de resposta: {duracao:.2f} segundos")
            uso = resposta.usage_metadata
            if uso:
                print(f"Tokens utilizados: {uso.total_token_count}")
                print(f"Tokens de entrada: {uso.prompt_token_count}")
                print(f"Tokens de saída: {uso.candidates_token_count}")
           
        except Exception as erro:
            print("\n" + tratar_erro_api(erro))

def tratar_erro_api(erro):
    detalhe = str(erro).upper()

    if "429" in detalhe or "RESOURCE_EXHAUSTED" in detalhe:
        return "Limite de utilização da API atingido. Aguarde a renovação da cota."

    elif "503" in detalhe or "UNAVAILABLE" in detalhe:
        return "O serviço do Gemini está temporariamente indisponível. Tente novamente."

    else:
        return f"Ocorreu um erro durante o atendimento: {erro}"
if __name__ == "__main__":
    iniciar_agente()