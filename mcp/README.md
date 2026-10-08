# DIO IBM Bob — MCP Server

Servidor [MCP (Model Context Protocol)](https://modelcontextprotocol.io) do projeto final do bootcamp **DIO + IBM Bob**.

Expõe as funcionalidades de trilhas, desafios e certificados como **ferramentas MCP** acessíveis por:

- **IBM Bob** (via stdio — subprocesso local)
- **HTTPS / API REST** (via Streamable HTTP Transport)
- **SSO / API Gateway** — coloque um proxy reverso com autenticação na frente (nginx, Caddy, Kong, AWS API Gateway etc.)

---

## Ferramentas disponíveis

| Tool | Descrição |
|---|---|
| `listar_trilhas` | Lista todo o catálogo DIO com filtro por nível |
| `trilha_buscar` | Busca trilha por tecnologia e retorna plano de estudos completo |
| `trilha_aleatoria` | Sorteia uma trilha do catálogo (com filtro de nível opcional) |
| `desafio_gerar` | Gera desafio de código contextualizado por tecnologia e nível |
| `certificado_gerar` | Emite certificado fictício DIO para um aluno e trilha concluída |

---

## Pré-requisitos

- **Node.js ≥ 18**
- **npm ≥ 9**

---

## Instalação

```bash
cd mcp
npm install
npm run build
```

O arquivo compilado ficará em `mcp/build/index.js`.

---

## Modos de execução

### 1. Modo stdio (IBM Bob como host)

Adicione ao seu `mcp.json` do Bob:

```json
{
  "mcpServers": {
    "dio-bob": {
      "command": "node",
      "args": ["/caminho/absoluto/para/mcp/build/index.js"],
      "env": {}
    }
  }
}
```

O servidor iniciará automaticamente quando o Bob precisar de uma tool.

---

### 2. Modo HTTP (acesso remoto / HTTPS / API)

```bash
# Copiar e editar as variáveis de ambiente
cp .env.example .env
# Edite .env e defina API_KEY e PORT

# Iniciar em modo HTTP
MCP_TRANSPORT=http PORT=3000 API_KEY=sua_chave node build/index.js
# ou simplesmente:
node build/index.js --http
```

O servidor ficará disponível em:
- `POST/GET/DELETE http://localhost:3000/mcp` — endpoint MCP principal
- `GET http://localhost:3000/health` — health-check

---

### 3. Atrás de HTTPS (produção)

Use um proxy reverso para expor o servidor com TLS. Exemplo com **Caddy**:

```caddyfile
mcp.seudominio.com {
    reverse_proxy localhost:3000
}
```

Ou com **nginx**:

```nginx
server {
    listen 443 ssl;
    server_name mcp.seudominio.com;
    # ... configuração TLS ...
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Registre no Bob como servidor remoto:

```json
{
  "mcpServers": {
    "dio-bob-remote": {
      "url": "https://mcp.seudominio.com/mcp",
      "headers": {
        "Authorization": "Bearer ${env:DIO_BOB_API_KEY}"
      }
    }
  }
}
```

---

## Autenticação

O servidor suporta autenticação via **Bearer token**:

```
Authorization: Bearer <API_KEY>
```

- Se `API_KEY` **não estiver definida** → servidor roda sem autenticação (apenas para dev/local)
- Se `API_KEY` **estiver definida** → toda requisição HTTP deve incluir o header `Authorization`

Para SSO, coloque um **API gateway** (Kong, AWS API Gateway, Keycloak Gatekeeper) na frente do servidor que:
1. Valide o token SSO/OAuth2/OIDC
2. Adicione o header `Authorization: Bearer <API_KEY>` ao fazer o proxy para o MCP Server

---

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `MCP_TRANSPORT` | `stdio` | Transporte: `stdio` ou `http` |
| `PORT` | `3000` | Porta HTTP |
| `API_KEY` | _(vazia)_ | Chave Bearer para autenticação HTTP |
| `DATA_PATH` | `../data/trilhas_dio.json` | Caminho para o JSON de trilhas |

---

## Exemplos de uso via API

### Health-check
```bash
curl http://localhost:3000/health
```

### Iniciar sessão MCP e listar trilhas

```bash
# 1. Inicializar sessão
curl -s -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sua_chave" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl-client","version":"0.1"}}}'

# 2. Chamar a tool listar_trilhas (usando o Mcp-Session-Id retornado)
curl -s -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sua_chave" \
  -H "Mcp-Session-Id: <session-id>" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"listar_trilhas","arguments":{"nivel":"todos"}}}'
```

---

## Estrutura de arquivos

```
mcp/
├── src/
│   └── index.ts          # Código-fonte principal (TypeScript)
├── build/                # Código compilado (gerado por npm run build)
│   └── index.js
├── data/                 # Symlink ou cópia de ../data/ (opcional)
├── package.json
├── tsconfig.json
├── .env.example          # Template de variáveis de ambiente
└── README.md
```

---

## Desenvolvimento

```bash
# Build incremental
npm run build

# Rodar em modo stdio (debug)
node build/index.js --stdio

# Rodar em modo HTTP (debug, sem autenticação)
node build/index.js --http
```

---

## Licença

MIT — Projeto educacional do bootcamp DIO + IBM Bob.
