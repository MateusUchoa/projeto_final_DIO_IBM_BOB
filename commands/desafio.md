---
name: desafio
description: Use quando o usuário digitar /desafio. Gera um desafio de código aleatório e contextualizado com base no nível (Iniciante, Intermediário ou Avançado) e na tecnologia escolhida pelo usuário.
metadata:
  argument-hint: "[tecnologia] [nível]"
  disable-model-invocation: true
---

# /desafio — Gerador de Desafio de Código DIO

## O que este comando faz
Recebe uma tecnologia e um nível de dificuldade, e gera um desafio de código completo, contextualizado e desafiador no estilo dos projetos práticos da DIO.

## Passos de execução

### 1. Coletar tecnologia e nível
Extraia do argumento do usuário:
- **Tecnologia**: ex: Python, TensorFlow, LangChain, OpenCV, etc.
- **Nível**: Iniciante | Intermediário | Avançado

Se algum dos dois estiver ausente, use `ask_followup_question` para coletar o dado faltante. Ofereça sugestões com base nas tecnologias presentes em `data/trilhas_dio.json`.

### 2. Ler o arquivo de trilhas
Use `read_file` para carregar `data/trilhas_dio.json` e encontrar uma trilha que use a tecnologia solicitada no nível indicado, para contextualizar o desafio.

### 3. Gerar o desafio
Crie um desafio único e criativo seguindo as diretrizes abaixo conforme o nível:

**Iniciante:**
- Problema simples, bem delimitado, com 1 função ou script pequeno
- Foco em sintaxe, estruturas básicas e lógica simples
- Entrada e saída claramente definidas

**Intermediário:**
- Problema com múltiplas etapas ou componentes
- Exige conhecimento de bibliotecas, APIs ou algoritmos específicos
- Deve ter pelo menos um caso de borda a tratar

**Avançado:**
- Problema complexo, próximo de um cenário real de produção
- Exige arquitetura de solução, otimização ou uso de múltiplas tecnologias
- Inclui requisitos não-funcionais (performance, escalabilidade, etc.)

### 4. Apresentar o desafio no seguinte formato

```
# ⚔️ Desafio DIO — [tecnologia] · Nível [nivel]

## 📋 Descrição
[Descrição clara e contextualizada do problema, com cenário fictício de empresa/produto]

## 🎯 Objetivos
Lista numerada com os requisitos funcionais do desafio.

## 📥 Entrada Esperada
Descreva o formato de entrada (dados, parâmetros, arquivos, etc.)

## 📤 Saída Esperada
Descreva o formato de saída esperado com exemplo concreto.

## 💡 Dicas
2 ou 3 dicas técnicas relevantes sem entregar a solução.

## 🧪 Casos de Teste
Pelo menos 2 casos de teste com entrada e saída esperada.

## 🏆 Critérios de Avaliação
- Correção da solução
- Qualidade do código (legibilidade, boas práticas)
- Tratamento de erros
- [critério adicional relevante ao nível]

## ⏱️ Tempo Sugerido
[Tempo estimado conforme o nível: Iniciante 30min | Intermediário 1h | Avançado 2h+]

## 🎖️ XP ao Completar
[XP fictício proporcional ao nível: Iniciante 150XP | Intermediário 350XP | Avançado 700XP]
```

### 5. Encerrar
Pergunte ao usuário se deseja ver uma solução de referência ou um novo desafio de mesmo nível e tecnologia.
