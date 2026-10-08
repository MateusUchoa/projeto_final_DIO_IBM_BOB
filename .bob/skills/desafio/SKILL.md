---
name: desafio
description: Use quando o usuário digitar /desafio. Gera um desafio de código aleatório e contextualizado com base no nível (Iniciante, Intermediário ou Avançado) e na tecnologia escolhida pelo usuário.
metadata:
  argument-hint: "[tecnologia] [nível]"
  disable-model-invocation: true
---

# /desafio — Gerador de Desafio de Código DIO

## O que este comando faz
Recebe tecnologia e nível de dificuldade e gera um desafio de código completo no estilo dos projetos práticos da DIO.

## Passos de execução

### 1. Coletar tecnologia e nível
Extraia do argumento do usuário:
- **Tecnologia**: ex: Python, TensorFlow, LangChain, OpenCV
- **Nível**: Iniciante | Intermediário | Avançado

Se algum dado estiver ausente, use `ask_followup_question`. Ofereça sugestões com base nas tecnologias presentes em `data/trilhas_dio.json` (use `read_file` para carregar o arquivo).

### 2. Definir complexidade conforme o nível

**Iniciante:**
- Problema simples e delimitado, 1 função ou script curto
- Foco em sintaxe, estruturas básicas e lógica simples
- Entrada e saída claramente definidas

**Intermediário:**
- Múltiplas etapas ou componentes
- Exige conhecimento de bibliotecas e algoritmos específicos
- Pelo menos um caso de borda a tratar

**Avançado:**
- Cenário real de produção com arquitetura de solução
- Uso de múltiplas tecnologias ou otimização
- Inclui requisitos não-funcionais (performance, escalabilidade)

### 3. Apresentar o desafio no seguinte formato

```
# ⚔️ Desafio DIO — [tecnologia] · Nível [nivel]

## 📋 Descrição
[Cenário fictício de empresa/produto contextualizando o problema]

## 🎯 Objetivos
Lista numerada com os requisitos funcionais.

## 📥 Entrada Esperada
Formato de entrada (dados, parâmetros, arquivos, etc.)

## 📤 Saída Esperada
Formato de saída com exemplo concreto.

## 💡 Dicas
2 ou 3 dicas técnicas sem entregar a solução.

## 🧪 Casos de Teste
Pelo menos 2 casos com entrada e saída esperada.

## 🏆 Critérios de Avaliação
- Correção da solução
- Qualidade e legibilidade do código
- Tratamento de erros
- [critério adicional relevante ao nível]

## ⏱️ Tempo Sugerido
Iniciante → 30min | Intermediário → 1h | Avançado → 2h+

## 🎖️ XP ao Completar
Iniciante → 150 XP | Intermediário → 350 XP | Avançado → 700 XP
```

### 4. Encerrar
Pergunte ao usuário com `ask_followup_question` se deseja ver uma solução de referência ou gerar um novo desafio de mesmo nível e tecnologia.
