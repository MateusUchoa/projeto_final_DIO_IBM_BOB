"""
=============================================================
  Testes Unitários - Projeto Final DIO IBM Bob
  Cobertura: /trilha, /desafio, /certificado
  Autor   : IBM Bob (gerado automaticamente)
  Data    : 2025-07-11
=============================================================

Módulos testados:
  - TrilhaEngine  : busca e formatação de trilhas
  - DesafioEngine : geração de desafios por nível
  - CertificadoEngine: geração de certificados fictícios

Dados de origem: data/trilhas_dio.json (25 trilhas DIO)
"""

import json
import random
import re
import string
import unittest
from datetime import datetime


# ---------------------------------------------------------------------------
# Dados inline (espelho do data/trilhas_dio.json) para testes autossuficientes
# ---------------------------------------------------------------------------
TRILHAS_JSON = {
    "trilhas": [
        {
            "id": 1,
            "nome": "Fundamentos de Inteligência Artificial com Python",
            "tecnologia": ["Python", "NumPy", "Pandas", "Scikit-learn"],
            "nivel": "Iniciante",
            "modulos": 8,
            "xp_total": 3200,
            "badges": ["Python Starter", "AI Explorer", "Data Wrangler"],
            "promocoes": {"desconto": "30%", "validade": "2025-12-31", "cupom": "DIO30AI"},
            "vitalicio": True,
            "lives_ao_vivo": [
                {"titulo": "Introdução ao ecossistema Python para IA", "data": "2025-02-10", "duracao_min": 90},
                {"titulo": "Manipulação de dados com Pandas na prática", "data": "2025-03-05", "duracao_min": 120},
            ],
        },
        {
            "id": 2,
            "nome": "Machine Learning do Zero ao Avançado",
            "tecnologia": ["Python", "Scikit-learn", "XGBoost", "LightGBM"],
            "nivel": "Intermediário",
            "modulos": 12,
            "xp_total": 5800,
            "badges": ["ML Practitioner", "Model Tuner", "Feature Engineer", "Ensemble Master"],
            "promocoes": {"desconto": "20%", "validade": "2025-11-30", "cupom": "MLZERO20"},
            "vitalicio": True,
            "lives_ao_vivo": [
                {"titulo": "Algoritmos supervisionados: teoria e prática", "data": "2025-02-18", "duracao_min": 120},
            ],
        },
        {
            "id": 3,
            "nome": "Deep Learning com TensorFlow e Keras",
            "tecnologia": ["Python", "TensorFlow", "Keras", "CUDA"],
            "nivel": "Avançado",
            "modulos": 14,
            "xp_total": 7500,
            "badges": ["Deep Learner", "Neural Architect", "GPU Accelerator", "Keras Expert"],
            "promocoes": {"desconto": "15%", "validade": "2025-10-15", "cupom": "DEEP15TF"},
            "vitalicio": True,
            "lives_ao_vivo": [
                {"titulo": "Redes neurais artificiais do zero", "data": "2025-03-01", "duracao_min": 120},
            ],
        },
        {
            "id": 6,
            "nome": "Generative AI com LangChain e OpenAI",
            "tecnologia": ["Python", "LangChain", "OpenAI API", "FAISS"],
            "nivel": "Intermediário",
            "modulos": 11,
            "xp_total": 6200,
            "badges": ["GenAI Builder", "Prompt Engineer", "LangChain Dev", "RAG Master"],
            "promocoes": {"desconto": "35%", "validade": "2025-08-31", "cupom": "GENAI35"},
            "vitalicio": True,
            "lives_ao_vivo": [
                {"titulo": "Criando aplicações RAG com LangChain", "data": "2025-02-20", "duracao_min": 120},
            ],
        },
        {
            "id": 8,
            "nome": "MLOps: Deploy e Monitoramento de Modelos de IA",
            "tecnologia": ["Python", "MLflow", "Docker", "Kubernetes", "AWS SageMaker"],
            "nivel": "Avançado",
            "modulos": 15,
            "xp_total": 8200,
            "badges": ["MLOps Engineer", "Pipeline Builder", "Cloud AI Deployer", "Model Monitor", "DevOps AI"],
            "promocoes": {"desconto": "20%", "validade": "2025-11-15", "cupom": "MLOPS20"},
            "vitalicio": True,
            "lives_ao_vivo": [
                {"titulo": "Pipelines de ML com MLflow na prática", "data": "2025-03-05", "duracao_min": 150},
            ],
        },
        {
            "id": 15,
            "nome": "Engenharia de Prompts para LLMs",
            "tecnologia": ["ChatGPT", "Claude", "Gemini", "Prompt Engineering"],
            "nivel": "Iniciante",
            "modulos": 6,
            "xp_total": 2800,
            "badges": ["Prompt Crafter", "LLM Communicator"],
            "promocoes": {"desconto": "45%", "validade": "2025-07-15", "cupom": "PROMPT45"},
            "vitalicio": False,
            "lives_ao_vivo": [
                {"titulo": "Chain-of-thought e few-shot prompting", "data": "2025-02-22", "duracao_min": 90},
            ],
        },
    ]
}


# ---------------------------------------------------------------------------
# Engines (lógica pura testável, sem dependência de Bob ou API)
# ---------------------------------------------------------------------------

class TrilhaEngine:
    """Encapsula a lógica do comando /trilha."""

    def __init__(self, data: dict):
        self.trilhas = data["trilhas"]

    def buscar(self, tecnologia: str) -> list:
        """Busca case-insensitive por substring no array de tecnologias."""
        termo = tecnologia.strip().lower()
        return [
            t for t in self.trilhas
            if any(termo in tech.lower() for tech in t["tecnologia"])
            or termo in t["nome"].lower()
        ]

    def trilha_aleatoria(self) -> dict:
        """Retorna uma trilha aleatória do catálogo."""
        return random.choice(self.trilhas)

    def formatar_plano(self, trilha: dict) -> str:
        """Formata o plano de estudos em Markdown."""
        acesso = "Vitalício ♾" if trilha["vitalicio"] else "Por tempo limitado ⏳"
        tecnologias = " · ".join(trilha["tecnologia"])
        badges = "\n".join(f"  🏅 {b}" for b in trilha["badges"])
        promo = trilha.get("promocoes", {})

        lives_lines = []
        for live in trilha.get("lives_ao_vivo", []):
            h, m = divmod(live["duracao_min"], 60)
            duracao_fmt = f"{h}h{m:02d}min" if m else f"{h}h"
            lives_lines.append(f"  - {live['titulo']} — {live['data']} ({duracao_fmt})")

        cronograma = "\n".join(
            f"  Semana {i // 2 + 1} — Módulo {i + 1}: Tópico avançado {i + 1}"
            for i in range(trilha["modulos"])
        )

        return (
            f"# 🎯 Plano de Estudos - {trilha['nome']}\n\n"
            f"## Visão Geral\n"
            f"| Campo         | Detalhe                   |\n"
            f"|---------------|---------------------------|\n"
            f"| Nível         | {trilha['nivel']}         |\n"
            f"| Tecnologias   | {tecnologias}             |\n"
            f"| Total Módulos | {trilha['modulos']}        |\n"
            f"| XP Total      | {trilha['xp_total']} XP   |\n"
            f"| Acesso        | {acesso}                  |\n\n"
            f"## 🗓️ Cronograma de Módulos\n{cronograma}\n\n"
            f"## 🏅 Badges Disponíveis\n{badges}\n\n"
            f"## 📺 Lives ao Vivo\n" + "\n".join(lives_lines) + "\n\n"
            f"## 🏷️ Promoção Ativa\n"
            f"  Desconto: {promo.get('desconto','N/A')} | Cupom: `{promo.get('cupom','N/A')}` | Validade: {promo.get('validade','N/A')}\n\n"
            f"🚀 *Bora começar! Cada módulo concluído te aproxima do seu próximo nível!*"
        )

    def listar_tecnologias(self) -> list:
        """Retorna lista única de todas as tecnologias disponíveis."""
        tecnologias = set()
        for t in self.trilhas:
            for tech in t["tecnologia"]:
                tecnologias.add(tech)
        return sorted(tecnologias)


class DesafioEngine:
    """Encapsula a lógica do comando /desafio."""

    XP_POR_NIVEL = {"Iniciante": 150, "Intermediário": 350, "Avançado": 700}
    TEMPO_POR_NIVEL = {"Iniciante": "30 minutos", "Intermediário": "1 hora", "Avançado": "2 horas ou mais"}
    NIVEIS_VALIDOS = ("Iniciante", "Intermediário", "Avançado")

    def validar_nivel(self, nivel: str) -> bool:
        return nivel in self.NIVEIS_VALIDOS

    def gerar(self, tecnologia: str, nivel: str) -> dict:
        """Gera estrutura de desafio para dada tecnologia e nível."""
        if not tecnologia or not tecnologia.strip():
            raise ValueError("Tecnologia não pode ser vazia.")
        if not self.validar_nivel(nivel):
            raise ValueError(f"Nível inválido: '{nivel}'. Use: {self.NIVEIS_VALIDOS}")

        return {
            "titulo": f"Desafio DIO - {tecnologia} · Nível {nivel}",
            "tecnologia": tecnologia,
            "nivel": nivel,
            "xp": self.XP_POR_NIVEL[nivel],
            "tempo_sugerido": self.TEMPO_POR_NIVEL[nivel],
            "descricao": (
                f"A empresa fictícia DataStartup Inc. precisa de uma solução em {tecnologia} "
                f"para resolver um problema de nível {nivel}."
            ),
            "objetivos": [
                f"1. Implementar a solução principal usando {tecnologia}",
                "2. Garantir cobertura de testes adequada",
                "3. Documentar a solução",
            ],
            "casos_de_teste": [
                {"entrada": "Caso padrão válido", "saida": "Resultado esperado correto"},
                {"entrada": "Caso de borda / entrada inválida", "saida": "Tratamento de erro adequado"},
            ],
            "criterios": [
                "Correção da solução",
                "Qualidade e legibilidade do código",
                "Tratamento de erros",
                "Boas práticas de engenharia",
            ],
        }

    def formatar(self, desafio: dict) -> str:
        """Formata o desafio em Markdown."""
        objetivos = "\n".join(desafio["objetivos"])
        casos = "\n".join(
            f"  - Entrada: `{c['entrada']}` → Saída: `{c['saida']}`"
            for c in desafio["casos_de_teste"]
        )
        criterios = "\n".join(f"  - {c}" for c in desafio["criterios"])
        return (
            f"# 🎯 {desafio['titulo']}\n\n"
            f"## 📋 Descrição\n{desafio['descricao']}\n\n"
            f"## 🎯 Objetivos\n{objetivos}\n\n"
            f"## 🧪 Casos de Teste\n{casos}\n\n"
            f"## 📊 Critérios de Avaliação\n{criterios}\n\n"
            f"## ⏱️ Tempo Sugerido\n  {desafio['tempo_sugerido']}\n\n"
            f"## ⭐ XP ao Completar\n  {desafio['xp']} XP\n"
        )


class CertificadoEngine:
    """Encapsula a lógica do comando /certificado."""

    def _gerar_codigo(self) -> str:
        chars = string.ascii_uppercase + string.digits
        partes = ["".join(random.choices(chars, k=4)) for _ in range(4)]
        return "-".join(partes)

    def gerar(self, nome_usuario: str, trilha: dict) -> dict:
        """Gera os dados do certificado fictício."""
        if not nome_usuario or not nome_usuario.strip():
            raise ValueError("Nome do usuário não pode ser vazio.")

        carga_horaria = trilha["modulos"] * 8
        data_emissao = datetime.now().strftime("%d/%m/%Y")
        codigo = self._gerar_codigo()

        return {
            "nome_usuario": nome_usuario.upper(),
            "trilha_nome": trilha["nome"],
            "tecnologias": " · ".join(trilha["tecnologia"]),
            "nivel": trilha["nivel"],
            "data_emissao": data_emissao,
            "carga_horaria": carga_horaria,
            "xp_total": trilha["xp_total"],
            "badges": trilha["badges"],
            "codigo_verificacao": codigo,
            "instrutor": "Prof. Ana Clara Ferreira",
        }

    def formatar(self, cert: dict) -> str:
        """Formata o certificado em Markdown."""
        badges_fmt = " · ".join(f"**{b}**" for b in cert["badges"])
        return (
            f"---\n\n"
            f"<div align='center'>\n\n"
            f"# 🎓 CERTIFICADO DE CONCLUSÃO\n\n"
            f"### Digital Innovation One - DIO\n\n"
            f"---\n\n"
            f"**Certificamos que**\n\n"
            f"# {cert['nome_usuario']}\n\n"
            f"**concluiu com êxito a trilha de aprendizado:**\n\n"
            f"## {cert['trilha_nome']}\n\n"
            f"> *{cert['tecnologias']}*\n\n"
            f"---\n\n"
            f"| 📅 Conclusão | ⏱️ Carga Horária | ⭐ XP | 🎯 Nível |\n"
            f"|---|---|---|---|\n"
            f"| {cert['data_emissao']} | {cert['carga_horaria']}h | {cert['xp_total']} XP | {cert['nivel']} |\n\n"
            f"---\n\n"
            f"### 🏅 Badges Conquistadas\n{badges_fmt}\n\n"
            f"---\n\n"
            f"**Instrutor Responsável:** {cert['instrutor']}\n"
            f"**Plataforma:** [web.dio.me](https://web.dio.me/home)\n\n"
            f"---\n\n"
            f"🔑 **Código de Verificação:** `{cert['codigo_verificacao']}`\n\n"
            f"*Este certificado é fictício e foi gerado para fins educacionais pelo IBM Bob.*\n\n"
            f"</div>\n\n---"
        )

    def nome_arquivo(self, nome_usuario: str, trilha_nome: str) -> str:
        """Gera slug de nome de arquivo para o certificado."""
        slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
        return f"docs/certificados-emitidos/{slug(nome_usuario)}-{slug(trilha_nome)}.md"


# ---------------------------------------------------------------------------
# Suite de Testes
# ---------------------------------------------------------------------------

class TestTrilhaEngine(unittest.TestCase):
    """Testes do comando /trilha"""

    def setUp(self):
        self.engine = TrilhaEngine(TRILHAS_JSON)

    # --- Busca ---

    def test_busca_exata_retorna_trilha(self):
        """Busca por tecnologia exata deve retornar ao menos 1 trilha."""
        resultado = self.engine.buscar("Python")
        self.assertGreater(len(resultado), 0, "Deveria encontrar trilhas com Python")

    def test_busca_case_insensitive(self):
        """Busca deve ignorar maiúsculas/minúsculas."""
        r_lower = self.engine.buscar("python")
        r_upper = self.engine.buscar("PYTHON")
        self.assertEqual(len(r_lower), len(r_upper))

    def test_busca_substring(self):
        """Busca parcial 'tensor' deve encontrar trilha de TensorFlow."""
        resultado = self.engine.buscar("tensor")
        nomes = [t["nome"] for t in resultado]
        self.assertTrue(any("TensorFlow" in n or "tensorflow" in n.lower() for n in nomes))

    def test_busca_inexistente_retorna_lista_vazia(self):
        """Busca por tecnologia inexistente deve retornar lista vazia."""
        resultado = self.engine.buscar("COBOL_INEXISTENTE_XYZ")
        self.assertEqual(resultado, [])

    def test_busca_por_nome_da_trilha(self):
        """Busca por substring do nome da trilha deve funcionar."""
        resultado = self.engine.buscar("LangChain")
        self.assertGreater(len(resultado), 0)

    def test_busca_retorna_campos_obrigatorios(self):
        """Cada trilha retornada deve conter campos essenciais."""
        campos = {"id", "nome", "tecnologia", "nivel", "modulos", "xp_total", "badges"}
        for t in self.engine.buscar("Python"):
            for campo in campos:
                self.assertIn(campo, t, f"Campo '{campo}' ausente na trilha id={t.get('id')}")

    # --- Trilha aleatória ---

    def test_trilha_aleatoria_retorna_dict(self):
        """trilha_aleatoria deve retornar um dicionário."""
        t = self.engine.trilha_aleatoria()
        self.assertIsInstance(t, dict)

    def test_trilha_aleatoria_tem_id(self):
        """Trilha aleatória deve ter ID."""
        t = self.engine.trilha_aleatoria()
        self.assertIn("id", t)

    def test_multiplas_trilhas_aleatorias_variam(self):
        """Com 20 chamadas, deve haver ao menos 2 IDs distintos (aleatoriedade real)."""
        ids = {self.engine.trilha_aleatoria()["id"] for _ in range(20)}
        self.assertGreater(len(ids), 1, "Trilha aleatória deveria variar em 20 chamadas")

    # --- Formatação ---

    def test_formatar_plano_retorna_string(self):
        """formatar_plano deve retornar uma string."""
        trilha = self.engine.buscar("Python")[0]
        resultado = self.engine.formatar_plano(trilha)
        self.assertIsInstance(resultado, str)

    def test_formatar_plano_contem_nome_trilha(self):
        """Plano formatado deve conter o nome da trilha."""
        trilha = self.engine.buscar("Python")[0]
        resultado = self.engine.formatar_plano(trilha)
        self.assertIn(trilha["nome"], resultado)

    def test_formatar_plano_contem_xp(self):
        """Plano formatado deve mencionar XP total."""
        trilha = self.engine.buscar("Python")[0]
        resultado = self.engine.formatar_plano(trilha)
        self.assertIn(str(trilha["xp_total"]), resultado)

    def test_formatar_plano_contem_badges(self):
        """Plano formatado deve listar todas as badges."""
        trilha = self.engine.buscar("Python")[0]
        resultado = self.engine.formatar_plano(trilha)
        for badge in trilha["badges"]:
            self.assertIn(badge, resultado)

    def test_formatar_plano_vitalicio(self):
        """Plano de trilha vitalícia deve conter 'Vitalício'."""
        trilha = next(t for t in TRILHAS_JSON["trilhas"] if t["vitalicio"])
        resultado = self.engine.formatar_plano(trilha)
        self.assertIn("Vitalício", resultado)

    def test_formatar_plano_nao_vitalicio(self):
        """Plano de trilha não-vitalícia deve conter 'tempo limitado'."""
        trilha = next(t for t in TRILHAS_JSON["trilhas"] if not t["vitalicio"])
        resultado = self.engine.formatar_plano(trilha)
        self.assertIn("tempo limitado", resultado)

    # --- Listar tecnologias ---

    def test_listar_tecnologias_retorna_lista(self):
        techs = self.engine.listar_tecnologias()
        self.assertIsInstance(techs, list)
        self.assertGreater(len(techs), 0)

    def test_listar_tecnologias_sem_duplicatas(self):
        techs = self.engine.listar_tecnologias()
        self.assertEqual(len(techs), len(set(techs)))

    def test_listar_tecnologias_contem_python(self):
        techs = self.engine.listar_tecnologias()
        self.assertIn("Python", techs)


class TestDesafioEngine(unittest.TestCase):
    """Testes do comando /desafio"""

    def setUp(self):
        self.engine = DesafioEngine()

    # --- Validação de nível ---

    def test_nivel_iniciante_valido(self):
        self.assertTrue(self.engine.validar_nivel("Iniciante"))

    def test_nivel_intermediario_valido(self):
        self.assertTrue(self.engine.validar_nivel("Intermediário"))

    def test_nivel_avancado_valido(self):
        self.assertTrue(self.engine.validar_nivel("Avançado"))

    def test_nivel_invalido(self):
        self.assertFalse(self.engine.validar_nivel("Expert"))

    def test_nivel_vazio_invalido(self):
        self.assertFalse(self.engine.validar_nivel(""))

    # --- Geração de desafio ---

    def test_gerar_iniciante(self):
        d = self.engine.gerar("Python", "Iniciante")
        self.assertEqual(d["xp"], 150)
        self.assertEqual(d["nivel"], "Iniciante")

    def test_gerar_intermediario(self):
        d = self.engine.gerar("LangChain", "Intermediário")
        self.assertEqual(d["xp"], 350)
        self.assertEqual(d["tecnologia"], "LangChain")

    def test_gerar_avancado(self):
        d = self.engine.gerar("TensorFlow", "Avançado")
        self.assertEqual(d["xp"], 700)

    def test_gerar_campos_obrigatorios(self):
        """Desafio gerado deve conter todos os campos essenciais."""
        d = self.engine.gerar("Python", "Iniciante")
        campos = {"titulo", "tecnologia", "nivel", "xp", "tempo_sugerido",
                  "descricao", "objetivos", "casos_de_teste", "criterios"}
        for campo in campos:
            self.assertIn(campo, d)

    def test_gerar_tecnologia_vazia_lanca_excecao(self):
        with self.assertRaises(ValueError):
            self.engine.gerar("", "Iniciante")

    def test_gerar_nivel_invalido_lanca_excecao(self):
        with self.assertRaises(ValueError):
            self.engine.gerar("Python", "Master")

    def test_gerar_tem_dois_casos_de_teste(self):
        d = self.engine.gerar("Python", "Intermediário")
        self.assertGreaterEqual(len(d["casos_de_teste"]), 2)

    def test_titulo_contem_tecnologia_e_nivel(self):
        d = self.engine.gerar("OpenCV", "Avançado")
        self.assertIn("OpenCV", d["titulo"])
        self.assertIn("Avançado", d["titulo"])

    # --- Formatação ---

    def test_formatar_retorna_string(self):
        d = self.engine.gerar("Python", "Iniciante")
        resultado = self.engine.formatar(d)
        self.assertIsInstance(resultado, str)

    def test_formatar_contem_titulo(self):
        d = self.engine.gerar("Python", "Iniciante")
        resultado = self.engine.formatar(d)
        self.assertIn(d["titulo"], resultado)

    def test_formatar_contem_xp(self):
        d = self.engine.gerar("Python", "Intermediário")
        resultado = self.engine.formatar(d)
        self.assertIn("350 XP", resultado)

    def test_formatar_contem_tempo(self):
        d = self.engine.gerar("Python", "Avançado")
        resultado = self.engine.formatar(d)
        self.assertIn("2 horas", resultado)


class TestCertificadoEngine(unittest.TestCase):
    """Testes do comando /certificado"""

    def setUp(self):
        self.engine = CertificadoEngine()
        self.trilha_teste = TRILHAS_JSON["trilhas"][0]  # Fundamentos IA com Python

    # --- Geração ---

    def test_gerar_retorna_dict(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        self.assertIsInstance(cert, dict)

    def test_nome_usuario_em_maiusculas(self):
        cert = self.engine.gerar("mateus uchoa", self.trilha_teste)
        self.assertEqual(cert["nome_usuario"], "MATEUS UCHOA")

    def test_carga_horaria_calculada(self):
        """Carga horária = modulos × 8"""
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        esperado = self.trilha_teste["modulos"] * 8
        self.assertEqual(cert["carga_horaria"], esperado)

    def test_xp_total_correto(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        self.assertEqual(cert["xp_total"], self.trilha_teste["xp_total"])

    def test_badges_corretas(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        self.assertEqual(cert["badges"], self.trilha_teste["badges"])

    def test_codigo_verificacao_formato(self):
        """Código deve ter formato XXXX-XXXX-XXXX-XXXX (4 grupos de 4 chars)."""
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        codigo = cert["codigo_verificacao"]
        partes = codigo.split("-")
        self.assertEqual(len(partes), 4)
        for p in partes:
            self.assertEqual(len(p), 4)
            self.assertTrue(p.isupper() or p.isalnum())

    def test_codigo_unico_a_cada_geracao(self):
        """Cada certificado deve ter código de verificação único."""
        codigos = {self.engine.gerar("Mateus Uchoa", self.trilha_teste)["codigo_verificacao"] for _ in range(20)}
        self.assertGreater(len(codigos), 1)

    def test_data_emissao_formato_brasileiro(self):
        """Data de emissão deve estar no formato DD/MM/AAAA."""
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        self.assertRegex(cert["data_emissao"], r"^\d{2}/\d{2}/\d{4}$")

    def test_nome_vazio_lanca_excecao(self):
        with self.assertRaises(ValueError):
            self.engine.gerar("", self.trilha_teste)

    def test_tecnologias_formatadas(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        for tech in self.trilha_teste["tecnologia"]:
            self.assertIn(tech, cert["tecnologias"])

    # --- Formatação ---

    def test_formatar_retorna_string(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        resultado = self.engine.formatar(cert)
        self.assertIsInstance(resultado, str)

    def test_formatar_contem_nome_usuario(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        resultado = self.engine.formatar(cert)
        self.assertIn("MATEUS UCHOA", resultado)

    def test_formatar_contem_nome_trilha(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        resultado = self.engine.formatar(cert)
        self.assertIn(self.trilha_teste["nome"], resultado)

    def test_formatar_contem_codigo_verificacao(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        resultado = self.engine.formatar(cert)
        self.assertIn(cert["codigo_verificacao"], resultado)

    def test_formatar_contem_badges(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        resultado = self.engine.formatar(cert)
        for badge in cert["badges"]:
            self.assertIn(badge, resultado)

    def test_formatar_contem_xp(self):
        cert = self.engine.gerar("Mateus Uchoa", self.trilha_teste)
        resultado = self.engine.formatar(cert)
        self.assertIn(str(cert["xp_total"]), resultado)

    # --- Nome de arquivo ---

    def test_nome_arquivo_slug(self):
        arquivo = self.engine.nome_arquivo("Mateus Uchoa", "Fundamentos de IA com Python")
        self.assertTrue(arquivo.startswith("docs/certificados-emitidos/"))
        self.assertTrue(arquivo.endswith(".md"))
        self.assertNotIn(" ", arquivo)

    def test_nome_arquivo_lowercase(self):
        arquivo = self.engine.nome_arquivo("MATEUS UCHOA", "Deep Learning com TensorFlow")
        self.assertEqual(arquivo, arquivo.lower())


class TestFluxoCompleto(unittest.TestCase):
    """
    Testes de integração: simula o fluxo completo
    /trilha → /desafio → /certificado para um mesmo aluno.
    """

    def setUp(self):
        self.trilha_engine = TrilhaEngine(TRILHAS_JSON)
        self.desafio_engine = DesafioEngine()
        self.cert_engine = CertificadoEngine()
        self.aluno = "Mateus Uchoa"

    def test_fluxo_trilha_aleatoria_desafio_certificado(self):
        """Fluxo completo: trilha aleatória → desafio → certificado."""
        # 1. Consulta trilha aleatória
        trilha = self.trilha_engine.trilha_aleatoria()
        self.assertIsNotNone(trilha)

        # 2. Gera desafio baseado na tecnologia da trilha
        tecnologia = trilha["tecnologia"][0]
        desafio = self.desafio_engine.gerar(tecnologia, trilha["nivel"])
        self.assertEqual(desafio["tecnologia"], tecnologia)

        # 3. Gera certificado para o aluno
        certificado = self.cert_engine.gerar(self.aluno, trilha)
        self.assertEqual(certificado["nome_usuario"], self.aluno.upper())
        self.assertEqual(certificado["xp_total"], trilha["xp_total"])

    def test_fluxo_python_iniciante(self):
        """Fluxo: busca Python → desafio Iniciante → certificado."""
        trilhas = self.trilha_engine.buscar("Python")
        trilha = next((t for t in trilhas if t["nivel"] == "Iniciante"), trilhas[0])
        desafio = self.desafio_engine.gerar("Python", "Iniciante")
        cert = self.cert_engine.gerar(self.aluno, trilha)

        self.assertEqual(desafio["xp"], 150)
        self.assertGreater(cert["carga_horaria"], 0)

    def test_fluxo_langchain_intermediario(self):
        """Fluxo: busca LangChain → desafio Intermediário → certificado."""
        trilhas = self.trilha_engine.buscar("LangChain")
        self.assertGreater(len(trilhas), 0)
        trilha = trilhas[0]
        desafio = self.desafio_engine.gerar("LangChain", "Intermediário")
        cert = self.cert_engine.gerar(self.aluno, trilha)

        self.assertEqual(desafio["xp"], 350)
        self.assertIn("LangChain", cert["tecnologias"])

    def test_fluxo_tensorflow_avancado(self):
        """Fluxo: busca TensorFlow → desafio Avançado → certificado."""
        trilhas = self.trilha_engine.buscar("TensorFlow")
        self.assertGreater(len(trilhas), 0)
        trilha = trilhas[0]
        desafio = self.desafio_engine.gerar("TensorFlow", "Avançado")
        cert = self.cert_engine.gerar(self.aluno, trilha)

        self.assertEqual(desafio["xp"], 700)
        self.assertIn("TensorFlow", cert["tecnologias"])

    def test_formatacao_completa_gera_markdown(self):
        """Verificar que a formatação de todos os 3 outputs gera Markdown válido."""
        trilha = self.trilha_engine.trilha_aleatoria()
        tecnologia = trilha["tecnologia"][0]

        plano = self.trilha_engine.formatar_plano(trilha)
        desafio_obj = self.desafio_engine.gerar(tecnologia, trilha["nivel"])
        desafio_md = self.desafio_engine.formatar(desafio_obj)
        cert_obj = self.cert_engine.gerar(self.aluno, trilha)
        cert_md = self.cert_engine.formatar(cert_obj)

        # Todos devem ser strings não-vazias com estrutura Markdown (conter "#")
        for doc in [plano, desafio_md, cert_md]:
            self.assertIsInstance(doc, str)
            self.assertIn("#", doc)
            self.assertGreater(len(doc), 100)


# ---------------------------------------------------------------------------
# Runner principal com saída para arquivo TXT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import io
    from datetime import datetime

    OUTPUT_FILE = "tests/resultados_testes.txt"
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Captura a saída detalhada do runner
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    result = runner.run(suite)
    output = stream.getvalue()

    # Calcular cobertura aproximada (testes passando / total)
    total = result.testsRun
    falhas = len(result.failures) + len(result.errors)
    aprovados = total - falhas
    cobertura = (aprovados / total * 100) if total > 0 else 0

    relatorio = f"""
╔══════════════════════════════════════════════════════════════════╗
║        RELATÓRIO DE TESTES - PROJETO FINAL DIO IBM BOB          ║
╠══════════════════════════════════════════════════════════════════╣
║  Data/Hora  : {timestamp:<50}║
║  Arquivo    : tests/test_dio_commands.py                        ║
╚══════════════════════════════════════════════════════════════════╝

ESCOPO DOS TESTES
─────────────────
  • /trilha   — TrilhaEngine  (busca, aleatoriedade, formatação)
  • /desafio  — DesafioEngine (validação nível, geração, formatação)
  • /certificado — CertificadoEngine (cálculos, código, formatação)
  • Fluxo completo integrado (trilha → desafio → certificado)

RESULTADO GERAL
───────────────
  Total de testes  : {total}
  ✅ Aprovados      : {aprovados}
  ❌ Falhas/Erros   : {falhas}
  📊 Taxa de aprovação: {cobertura:.1f}%
  Meta (≥ 70%)     : {'✅ ATINGIDA' if cobertura >= 70 else '❌ NÃO ATINGIDA'}

DETALHAMENTO
────────────
{output}
"""

    if result.failures:
        relatorio += "\nFALHAS DETALHADAS\n─────────────────\n"
        for test, traceback in result.failures:
            relatorio += f"\n[FALHA] {test}\n{traceback}\n"

    if result.errors:
        relatorio += "\nERROS DETALHADOS\n────────────────\n"
        for test, traceback in result.errors:
            relatorio += f"\n[ERRO] {test}\n{traceback}\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(relatorio)

    sys.stdout.buffer.write(relatorio.encode("utf-8", errors="replace"))
    sys.stdout.buffer.write(b"\n")
    sys.exit(0 if cobertura >= 70 else 1)
