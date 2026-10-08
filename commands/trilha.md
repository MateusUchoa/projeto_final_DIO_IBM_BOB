---
name: trilha
description: Use quando o usuário digitar /trilha seguido de uma tecnologia. Lê o arquivo data/trilhas_dio.json e retorna um plano de estudos detalhado com os módulos da trilha correspondente.
metadata:
  argument-hint: "[nome da tecnologia]"
  disable-model-invocation: true
---

# /trilha — Plano de Estudos DIO

## O que este comando faz
Recebe o nome de uma tecnologia como argumento, busca a trilha correspondente em `data/trilhas_dio.json` e apresenta um plano de estudos completo e detalhado ao usuário.

## Passos de execução

### 1. Ler o arquivo de trilhas
Use `read_file` para carregar o conteúdo de `data/trilhas_dio.json`. Se o arquivo não existir no workspace, informe o usuário que ele precisa estar na pasta `data/` do projeto.

### 2. Identificar a tecnologia solicitada
Extraia o argumento passado pelo usuário após `/trilha`. Faça a busca de forma **case-insensitive** e por **substring** — por exemplo, `/trilha python` deve encontrar trilhas que contenham "Python" em qualquer campo `tecnologia`.

### 3. Verificar correspondências
- Se **nenhuma trilha** for encontrada: informe o usuário e liste as tecnologias disponíveis no arquivo.
- Se **mais de uma trilha** for encontrada: liste as opções encontradas e peça ao usuário para escolher uma usando `ask_followup_question`.
- Se **exatamente uma trilha** for encontrada: prossiga para o passo 4.

### 4. Montar e exibir o plano de estudos
Apresente o plano de estudos no seguinte formato markdown:

```
# 📚 Plano de Estudos — [nome da trilha]

## Visão Geral
| Campo         | Detalhe                        |
|---------------|--------------------------------|
| Nível         | [nivel]                        |
| Tecnologias   | [tecnologia join ", "]         |
| Total Módulos | [modulos]                      |
| XP Total      | [xp_total] XP                  |
| Acesso        | Vitalício / Por tempo limitado |

## 🏅 Badges Disponíveis
Liste cada badge como item de lista com emoji de medalha.

## 🗓️ Cronograma de Módulos
Distribua os módulos em semanas, sugerindo nomes fictícios e progressivos para cada módulo com base na tecnologia (ex: Módulo 1 — Introdução ao [tecnologia], Módulo 2 — Configuração do ambiente, etc.), indicando a semana sugerida.

## 🎥 Lives ao Vivo
Liste cada live com título, data e duração formatada (ex: 2h30min).

## 🎁 Promoção Ativa
Exiba desconto, cupom e validade se houver promoção.

## 🚀 Próximos Passos
Sugira 3 trilhas complementares com base na mesma área de tecnologia presentes no JSON.
```

### 5. Encerrar
Finalize com uma mensagem motivacional curta no estilo DIO incentivando o usuário a iniciar a trilha.
