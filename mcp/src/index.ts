#!/usr/bin/env node
/**
 * DIO IBM Bob — MCP Server
 * ========================
 * Expõe as funcionalidades do projeto como ferramentas MCP:
 *   - trilha_buscar      : busca trilhas por tecnologia
 *   - trilha_aleatoria   : retorna uma trilha aleatória do catálogo
 *   - desafio_gerar      : gera um desafio de código por tecnologia e nível
 *   - certificado_gerar  : emite certificado fictício DIO para um aluno
 *
 * Transportes suportados:
 *   --stdio  (padrão quando chamado pelo Bob como subprocesso)
 *   --http   Streamable HTTP na porta PORT (padrão 3000)
 *            Recomendado para acesso remoto via HTTPS / SSO / API gateway
 *
 * Variáveis de ambiente:
 *   PORT          Porta HTTP (padrão: 3000)
 *   API_KEY       Chave de autenticação Bearer para o transporte HTTP
 *                 Se não definida, o servidor roda sem autenticação (apenas local/dev)
 *   DATA_PATH     Caminho absoluto para trilhas_dio.json
 *                 (padrão: ../data/trilhas_dio.json relativo a este arquivo)
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { randomUUID } from "crypto";
import { createServer, IncomingMessage, ServerResponse } from "http";
import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { z } from "zod";

// ---------------------------------------------------------------------------
// Tipos
// ---------------------------------------------------------------------------

interface Promocao {
  desconto: string;
  validade: string;
  cupom: string;
}

interface Live {
  titulo: string;
  data: string;
  duracao_min: number;
}

interface Trilha {
  id: number;
  nome: string;
  tecnologia: string[];
  nivel: string;
  modulos: number;
  xp_total: number;
  badges: string[];
  promocoes: Promocao;
  vitalicio: boolean;
  lives_ao_vivo: Live[];
}

interface TrilhasDB {
  trilhas: Trilha[];
}

// ---------------------------------------------------------------------------
// Carregamento dos dados
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function carregarTrilhas(): Trilha[] {
  const dataPath =
    process.env.DATA_PATH ??
    resolve(__dirname, "..", "data", "trilhas_dio.json");
  try {
    const raw = readFileSync(dataPath, "utf-8");
    const db: TrilhasDB = JSON.parse(raw);
    return db.trilhas;
  } catch {
    // Fallback: catálogo embutido mínimo para o servidor funcionar mesmo sem o arquivo
    console.error(
      `[WARN] Não foi possível carregar ${dataPath}. Usando catálogo embutido mínimo.`
    );
    return CATALOGO_EMBUTIDO;
  }
}

// Catálogo embutido de emergência (subset das 6 trilhas mais usadas nos testes)
const CATALOGO_EMBUTIDO: Trilha[] = [
  {
    id: 1,
    nome: "Fundamentos de Inteligência Artificial com Python",
    tecnologia: ["Python", "NumPy", "Pandas", "Scikit-learn"],
    nivel: "Iniciante",
    modulos: 8,
    xp_total: 3200,
    badges: ["Python Starter", "AI Explorer", "Data Wrangler"],
    promocoes: { desconto: "30%", validade: "2025-12-31", cupom: "DIO30AI" },
    vitalicio: true,
    lives_ao_vivo: [
      {
        titulo: "Introdução ao ecossistema Python para IA",
        data: "2025-02-10",
        duracao_min: 90,
      },
    ],
  },
  {
    id: 6,
    nome: "Generative AI com LangChain e OpenAI",
    tecnologia: ["Python", "LangChain", "OpenAI API", "FAISS"],
    nivel: "Intermediário",
    modulos: 11,
    xp_total: 6200,
    badges: ["GenAI Builder", "Prompt Engineer", "LangChain Dev", "RAG Master"],
    promocoes: { desconto: "35%", validade: "2025-08-31", cupom: "GENAI35" },
    vitalicio: true,
    lives_ao_vivo: [
      {
        titulo: "Criando aplicações RAG com LangChain",
        data: "2025-02-20",
        duracao_min: 120,
      },
    ],
  },
  {
    id: 8,
    nome: "MLOps: Deploy e Monitoramento de Modelos de IA",
    tecnologia: ["Python", "MLflow", "Docker", "Kubernetes", "AWS SageMaker"],
    nivel: "Avançado",
    modulos: 15,
    xp_total: 8200,
    badges: [
      "MLOps Engineer",
      "Pipeline Builder",
      "Cloud AI Deployer",
      "Model Monitor",
      "DevOps AI",
    ],
    promocoes: { desconto: "20%", validade: "2025-11-15", cupom: "MLOPS20" },
    vitalicio: true,
    lives_ao_vivo: [
      {
        titulo: "Pipelines de ML com MLflow na prática",
        data: "2025-03-05",
        duracao_min: 150,
      },
    ],
  },
];

// ---------------------------------------------------------------------------
// Helpers de lógica de negócio
// ---------------------------------------------------------------------------

function buscarTrilhas(trilhas: Trilha[], tecnologia: string): Trilha[] {
  const termo = tecnologia.trim().toLowerCase();
  return trilhas.filter(
    (t) =>
      t.tecnologia.some((tech) => tech.toLowerCase().includes(termo)) ||
      t.nome.toLowerCase().includes(termo)
  );
}

function formatarDuracao(minutos: number): string {
  const h = Math.floor(minutos / 60);
  const m = minutos % 60;
  return h > 0 ? (m > 0 ? `${h}h${m.toString().padStart(2, "0")}min` : `${h}h`) : `${m}min`;
}

function formatarPlano(trilha: Trilha): string {
  const acesso = trilha.vitalicio ? "Vitalício ♾" : "Por tempo limitado ⏳";
  const tecnologias = trilha.tecnologia.join(" · ");
  const badges = trilha.badges.map((b) => `  🏅 ${b}`).join("\n");
  const lives = trilha.lives_ao_vivo
    .map(
      (l) =>
        `  - ${l.titulo} — ${l.data} (${formatarDuracao(l.duracao_min)})`
    )
    .join("\n");
  const cronograma = Array.from({ length: trilha.modulos }, (_, i) =>
    `  Semana ${Math.floor(i / 2) + 1} — Módulo ${i + 1}: Tópico ${i + 1}`
  ).join("\n");
  const p = trilha.promocoes;

  return [
    `# 🎯 Plano de Estudos — ${trilha.nome}`,
    "",
    "## Visão Geral",
    "| Campo         | Detalhe                          |",
    "|---------------|----------------------------------|",
    `| Nível         | ${trilha.nivel}                  |`,
    `| Tecnologias   | ${tecnologias}                   |`,
    `| Total Módulos | ${trilha.modulos}                |`,
    `| XP Total      | ${trilha.xp_total} XP            |`,
    `| Acesso        | ${acesso}                        |`,
    "",
    "## 🗓️ Cronograma de Módulos",
    cronograma,
    "",
    "## 🏅 Badges Disponíveis",
    badges,
    "",
    "## 📺 Lives ao Vivo",
    lives || "  Nenhuma live cadastrada.",
    "",
    "## 🏷️ Promoção Ativa",
    `  Desconto: **${p.desconto}** | Cupom: \`${p.cupom}\` | Validade: ${p.validade}`,
    "",
    "🚀 *Bora começar! Cada módulo concluído te aproxima do seu próximo nível!*",
  ].join("\n");
}

function gerarDesafio(tecnologia: string, nivel: string): string {
  const XP: Record<string, number> = {
    Iniciante: 150,
    Intermediário: 350,
    Avançado: 700,
  };
  const TEMPO: Record<string, string> = {
    Iniciante: "30 minutos",
    Intermediário: "1 hora",
    Avançado: "2 horas ou mais",
  };

  if (!["Iniciante", "Intermediário", "Avançado"].includes(nivel)) {
    throw new Error(
      `Nível inválido: "${nivel}". Use Iniciante, Intermediário ou Avançado.`
    );
  }

  const xp = XP[nivel];
  const tempo = TEMPO[nivel];

  return [
    `# 🎯 Desafio DIO — ${tecnologia} · Nível ${nivel}`,
    "",
    "## 📋 Descrição",
    `A empresa fictícia **DataStartup Inc.** precisa de uma solução em **${tecnologia}** para`,
    `resolver um problema real de nível **${nivel}**. Você foi selecionado(a) para implementá-la.`,
    "",
    "## 🎯 Objetivos",
    `1. Implementar a solução principal usando ${tecnologia}`,
    "2. Garantir cobertura de testes adequada (mínimo 70%)",
    "3. Documentar a solução com comentários e README",
    "4. Tratar erros e casos de borda",
    "",
    "## 📥 Entrada Esperada",
    "```",
    `# Parâmetros da função principal`,
    `entrada = { "dados": [...], "configuracao": {...} }`,
    "```",
    "",
    "## 📤 Saída Esperada",
    "```",
    `{ "resultado": ..., "status": "ok", "processado_em_ms": 42 }`,
    "```",
    "",
    "## 💡 Dicas",
    `- Consulte a documentação oficial de ${tecnologia} antes de começar`,
    "- Comece pelo caso de uso mais simples e evolua incrementalmente",
    "- Use testes automatizados desde o início",
    "",
    "## 🧪 Casos de Teste",
    "| # | Entrada             | Saída esperada          |",
    "|---|---------------------|-------------------------|",
    "| 1 | Entrada válida padrão | Resultado correto     |",
    "| 2 | Entrada vazia/nula  | Erro tratado graciosamente |",
    "",
    "## 📊 Critérios de Avaliação",
    "- ✅ Correção da solução",
    "- ✅ Qualidade e legibilidade do código",
    "- ✅ Tratamento de erros",
    "- ✅ Boas práticas de engenharia de software",
    "",
    `## ⏱️ Tempo Sugerido\n  ${tempo}`,
    "",
    `## ⭐ XP ao Completar\n  **${xp} XP**`,
    "",
    "---",
    "*Desafio gerado pelo DIO IBM Bob MCP Server*",
  ].join("\n");
}

function gerarCodigo(): string {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  return Array.from({ length: 4 }, () =>
    Array.from({ length: 4 }, () =>
      chars[Math.floor(Math.random() * chars.length)]
    ).join("")
  ).join("-");
}

function gerarCertificado(nomeUsuario: string, trilha: Trilha): string {
  const dataEmissao = new Date().toLocaleDateString("pt-BR");
  const cargaHoraria = trilha.modulos * 8;
  const codigo = gerarCodigo();
  const tecnologias = trilha.tecnologia.join(" · ");
  const badgesFmt = trilha.badges.map((b) => `**${b}**`).join(" · ");
  const nomeUpper = nomeUsuario.toUpperCase();

  return [
    "---",
    "",
    "<div align='center'>",
    "",
    "# 🎓 CERTIFICADO DE CONCLUSÃO",
    "",
    "### Digital Innovation One — DIO",
    "",
    "---",
    "",
    "**Certificamos que**",
    "",
    `# ${nomeUpper}`,
    "",
    "**concluiu com êxito a trilha de aprendizado:**",
    "",
    `## ${trilha.nome}`,
    "",
    `> *${tecnologias}*`,
    "",
    "---",
    "",
    "| 📅 Conclusão | ⏱️ Carga Horária | ⭐ XP | 🎯 Nível |",
    "|---|---|---|---|",
    `| ${dataEmissao} | ${cargaHoraria}h | ${trilha.xp_total} XP | ${trilha.nivel} |`,
    "",
    "---",
    "",
    "### 🏅 Badges Conquistadas",
    badgesFmt,
    "",
    "---",
    "",
    "### 📚 Conteúdo Abordado",
    trilha.tecnologia
      .map((t, i) => `- Módulo ${i + 1}: Fundamentos e prática de ${t}`)
      .join("\n"),
    "",
    "---",
    "",
    "**Instrutor Responsável:** Prof. Ana Clara Ferreira",
    "**Plataforma:** [web.dio.me](https://web.dio.me/home)",
    "",
    "---",
    "",
    `🔑 **Código de Verificação:** \`${codigo}\``,
    "",
    "*Este certificado é fictício e foi gerado para fins educacionais pelo IBM Bob MCP Server.*",
    `*Emitido digitalmente pela plataforma DIO em ${dataEmissao}.*`,
    "",
    "</div>",
    "",
    "---",
  ].join("\n");
}

// ---------------------------------------------------------------------------
// Criação e registro do servidor MCP
// ---------------------------------------------------------------------------

function criarServidor(): McpServer {
  const server = new McpServer({
    name: "dio-bob-mcp-server",
    version: "1.0.0",
  });

  const trilhas = carregarTrilhas();

  // ── Tool 1: listar_trilhas ──────────────────────────────────────────────
  server.registerTool(
    "listar_trilhas",
    {
      description:
        "Lista todas as trilhas disponíveis no catálogo DIO com resumo (id, nome, nível, tecnologias, XP).",
      inputSchema: z.object({
        nivel: z
          .enum(["Iniciante", "Intermediário", "Avançado", "todos"])
          .default("todos")
          .describe("Filtrar por nível de dificuldade. Use 'todos' para listar todas."),
      }),
    },
    async ({ nivel }) => {
      const filtradas =
        nivel === "todos"
          ? trilhas
          : trilhas.filter((t) => t.nivel === nivel);

      if (filtradas.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: `Nenhuma trilha encontrada para o nível "${nivel}".`,
            },
          ],
        };
      }

      const linhas = filtradas.map(
        (t) =>
          `- **[${t.id}]** ${t.nome} | ${t.nivel} | ${t.xp_total} XP | ${t.tecnologia.join(", ")}`
      );

      return {
        content: [
          {
            type: "text",
            text: [
              `## 📚 Catálogo DIO — ${filtradas.length} trilha(s) encontrada(s)`,
              "",
              ...linhas,
            ].join("\n"),
          },
        ],
      };
    }
  );

  // ── Tool 2: trilha_buscar ───────────────────────────────────────────────
  server.registerTool(
    "trilha_buscar",
    {
      description:
        "Busca trilhas DIO por tecnologia ou nome. Retorna plano de estudos detalhado em Markdown.",
      inputSchema: z.object({
        tecnologia: z
          .string()
          .min(1)
          .describe(
            "Nome (ou parte do nome) da tecnologia ou trilha. Ex: 'Python', 'LangChain', 'TensorFlow'."
          ),
      }),
    },
    async ({ tecnologia }) => {
      const encontradas = buscarTrilhas(trilhas, tecnologia);

      if (encontradas.length === 0) {
        const disponiveis = [
          ...new Set(trilhas.flatMap((t) => t.tecnologia)),
        ].sort();
        return {
          content: [
            {
              type: "text",
              text: [
                `Nenhuma trilha encontrada para "${tecnologia}".`,
                "",
                "**Tecnologias disponíveis:**",
                disponiveis.map((t) => `- ${t}`).join("\n"),
              ].join("\n"),
            },
          ],
        };
      }

      if (encontradas.length === 1) {
        return {
          content: [{ type: "text", text: formatarPlano(encontradas[0]) }],
        };
      }

      // Mais de uma: lista as opções
      const opcoes = encontradas
        .map((t) => `- **[${t.id}]** ${t.nome} (${t.nivel})`)
        .join("\n");

      return {
        content: [
          {
            type: "text",
            text: [
              `Encontrei **${encontradas.length} trilhas** para "${tecnologia}". Especifique melhor ou use o ID:`,
              "",
              opcoes,
              "",
              "Use `trilha_buscar` com o nome exato para ver o plano completo.",
            ].join("\n"),
          },
        ],
      };
    }
  );

  // ── Tool 3: trilha_aleatoria ────────────────────────────────────────────
  server.registerTool(
    "trilha_aleatoria",
    {
      description:
        "Retorna uma trilha aleatória do catálogo DIO com plano de estudos completo. Ótimo para descoberta.",
      inputSchema: z.object({
        nivel: z
          .enum(["Iniciante", "Intermediário", "Avançado", "qualquer"])
          .default("qualquer")
          .describe("Nível desejado. Use 'qualquer' para sortear de todo o catálogo."),
      }),
    },
    async ({ nivel }) => {
      const pool =
        nivel === "qualquer"
          ? trilhas
          : trilhas.filter((t) => t.nivel === nivel);

      if (pool.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: `Nenhuma trilha disponível para o nível "${nivel}".`,
            },
          ],
        };
      }

      const sorteada = pool[Math.floor(Math.random() * pool.length)];
      return {
        content: [{ type: "text", text: formatarPlano(sorteada) }],
      };
    }
  );

  // ── Tool 4: desafio_gerar ───────────────────────────────────────────────
  server.registerTool(
    "desafio_gerar",
    {
      description:
        "Gera um desafio de código DIO contextualizado para uma tecnologia e nível de dificuldade.",
      inputSchema: z.object({
        tecnologia: z
          .string()
          .min(1)
          .describe("Tecnologia do desafio. Ex: 'Python', 'TensorFlow', 'LangChain'."),
        nivel: z
          .enum(["Iniciante", "Intermediário", "Avançado"])
          .describe("Nível de dificuldade do desafio."),
      }),
    },
    async ({ tecnologia, nivel }) => {
      try {
        const markdown = gerarDesafio(tecnologia, nivel);
        return { content: [{ type: "text", text: markdown }] };
      } catch (err) {
        return {
          content: [
            {
              type: "text",
              text: `Erro ao gerar desafio: ${err instanceof Error ? err.message : String(err)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  // ── Tool 5: certificado_gerar ───────────────────────────────────────────
  server.registerTool(
    "certificado_gerar",
    {
      description:
        "Emite um certificado fictício DIO de conclusão de trilha para um aluno. Retorna Markdown pronto para salvar.",
      inputSchema: z.object({
        nome_usuario: z
          .string()
          .min(2)
          .describe("Nome completo do aluno que concluiu a trilha."),
        tecnologia: z
          .string()
          .min(1)
          .describe(
            "Tecnologia ou nome da trilha concluída. Será usada para buscar a trilha no catálogo."
          ),
      }),
    },
    async ({ nome_usuario, tecnologia }) => {
      const encontradas = buscarTrilhas(trilhas, tecnologia);

      if (encontradas.length === 0) {
        return {
          content: [
            {
              type: "text",
              text: `Trilha não encontrada para "${tecnologia}". Verifique o nome e tente novamente.`,
            },
          ],
          isError: true,
        };
      }

      // Usa a trilha de melhor correspondência (primeira do resultado)
      const trilha = encontradas[0];
      const markdown = gerarCertificado(nome_usuario, trilha);

      return {
        content: [
          {
            type: "text",
            text: markdown,
          },
        ],
      };
    }
  );

  return server;
}

// ---------------------------------------------------------------------------
// Middleware de autenticação Bearer (para transporte HTTP)
// ---------------------------------------------------------------------------

function autenticar(req: IncomingMessage): boolean {
  const apiKey = process.env.API_KEY;
  if (!apiKey) return true; // sem chave configurada = servidor aberto (dev/local)

  const auth = req.headers["authorization"] ?? "";
  return auth === `Bearer ${apiKey}`;
}

// ---------------------------------------------------------------------------
// Transporte HTTP (Streamable HTTP — MCP 2025-03-26)
// ---------------------------------------------------------------------------

async function iniciarHTTP(server: McpServer, porta: number): Promise<void> {
  // Mapa de sessões ativas: sessionId → transport
  const sessoes = new Map<string, StreamableHTTPServerTransport>();

  const httpServer = createServer(async (req: IncomingMessage, res: ServerResponse) => {
    // CORS para acesso a partir de qualquer origem (ajuste em produção)
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, Mcp-Session-Id");

    if (req.method === "OPTIONS") {
      res.writeHead(204);
      res.end();
      return;
    }

    // Autenticação Bearer
    if (!autenticar(req)) {
      res.writeHead(401, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Unauthorized — forneça um Bearer token válido em Authorization." }));
      return;
    }

    const url = new URL(req.url ?? "/", `http://localhost:${porta}`);

    // Rota de health-check
    if (url.pathname === "/health") {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(
        JSON.stringify({
          status: "ok",
          server: "dio-bob-mcp-server",
          version: "1.0.0",
          sessoes_ativas: sessoes.size,
          timestamp: new Date().toISOString(),
        })
      );
      return;
    }

    if (url.pathname !== "/mcp") {
      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: `Rota não encontrada: ${url.pathname}. Use /mcp ou /health.` }));
      return;
    }

    // ── POST /mcp — nova mensagem MCP ──
    if (req.method === "POST") {
      const sessionId = req.headers["mcp-session-id"] as string | undefined;

      if (sessionId && sessoes.has(sessionId)) {
        // Sessão existente
        const transport = sessoes.get(sessionId)!;
        await transport.handleRequest(req, res);
        return;
      }

      // Nova sessão
      const novoId = randomUUID();
      const transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: () => novoId,
        onsessioninitialized: (id) => {
          sessoes.set(id, transport);
          console.error(`[MCP] Sessão iniciada: ${id} (total: ${sessoes.size})`);
        },
      });

      transport.onclose = () => {
        sessoes.delete(novoId);
        console.error(`[MCP] Sessão encerrada: ${novoId} (total: ${sessoes.size})`);
      };

      // Conecta uma nova instância do servidor a este transport
      const sessaoServer = criarServidor();
      await sessaoServer.connect(transport);
      await transport.handleRequest(req, res);
      return;
    }

    // ── GET /mcp — SSE stream (para clientes que fazem polling) ──
    if (req.method === "GET") {
      const sessionId = req.headers["mcp-session-id"] as string | undefined;
      if (!sessionId || !sessoes.has(sessionId)) {
        res.writeHead(400, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "Mcp-Session-Id inválido ou ausente." }));
        return;
      }
      const transport = sessoes.get(sessionId)!;
      await transport.handleRequest(req, res);
      return;
    }

    // ── DELETE /mcp — encerrar sessão ──
    if (req.method === "DELETE") {
      const sessionId = req.headers["mcp-session-id"] as string | undefined;
      if (sessionId && sessoes.has(sessionId)) {
        const transport = sessoes.get(sessionId)!;
        await transport.handleRequest(req, res);
        sessoes.delete(sessionId);
      } else {
        res.writeHead(404, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "Sessão não encontrada." }));
      }
      return;
    }

    res.writeHead(405, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Método não permitido." }));
  });

  httpServer.listen(porta, () => {
    console.error(
      `[MCP] dio-bob-mcp-server rodando em http://0.0.0.0:${porta}/mcp`
    );
    console.error(
      `[MCP] Health-check: http://localhost:${porta}/health`
    );
    if (!process.env.API_KEY) {
      console.error(
        "[WARN] API_KEY não definida — servidor rodando sem autenticação. Defina API_KEY para produção."
      );
    }
  });
}

// ---------------------------------------------------------------------------
// Ponto de entrada
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const modoHTTP = args.includes("--http") || process.env.MCP_TRANSPORT === "http";
  const porta = parseInt(process.env.PORT ?? "3000", 10);

  if (modoHTTP) {
    const server = criarServidor();
    await iniciarHTTP(server, porta);
  } else {
    // Modo stdio (padrão — para uso direto com Bob como subprocesso)
    const server = criarServidor();
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("[MCP] dio-bob-mcp-server rodando via stdio");
  }
}

main().catch((err) => {
  console.error("[FATAL]", err);
  process.exit(1);
});
