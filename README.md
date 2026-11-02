# Agente de Atendimento — Empório da Música

Agente de atendimento inteligente desenvolvido em Python como parte do desafio técnico para a posição de AI Engineer na Artefact.

O projeto simula um assistente virtual capaz de responder dúvidas de clientes da loja fictícia Empório da Música, consultando dados operacionais e aplicando as políticas de atendimento fornecidas no desafio.

## Objetivos

Desenvolver um agente que consiga:

- Buscar instrumentos musicais no catálogo.
- Consultar preços e promoções ativas.
- Verificar disponibilidade em estoque.
- Consultar pedidos e informações de entrega.
- Responder dúvidas sobre pagamentos, frete, trocas, devoluções e garantias.
- Respeitar o escopo de atendimento da empresa e evitar respostas sem fundamentação nos dados disponíveis.


## Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **Google Gemini API:** modelo de linguagem utilizado para interpretar solicitações e formular respostas.
- **Google GenAI SDK:** integração com a API Gemini e execução de Function Calling.
- **Pandas:** leitura e manipulação dos arquivos CSV.
- **Python-dotenv:** gerenciamento da chave de API por variável de ambiente.
- **Pytest:** testes automatizados das funcionalidades.

## Arquitetura e funcionamento

A solução utiliza uma abordagem de agente com Function Calling.

Em vez de depender exclusivamente do conhecimento do modelo, o agente recebe ferramentas em Python que permitem consultar informações específicas antes de responder ao usuário.

O fluxo geral é:

1. O usuário envia uma mensagem.
2. O Gemini interpreta a solicitação e identifica se precisa consultar alguma ferramenta.
3. A ferramenta correspondente é executada em Python.
4. Os dados encontrados são retornados ao modelo.
5. O Gemini utiliza o resultado para formular uma resposta em linguagem natural.

## Exemplos de conversas

Exemplos de interações e testes realizados durante o desenvolvimento
estão disponíveis em [`examples/conversas.md`](examples/conversas.md).
O documento apresenta cenários de atendimento, consultas comerciais
e validação de acesso a pedidos.

### Ferramentas implementadas

| Ferramenta | Responsabilidade |
|---|---|
| `buscar_produto` | Localizar produtos por nome ou descrição. |
| `consultar_estoque` | Consultar quantidade disponível e situação do produto. |
| `consultar_preco` | Consultar preço original, promoções ativas e economia. |
| `consultar_pedido` | Consultar pedido mediante confirmação do e-mail do cliente. |
| `buscar_politica` | Localizar informações no manual de políticas da loja. |

As consultas são realizadas por funções Python, mantendo a lógica de acesso aos dados separada da geração de respostas do modelo.

### Estratégia de recuperação de informações

Para os dados estruturados, são utilizadas consultas com Pandas sobre os arquivos CSV.

Para o manual de políticas, foi implementada uma busca textual baseada em seções, títulos e expansão de termos por sinônimos.

A solução não utiliza banco vetorial nem embeddings. A recuperação do manual é lexical e baseada no conteúdo do documento.

## Estrutura do projeto


desafio_artefact/
│
├── data/
│   ├── categories.csv
│   ├── customers.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── promotions.csv
│   ├── politicas_loja.md
│   ├── analisar_dados.py
│   └── validar_dados.py
│
├── src/
│   ├── agent.py
│   ├── data_loader.py
│   └── tools.py
│
├── tests/
│   ├── test_produtos.py
│   ├── test_precos.py
│   ├── test_pedidos.py
│   ├── test_politicas.py
│   └── test_erros.py
│
├── examples/
│   └── conversas.md
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── testar_carregamento.py
├── testar_gemini.py
└── testar_tools.py


## Requisitos

- Python 3.15.2 (versão utilizada durante o desenvolvimento e os testes).
- Chave de API do Google AI Studio.
- Git (opcional, para clonar o repositório).

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/FabioJrRodriguesGomes/desafio-artefact-ai-agent.git
cd desafio-artefact-ai-agent
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

Ativar no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar a chave da API

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
```

Substitua `sua_chave_aqui` pela chave gerada no Google AI Studio.

**Importante:** não compartilhe nem publique o arquivo `.env`. Ele está incluído no `.gitignore`.

### 5. Executar o agente

Na raiz do projeto:

```bash
python -m src.agent
```

O agente iniciará no terminal e permitirá enviar mensagens interativamente. Para encerrar, utilize o comando `sair`.

## Testes automatizados

O projeto utiliza Pytest para verificar as funcionalidades implementadas.

Execute:

```bash
python -m pytest -v
```

Os testes estão organizados por funcionalidade:

- Produtos e disponibilidade.
- Preços e promoções.
- Consulta de pedidos e validação de e-mail.
- Busca de políticas.
- Tratamento de erros.

Na versão atual, foram executados **24 testes automatizados, todos aprovados**.

## Decisões técnicas

- **Function Calling:** permite que o modelo solicite consultas específicas em funções Python, evitando depender exclusivamente de respostas geradas a partir do conhecimento geral do LLM.
- **Separação de responsabilidades:** carregamento de dados, ferramentas de consulta e interação com o modelo estão organizados em módulos diferentes.
- **Pandas e CSV:** escolha adequada ao volume e ao formato dos dados disponibilizados no desafio.
- **Busca textual no manual:** abordagem simples e de fácil manutenção, com expansão por sinônimos para melhorar a recuperação de informações.
- **Validação de pedidos:** a consulta exige o identificador do pedido e o e-mail associado ao cliente, como verificação básica antes de apresentar informações.
- **Restrições de escopo:** o agente foi orientado a atender exclusivamente assuntos relacionados à Empório da Música.

## Limitações conhecidas

- Os arquivos CSV representam uma base estática, não uma integração com sistemas operacionais em tempo real.
- A busca no manual utiliza correspondência textual e sinônimos, podendo não recuperar corretamente todas as perguntas formuladas de maneiras diferentes.
- A validação de identidade por e-mail é uma proteção básica de protótipo, não um mecanismo robusto de autenticação.
- O agente depende da disponibilidade e dos limites de uso da API Gemini.
- Algumas regras do manual apresentam ambiguidades ou informações que precisam de confirmação da gerência.
- Não há persistência de histórico de conversas entre execuções.

## Uso de ferramentas de IA durante o desenvolvimento

O ChatGPT foi utilizado como apoio ao aprendizado, planejamento da arquitetura, implementação de funcionalidades, identificação de erros e elaboração de testes.

O Gemini foi utilizado como modelo de linguagem integrado ao agente, por meio da API do Google AI Studio.

As decisões e implementações foram desenvolvidas e testadas iterativamente, com o objetivo de compreender o funcionamento das ferramentas e conseguir justificar as escolhas técnicas realizadas.

## Autor

Desenvolvido como projeto de desafio técnico para AI Engineer — Artefact.