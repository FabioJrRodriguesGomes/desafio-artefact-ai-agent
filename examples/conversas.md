# Exemplos de Conversas e Testes

Este documento apresenta exemplos de interações do agente de atendimento da Empório da Música e resultados de testes funcionais realizados durante o desenvolvimento.

As conversas foram executadas com o modelo Gemini integrado ao sistema por meio de Function Calling. Quando a transcrição integral não estava disponível, o resultado foi identificado como um resumo do teste.

---

## 1. Saudação e apresentação do agente

**Objetivo:** verificar se o agente inicia o atendimento com uma comunicação acolhedora e adequada à identidade da loja.

**Cliente:**
> Olá td bem?

**Agente:**
> Olá! Tudo ótimo por aqui, e com você? Seja muito bem-vindo(a) ao Empório da Música! Como posso te ajudar hoje? Está procurando algum instrumento específico, quer tirar dúvidas sobre pedidos ou saber mais sobre nossas políticas? Fique à vontade!

**Resultado:** comportamento esperado. O agente respondeu de maneira cordial e apresentou as principais possibilidades de atendimento.

---

## 2. Consulta sobre condições de parcelamento

**Objetivo:** verificar se o agente consulta as políticas comerciais antes de responder sobre condições de pagamento.

**Cliente:**
> Posso parcelar uma compra de 800 reais em 10 vezes?

**Resultado observado:**

O agente explicou que, para compras parceladas entre 7 e 12 vezes, a parcela mínima é de R$ 100,00. Portanto, uma compra de R$ 800,00 não atende à condição de parcelamento em 10 vezes, pois resultaria em parcelas de R$ 80,00.

Também apresentou a possibilidade de parcelamento em até 8 vezes de R$ 100,00 e informou sobre o desconto de 5% para pagamentos via PIX, conforme as políticas da loja.

**Resultado:** comportamento esperado. O agente utilizou as regras de parcelamento para avaliar a solicitação, em vez de responder apenas com informações genéricas.

---

## 3. Consulta de preço e promoção de produto

**Objetivo:** verificar se o agente utiliza os dados do catálogo e das promoções para informar corretamente os valores.

**Produto consultado:** Ohana CK-20 Concert Natural.

**Resultado da consulta:**

| Informação | Valor |
|---|---:|
| Preço original | R$ 549,00 |
| Desconto ativo | 20% |
| Preço promocional | R$ 439,20 |
| Economia | R$ 109,80 |

**Resultado:** consulta de preço executada com sucesso. O agente identificou o desconto ativo e apresentou os valores correspondentes.

---

## 4. Proteção de dados na consulta de pedidos

**Objetivo:** verificar se o agente impede o acesso a informações de pedidos quando os dados de identificação fornecidos não correspondem ao cadastro do cliente.

**Cenário:** um cliente tenta consultar um pedido utilizando um endereço de e-mail incorreto.

**Resultado observado:**

A ferramenta `consultar_pedido` identificou a divergência entre o e-mail informado e o e-mail cadastrado para o pedido. O agente recusou a solicitação e não revelou os detalhes da compra.

**Resultado:** comportamento esperado. A validação impede que informações do pedido sejam retornadas quando a identificação não corresponde ao cadastro.

---

## Considerações sobre os testes

Os exemplos demonstram diferentes aspectos do agente:

- Atendimento inicial e comunicação com o cliente.
- Interpretação de regras comerciais.
- Consulta de preços e promoções nos dados estruturados.
- Proteção de informações de pedidos por validação de identidade.

Os testes funcionais automatizados também verificam o comportamento das ferramentas em cenários de sucesso e erro.

**Limitação:** a validação por e-mail é uma proteção básica para este protótipo e não substitui um sistema robusto de autenticação. Além disso, os dados utilizados são estáticos, provenientes dos arquivos CSV disponibilizados no desafio.