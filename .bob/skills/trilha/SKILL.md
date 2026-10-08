---
name: trilha
description: Use quando o usuário digitar /trilha seguido de uma tecnologia. Lê o arquivo data/trilhas_dio.json e retorna um plano de estudos detalhado com os módulos da trilha correspondente.
metadata:
  argument-hint: "[nome da tecnologia]"
  disable-model-invocation: true
---

# /trilha — Plano de Estudos DIO

## O que este comando faz
Recebe o nome de uma tecnologia como argumento, busca a trilha correspondente em `data/trilhas_dio.json` e apresenta um plano de estudos completo e formatado.

## Passos de execução

### 1. Ler o arquivo de trilhas
Use `read_file` para carregar o conteúdo de `data/trilhas_dio.json`. Se o arquivo não existir, informe o usuário.

### 2. Identificar a tecnologia solicitada
Extraia o argumento passado pelo usuário após `/trilha`. Faça a busca de forma **case-insensitive** e por **substring** — `/trilha python` deve encontrar trilhas que contenham "Python" em qualquer elemento do array `tecnologia`.

### 3. Verificar correspondências
- **Nenhuma trilha encontrada**: informe e liste as tecnologias disponíveis no arquivo.
- **Mais de uma trilha encontrada**: use `ask_followup_question` para o usuário escolher.
- **Exatamente uma trilha**: prossiga para o passo 4.

### 4. Montar e exibir o plano de estudos

Apresente no seguinte formato:

```
# 📚 Plano de Estudos — [nome da trilha]

## Visão Geral
| Campo         | Detalhe                              |
|---------------|--------------------------------------|
| Nível         | [nivel]                              |
| Tecnologias   | [tecnologias separadas por " · "]    |
| Total Módulos | [modulos]                            |
| XP Total      | [xp_total] XP                        |
| Acesso        | Vitalício ✅ ou Por tempo limitado ⏳ |

## 🗓️ Cronograma de Módulos
Distribua os [modulos] módulos em semanas. Gere nomes fictícios e progressivos para cada módulo com base nas tecnologias da trilha (ex: Módulo 1 — Introdução ao ambiente, Módulo 2 — Configuração e setup, etc.), indicando a semana sugerida.

## 🏅 Badges Disponíveis
Liste cada badge como item com emoji de medalha 🥇.

## 🎥 Lives ao Vivo
Para cada live: título, data formatada (DD/MM/AAAA) e duração em horas/minutos.

## 🎁 Promoção Ativa
Desconto, cupom de desconto e validade.

## 🚀 Trilhas Complementares
Sugira 3 trilhas do mesmo JSON que usem tecnologias relacionadas.
```

### 5. Encerrar
Finalize com uma mensagem motivacional curta no estilo DIO incentivando o usuário a iniciar a trilha.
