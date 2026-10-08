# 🤖 Geo-Explorer — Assistente de Trilhas de IA com IBM Bob

> **Desafio Geo-Explorer** do Bootcamp DIO + IBM Bob. Projeto que constrói um assistente inteligente capaz de consultar trilhas de aprendizado, gerar desafios de código e emitir certificados fictícios — tudo orquestrado por um agente de IA com Slash Commands, Skills e um servidor MCP.

---

## 📋 Índice

1. [Visão Geral](#-visão-geral)
2. [Estrutura do Repositório](#-estrutura-do-repositório)
3. [Funcionalidades](#-funcionalidades)
4. [Como Usar](#-como-usar)
   - [Pré-requisitos](#pré-requisitos)
   - [Usando com IBM Bob](#usando-com-ibm-bob)
   - [Usando via MCP Server HTTP](#usando-via-mcp-server-http)
5. [Prompts Usados no Desenvolvimento](#-prompts-usados-no-desenvolvimento)
6. [Arquitetura e Decisões Técnicas](#️-arquitetura-e-decisões-técnicas)
7. [Testes](#-testes)
8. [Insights e Dicas para Profissionais](#-insights-e-dicas-para-profissionais)
9. [O que Aprendi](#-o-que-aprendi)
10. [Glossário](#-glossário)
11. [Tecnologias Utilizadas](#-tecnologias-utilizadas)
12. [Licença](#-licença)

---

## 🎯 Visão Geral

Este projeto demonstra na prática como construir um **sistema de agente de IA** usando o IBM Bob como orquestrador central. O assistente é capaz de:

- **Consultar trilhas** de aprendizagem em IA/ML de um catálogo com 25 trilhas reais
- **Gerar desafios de código** contextualizados por tecnologia e nível de dificuldade
- **Emitir certificados fictícios** estilizados no padrão DIO com badges, XP e código de verificação
- **Expor tudo via API MCP** acessível localmente (stdio) ou remotamente (HTTP/HTTPS/SSO)

O projeto é uma referência de como combinar **Slash Commands**, **Skills**, **MCP Servers** e **testes automatizados** em um único fluxo de trabalho orientado a IA.

---

## 📁 Estrutura do Repositório

```
projeto_final_DIO_IBM_BOB/
│
├── .bob/                          # Configurações do IBM Bob
│   └── skills/                    # Skills personalizadas
│       ├── trilha/SKILL.md        # Skill do comando /trilha
│       ├── desafio/SKILL.md       # Skill do comando /desafio
│       └── certificado/SKILL.md  # Skill do comando /certificado
│
├── .bobignore                     # Arquivos ignorados pelo Bob
│
├── commands/                      # Slash Commands do Bob
│   ├── trilha.md                  # Definição do comando /trilha
│   ├── desafio.md                 # Definição do comando /desafio
│   └── certificado.md             # Definição do comando /certificado
│
├── data/
│   └── trilhas_dio.json           # Catálogo com 25 trilhas de IA/ML
│
├── mcp/                           # MCP Server (Node.js + TypeScript)
│   ├── src/index.ts               # Código-fonte principal
│   ├── build/index.js             # Build compilado (pronto para rodar)
│   ├── package.json
│   ├── tsconfig.json
│   ├── .env.example               # Template de variáveis de ambiente
│   └── README.md                  # Documentação do servidor MCP
│
└── tests/
    ├── test_dio_commands.py       # Suite de 58 testes unitários (Python)
    └── resultados_testes.txt      # Relatório de execução dos testes
```

---

## ⚡ Funcionalidades

### `/trilha [tecnologia]`
Busca trilhas no catálogo por nome de tecnologia (busca case-insensitive por substring).

```
/trilha python
/trilha LangChain
/trilha tensor
```

**O que retorna:**
- Visão geral da trilha (nível, XP, módulos, acesso)
- Cronograma de módulos distribuído por semanas
- Badges disponíveis
- Lives ao vivo com datas e duração
- Promoção ativa com cupom
- Trilhas complementares sugeridas
- Mensagem motivacional

---

### `/desafio [tecnologia] [nível]`
Gera um desafio de código contextualizado com cenário fictício de empresa.

```
/desafio Python Iniciante
/desafio TensorFlow Avançado
/desafio LangChain Intermediário
```

**Níveis e XP:**
| Nível | Tempo sugerido | XP |
|---|---|---|
| Iniciante | 30 minutos | 150 XP |
| Intermediário | 1 hora | 350 XP |
| Avançado | 2 horas+ | 700 XP |

**O que retorna:**
- Descrição com cenário fictício (empresa DataStartup Inc.)
- Objetivos numerados
- Entradas e saídas esperadas
- Dicas técnicas (sem entregar a solução)
- Casos de teste
- Critérios de avaliação

---

### `/certificado [nome] | [trilha]`
Emite um certificado fictício DIO de conclusão de trilha.

```
/certificado Mateus Uchoa | Python
/certificado Ana Silva | LangChain
```

**O que retorna:**
- Certificado formatado em Markdown estilo DIO
- Data de emissão no formato DD/MM/AAAA
- Carga horária calculada (`módulos × 8h`)
- XP total da trilha
- Lista de badges conquistadas
- Código de verificação fictício (`XXXX-XXXX-XXXX-XXXX`)
- Opção de salvar como arquivo `.md` em `docs/certificados-emitidos/`

---

## 🚀 Como Usar

### Pré-requisitos

- [IBM Bob](https://www.ibm.com/products/ibm-watsonx-code-assistant) instalado
- Node.js ≥ 18 (para o MCP Server)
- Python ≥ 3.8 (para os testes)
- Git

---

### Usando com IBM Bob

**1. Clone o repositório:**
```bash
git clone https://github.com/MateusUchoa/projeto_final_DIO_IBM_BOB.git
cd projeto_final_DIO_IBM_BOB
```

**2. Abra a pasta no IBM Bob.**
O Bob detectará automaticamente os arquivos em `commands/` e `.bob/skills/` e os disponibilizará como comandos e skills.

**3. Use os comandos diretamente no chat:**
```
/trilha python
/desafio Python Iniciante
/certificado Seu Nome | Python
```

**4. Para usar o MCP Server localmente (stdio), adicione ao seu `mcp.json`:**
```json
{
  "mcpServers": {
    "dio-bob": {
      "command": "node",
      "args": ["/caminho/absoluto/para/mcp/build/index.js"]
    }
  }
}
```

---

### Usando via MCP Server HTTP

**1. Instale as dependências e compile:**
```bash
cd mcp
npm install
npm run build
```

**2. Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite .env com seu API_KEY e PORT
```

**3. Inicie o servidor:**
```bash
# Modo HTTP (porta 3000 por padrão)
node build/index.js --http

# Com variáveis explícitas
MCP_TRANSPORT=http PORT=3000 API_KEY=sua_chave node build/index.js
```

**4. Verifique o health-check:**
```bash
curl http://localhost:3000/health
```

**5. Registre no Bob como servidor remoto:**
```json
{
  "mcpServers": {
    "dio-bob-remote": {
      "url": "https://seu-dominio.com/mcp",
      "headers": {
        "Authorization": "Bearer ${env:DIO_BOB_API_KEY}"
      }
    }
  }
}
```

**Ferramentas MCP disponíveis:**
| Tool | Descrição |
|---|---|
| `listar_trilhas` | Lista o catálogo com filtro por nível |
| `trilha_buscar` | Busca e retorna plano de estudos |
| `trilha_aleatoria` | Sorteia uma trilha aleatória |
| `desafio_gerar` | Gera desafio de código |
| `certificado_gerar` | Emite certificado fictício |

---

## 💬 Prompts Usados no Desenvolvimento

Esta seção documenta os prompts reais utilizados durante o desenvolvimento do projeto no IBM Bob. São um guia valioso para quem quer entender como dirigir um agente de IA para construir sistemas completos.

---

### 1. Verificar estado do repositório
```
no repositório recém criado mostra como ele esta em formato de árvore
```
**Resultado:** O Bob usou `git ls-remote` + `tree` para exibir a estrutura completa do repositório remoto em formato de árvore ASCII.

**Insight:** Antes de qualquer implementação, verificar o estado atual evita retrabalho e conflitos. O Bob usa ferramentas de sistema para inspecionar sem especulação.

---

### 2. Criar testes unitários com cobertura mínima
```
Bob crie arquivos de teste unitários e teste este fluxo para atingir uma cobertura 
de 70% de aprovação, teste os comandos /trilha para consultar trilhas aleatórias, 
gere um arquivo de /desafio para o aluno e um /certificado para o mesmo. 
Grave os resultados em um arquivo txt para acompanhamento.
```
**Resultado:** Suite de 58 testes unitários em Python cobrindo `TrilhaEngine`, `DesafioEngine`, `CertificadoEngine` e um `TestFluxoCompleto` integrado. Taxa final: **100% (58/58)**. Resultados gravados em `tests/resultados_testes.txt`.

**Técnica usada:** O prompt especifica **métrica quantitativa** (70%), **escopo** (3 comandos), **fluxo** (trilha → desafio → certificado) e **entregável** (arquivo txt). Isso direciona o agente a criar lógica testável pura (engines desacopladas) em vez de scripts acoplados a arquivos.

---

### 3. Criar o MCP Server com múltiplos transportes
```
Bob, quero que você crie um MCP server do projeto e suba no repositório remoto 
para que futuramente pessoas possam vir acessar por meio de um servidor https ou 
sso ou via api. Use a pasta mcp para isso.
```
**Resultado:** Servidor MCP completo em TypeScript com:
- 5 ferramentas MCP (`listar_trilhas`, `trilha_buscar`, `trilha_aleatoria`, `desafio_gerar`, `certificado_gerar`)
- Transporte stdio (para Bob como subprocesso)
- Transporte HTTP Streamable com sessões por UUID
- Autenticação Bearer token via `API_KEY`
- Endpoint `/health` para monitoramento
- Documentação de integração com HTTPS, Caddy, nginx e Kong

**Técnica usada:** O prompt menciona **casos de uso futuros** (HTTPS, SSO, API) sem especificar implementação. O agente inferiu o padrão Streamable HTTP Transport do protocolo MCP 2024-11-05 como a solução correta.

---

### 4. Limpar arquivos desnecessários do repositório
```
ainda bem que percebi a tempo exclua/delete do repositório o arquivo hello.md 
e todos os arquivos .gitkeep das pastas que você criou porque não podia criar 
as pastas vazias no repositório para ficar somente os arquivos que realmente 
fazem parte do projeto
```
**Resultado:** Remoção cirúrgica via `git rm` de `hello.md` + 4 arquivos `.gitkeep` com commit e push automatizados.

**Insight:** `.gitkeep` é uma convenção para manter pastas vazias no Git. Assim que as pastas recebem conteúdo real, os `.gitkeep` devem ser removidos — o projeto fica mais limpo e profissional.

---

### 5. Documentar todo o projeto
```
Bob agora documente todo o projeto feito até o momento, com todos os prompts usados, 
modos de uso, dicas de uso e insights para futuros profissionais ou pessoas aprendendo 
sobre o assunto e quiser pesquisar no repositório
```
**Resultado:** Este arquivo `README.md`.

**Técnica usada:** Documentação dirigida por prompt lê todos os artefatos existentes antes de escrever — evitando inventar comportamentos não implementados. O resultado é uma documentação **baseada em evidências**, não em suposições.

---

## 🏗️ Arquitetura e Decisões Técnicas

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                      USUÁRIO                            │
│  digita: /trilha python  /desafio Python Iniciante      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   IBM BOB (Host MCP)                    │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  commands/  │  │ .bob/skills/ │  │  mcp.json    │   │
│  │  trilha.md  │  │  trilha/     │  │  (registro   │   │
│  │  desafio.md │  │  desafio/    │  │   do server) │   │
│  │  certif.md  │  │  certif/     │  └──────┬───────┘   │
│  └──────┬──────┘  └──────┬───────┘         │           │
│         │                │                  │           │
└─────────┼────────────────┼──────────────────┼───────────┘
          │                │                  │
          ▼                ▼                  ▼
┌─────────────────┐ ┌──────────────┐ ┌───────────────────┐
│  Slash Command  │ │    Skill     │ │   MCP Server      │
│  (instrução de  │ │ (instrução   │ │   (Node.js)       │
│   execução)     │ │  estendida)  │ │                   │
└────────┬────────┘ └──────┬───────┘ │  ┌─────────────┐ │
         │                 │         │  │listar_trilhas│ │
         └────────┬─────────┘        │  │trilha_buscar │ │
                  │                  │  │trilha_random │ │
                  ▼                  │  │desafio_gerar │ │
         ┌────────────────┐          │  │certif_gerar  │ │
         │ data/          │◄─────────│  └─────────────┘ │
         │ trilhas_dio    │          │                   │
         │ .json          │          │  stdio | HTTP     │
         │ (25 trilhas)   │          └───────────────────┘
         └────────────────┘
```

---

### Por que Skills + Commands separados?

O projeto mantém **dois artefatos paralelos** para cada funcionalidade:

| Artefato | Localização | Quando é usado |
|---|---|---|
| **Slash Command** | `commands/*.md` | Quando o usuário digita `/trilha` no chat |
| **Skill** | `.bob/skills/*/SKILL.md` | Quando o Bob precisa ativar a lógica internamente |

Os **Slash Commands** são a interface do usuário — instruções de execução passo a passo que o Bob segue quando o usuário digita o comando. As **Skills** são instruções que o Bob pode carregar autonomamente em qualquer contexto, sem o usuário precisar digitar o slash.

---

### Por que MCP Server em TypeScript?

- **Tipagem forte**: o schema de cada tool é validado em tempo de compilação com `zod`
- **Ecossistema MCP**: o SDK oficial `@modelcontextprotocol/sdk` é em TypeScript/JavaScript
- **Flexibilidade de transporte**: o mesmo código serve stdio (Bob local) e HTTP (acesso remoto) via flag `--http`
- **Produção-ready**: o Streamable HTTP Transport é o padrão MCP 2024-11-05, compatível com qualquer cliente MCP moderno

---

### Estrutura do `trilhas_dio.json`

```json
{
  "trilhas": [
    {
      "id": 1,
      "nome": "Fundamentos de Inteligência Artificial com Python",
      "tecnologia": ["Python", "NumPy", "Pandas", "Scikit-learn"],
      "nivel": "Iniciante",
      "modulos": 8,
      "xp_total": 3200,
      "badges": ["Python Starter", "AI Explorer", "Data Wrangler"],
      "promocoes": {
        "desconto": "30%",
        "validade": "2025-12-31",
        "cupom": "DIO30AI"
      },
      "vitalicio": true,
      "lives_ao_vivo": [
        {
          "titulo": "Introdução ao ecossistema Python para IA",
          "data": "2025-02-10",
          "duracao_min": 90
        }
      ]
    }
    // ... 24 trilhas adicionais
  ]
}
```

O catálogo cobre 25 trilhas em 3 níveis:
- **Iniciante** (4 trilhas): Python/IA, AutoML, Engenharia de Prompts, IA Ética
- **Intermediário** (11 trilhas): ML, Visão Computacional, GenAI, Azure AI, Gemini, etc.
- **Avançado** (10 trilhas): Deep Learning, MLOps, NLP, Robótica, Saúde, etc.

---

## 🧪 Testes

### Executar localmente

```bash
python tests/test_dio_commands.py
```

Os resultados são gravados automaticamente em `tests/resultados_testes.txt`.

### Estrutura da suite

```
TestTrilhaEngine       (19 testes)
├── test_busca_exata_retorna_trilha
├── test_busca_case_insensitive
├── test_busca_substring
├── test_busca_inexistente_retorna_lista_vazia
├── test_busca_por_nome_da_trilha
├── test_busca_retorna_campos_obrigatorios
├── test_trilha_aleatoria_retorna_dict
├── test_trilha_aleatoria_tem_id
├── test_multiplas_trilhas_aleatorias_variam
├── test_formatar_plano_retorna_string
├── test_formatar_plano_contem_nome_trilha
├── test_formatar_plano_contem_xp
├── test_formatar_plano_contem_badges
├── test_formatar_plano_vitalicio
├── test_formatar_plano_nao_vitalicio
├── test_listar_tecnologias_retorna_lista
├── test_listar_tecnologias_sem_duplicatas
└── test_listar_tecnologias_contem_python

TestDesafioEngine      (16 testes)
├── test_nivel_iniciante/intermediario/avancado_valido
├── test_nivel_invalido / test_nivel_vazio_invalido
├── test_gerar_iniciante / intermediario / avancado
├── test_gerar_campos_obrigatorios
├── test_gerar_tecnologia_vazia_lanca_excecao
├── test_gerar_nivel_invalido_lanca_excecao
├── test_gerar_tem_dois_casos_de_teste
├── test_titulo_contem_tecnologia_e_nivel
└── test_formatar_retorna_string / contem_titulo / xp / tempo

TestCertificadoEngine  (18 testes)
├── test_gerar_retorna_dict
├── test_nome_usuario_em_maiusculas
├── test_carga_horaria_calculada         (módulos × 8)
├── test_xp_total_correto
├── test_badges_corretas
├── test_codigo_verificacao_formato      (XXXX-XXXX-XXXX-XXXX)
├── test_codigo_unico_a_cada_geracao
├── test_data_emissao_formato_brasileiro (DD/MM/AAAA)
├── test_nome_vazio_lanca_excecao
├── test_tecnologias_formatadas
└── test_formatar_* / test_nome_arquivo_*

TestFluxoCompleto      (5 testes)
├── test_fluxo_trilha_aleatoria_desafio_certificado
├── test_fluxo_python_iniciante
├── test_fluxo_langchain_intermediario
├── test_fluxo_tensorflow_avancado
└── test_formatacao_completa_gera_markdown
```

**Resultado:** 58/58 ✅ — 100% de aprovação (meta: 70%)

---

## 💡 Insights e Dicas para Profissionais

### Para quem está aprendendo sobre Agentes de IA

**1. Prompt Engineering é design de software**
O prompt não é uma "frase mágica" — é uma especificação funcional. Um bom prompt define: *o que fazer*, *como fazer*, *o formato da saída* e *o que fazer em caso de erro*. Veja como os Slash Commands deste projeto estruturam cada passo de execução como um algoritmo legível.

**2. Separe lógica de negócio da interface**
Os `engines` nos testes (`TrilhaEngine`, `DesafioEngine`, `CertificadoEngine`) são a lógica pura — sem dependência do Bob, sem arquivos, sem estado externo. Isso é o que permite testar 58 cenários em 0.002 segundos. Sempre que construir um agente, pergunte: *qual parte deste código pode ser testada sem o LLM?*

**3. MCP é o HTTP dos agentes**
O Model Context Protocol padroniza como agentes descobrem e chamam ferramentas, da mesma forma que HTTP padroniza como browsers se comunicam com servidores. Aprender MCP hoje é equivalente a aprender REST API em 2010 — será fundacional.

**4. Skills vs Commands: camadas de abstração**
- **Command** = interface do usuário (o usuário digita `/trilha`)
- **Skill** = comportamento do agente (o Bob "sabe" como buscar trilhas)
- **MCP Tool** = serviço consumível por qualquer cliente MCP

Cada camada tem sua responsabilidade. Misturá-las cria acoplamento desnecessário.

**5. O `.bobignore` é tão importante quanto o `.gitignore`**
Arquivos grandes, credenciais, caches e outputs gerados não devem estar no contexto do agente. Um contexto poluído degrada a qualidade das respostas. Seja deliberado sobre o que o agente vê.

---

### Para quem quer expandir este projeto

**Ideia 1 — Progresso do aluno**
Crie `data/cache-progresso/[usuario].json` para rastrear quais trilhas e desafios cada aluno já acessou. A pasta já está no `.bobignore` aguardando uso.

**Ideia 2 — Certificados reais em PDF**
Use a tool `certificado_gerar` do MCP Server + uma biblioteca como `puppeteer` ou `pdfkit` para gerar PDFs reais a partir do Markdown.

**Ideia 3 — Integração com GitHub Actions**
Adicione um workflow `.github/workflows/tests.yml` que rode `python tests/test_dio_commands.py` a cada push. O arquivo de resultados em `txt` pode ser publicado como artefato da CI.

**Ideia 4 — Autenticação SSO real**
O MCP Server já tem suporte a Bearer token. Para SSO real (OAuth2/OIDC), coloque um API gateway (Keycloak, Auth0, AWS Cognito) na frente que valide o JWT e injete o header `Authorization: Bearer <internal-key>` ao fazer proxy para o servidor MCP.

**Ideia 5 — Dashboard de analytics**
Adicione logging estruturado (JSON) no `src/index.ts` para cada chamada de tool. Conecte a um Elasticsearch ou Grafana Loki para visualizar quais trilhas são mais consultadas.

**Ideia 6 — RAG sobre o catálogo**
Indexe o `trilhas_dio.json` em um vector store (FAISS, Pinecone, ChromaDB) e substitua a busca por substring por busca semântica. `/trilha redes neurais para imagens médicas` encontraria a trilha correta mesmo sem a tecnologia exata.

---

### Armadilhas comuns a evitar

| Armadilha | O que acontece | Como evitar |
|---|---|---|
| `console.log` no servidor MCP | Corrompe o canal stdio do protocolo MCP | **Sempre use `console.error`** para logs no servidor |
| Hardcodar credenciais | Vazamento de API keys no repositório | Use `process.env.API_KEY` + `.env.example` sem valores reais |
| Deixar `node_modules/` no repositório | Repositório gigante, conflitos de plataforma | Adicione ao `.gitignore` / `.bobignore` |
| `.gitkeep` em pastas com conteúdo | Arquivo desnecessário, repositório sujo | Remova quando a pasta receber arquivos reais |
| Skills e Commands duplicados desatualizados | Comportamento inconsistente | Mantenha os dois em sincronia ou escolha apenas um |

---

## 📖 Glossário

| Termo | Definição |
|---|---|
| **IBM Bob** | Assistente de IA da IBM baseado em watsonx, com suporte a agentes, MCP e comandos personalizados |
| **MCP** | Model Context Protocol — padrão aberto para comunicação entre hosts de IA e servidores de ferramentas |
| **Slash Command** | Arquivo `.md` em `commands/` que define como o Bob executa um comando digitado pelo usuário |
| **Skill** | Arquivo `SKILL.md` em `.bob/skills/` que o Bob pode ativar automaticamente para executar uma tarefa |
| **MCP Tool** | Função registrada no servidor MCP que pode ser chamada por qualquer cliente do protocolo |
| **Streamable HTTP Transport** | Transporte MCP baseado em HTTP com suporte a SSE para streaming (padrão 2024-11-05) |
| **Bearer Token** | Mecanismo de autenticação HTTP onde o cliente envia um token no header `Authorization: Bearer <token>` |
| **XP** | Experience Points — métrica fictícia de progresso usada na gamificação da plataforma DIO |
| **Código de Verificação** | String alfanumérica de 16 chars (`XXXX-XXXX-XXXX-XXXX`) que identifica unicamente um certificado |
| **`.bobignore`** | Arquivo que lista padrões de arquivos/pastas que o Bob deve ignorar ao ler o workspace |
| **Engine** | Classe Python pura (sem efeitos colaterais) que encapsula a lógica de negócio testável |

---

## 🎓 O que Aprendi

Este desafio foi muito mais do que gerar código com uma IA — foi aprender a **trabalhar com um agente como parceiro de desenvolvimento**, entendendo o que ele faz bem, onde ele precisa de direção e como validar o que ele entrega.

### Sobre Agentes de IA na prática
- **Prompts são especificações, não pedidos.** Quanto mais claro eu era sobre o formato de saída, os casos de erro e os critérios de aceitação, melhor e mais preciso era o resultado. A diferença entre "crie testes" e "crie testes com 70% de cobertura, cobrindo os 3 comandos, gravando resultado em txt" é enorme.
- **O agente não especula — ele lê.** Antes de qualquer implementação, o Bob inspecionava os arquivos existentes. Isso evitou retrabalho e conflitos. Aprendi a sempre verificar o estado atual antes de pedir uma mudança.
- **Revisar o que o agente entrega é parte do trabalho.** Percebi que arquivos como `hello.md` e `.gitkeep` foram criados como scaffolding inicial e precisavam ser removidos antes da entrega. O agente não toma essa decisão sozinho — cabe ao desenvolvedor.

### Sobre o protocolo MCP
- Entendi que o **MCP (Model Context Protocol)** funciona como uma API padronizada para ferramentas de IA. Da mesma forma que qualquer aplicação pode consumir uma REST API, qualquer cliente MCP pode consumir as ferramentas do servidor que construímos — independente de qual LLM está sendo usado.
- Aprendi a diferença entre **transporte stdio** (quando o Bob inicia o servidor como subprocesso) e **transporte HTTP** (quando o servidor roda de forma independente e aceita conexões remotas).
- Entendi por que `console.log` quebra o servidor MCP em modo stdio: a saída padrão é o canal do protocolo, então qualquer texto que não seja JSON-RPC corrompe a comunicação.

### Sobre estrutura de projetos com IA
- **Skills e Commands são camadas diferentes** com propósitos distintos: o Command é acionado pelo usuário com `/`, enquanto a Skill é o comportamento que o agente carrega internamente. Manter os dois em sincronia é responsabilidade do desenvolvedor.
- **Separar lógica de negócio das integrações** permitiu criar 58 testes unitários que rodam em 0.002 segundos, sem depender do LLM, sem arquivos externos. Isso mostrou que boas práticas de software se aplicam igualmente a projetos com IA.
- **O `.bobignore` tem o mesmo papel do `.gitignore`**: define o que o agente não precisa ver. Um contexto limpo produz respostas mais precisas.

### Melhorias que realizei além do básico
- Catálogo com **25 trilhas** reais de IA/ML (o desafio pedia apenas trilhas fictícias)
- **MCP Server com duplo transporte** (stdio + HTTP Streamable) pronto para produção
- **Autenticação Bearer token** com variável de ambiente para o servidor HTTP
- **58 testes automatizados** com 100% de aprovação (a meta era 70%)
- Documentação detalhada dos **5 prompts reais** usados no desenvolvimento, com análise técnica de cada um
- **Diagrama de arquitetura** em ASCII mostrando o fluxo completo de componentes

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| IBM Bob | — | Orquestrador de IA, host MCP, execução de commands/skills |
| TypeScript | 5.8+ | Código-fonte do servidor MCP |
| Node.js | 18+ | Runtime do servidor MCP |
| `@modelcontextprotocol/sdk` | 1.12+ | SDK oficial do protocolo MCP |
| `zod` | 3.25+ | Validação de schemas das MCP tools |
| Python | 3.8+ | Suite de testes unitários |
| `unittest` | stdlib | Framework de testes Python |
| Git | — | Controle de versão |
| GitHub | — | Hospedagem do repositório remoto |

---

## 📄 Licença

MIT — Projeto educacional desenvolvido durante o Bootcamp DIO + IBM Bob.

---

<div align="center">

**Desenvolvido com 🤖 IBM Bob durante o Bootcamp DIO — Desafio Geo-Explorer**

*"A melhor forma de aprender IA é construindo com ela."*

</div>
