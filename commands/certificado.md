---
name: certificado
description: Use quando o usuário digitar /certificado. Gera um certificado fictício de conclusão em formato markdown com o nome do usuário e a trilha concluída, no estilo DIO.
metadata:
  argument-hint: "[seu nome] | [nome da trilha]"
  disable-model-invocation: true
---

# /certificado — Gerador de Certificado DIO

## O que este comando faz
Recebe o nome do usuário e o nome (ou tecnologia) de uma trilha concluída, e gera um certificado fictício de conclusão em markdown formatado no estilo da plataforma DIO.

## Passos de execução

### 1. Coletar nome do usuário e trilha
Extraia do argumento do usuário:
- **Nome completo** do usuário
- **Nome ou tecnologia** da trilha concluída

Se algum dos dois estiver ausente, use `ask_followup_question` para coletar o dado faltante.

### 2. Buscar a trilha no JSON
Use `read_file` para carregar `data/trilhas_dio.json` e localizar a trilha pelo nome ou tecnologia (busca case-insensitive por substring). Se mais de uma for encontrada, peça ao usuário que escolha com `ask_followup_question`.

### 3. Gerar dados do certificado
Calcule ou gere os seguintes dados para compor o certificado:
- **Data de emissão**: data atual formatada como DD/MM/AAAA
- **Código de verificação**: string fictícia alfanumérica de 16 caracteres em maiúsculas separada por hífens a cada 4 caracteres (ex: `A3F2-K9LM-7TQX-B6WZ`)
- **Carga horária**: calcule como `modulos × 8 horas` da trilha encontrada
- **XP conquistado**: valor `xp_total` da trilha
- **Badges conquistadas**: lista todas as badges da trilha
- **Instrutor fictício**: gere um nome de instrutor fictício plausível

### 4. Gerar e exibir o certificado no seguinte formato markdown

```markdown
---

<div align="center">

# 🎓 CERTIFICADO DE CONCLUSÃO

### Digital Innovation One — DIO

---

**Certificamos que**

# [NOME COMPLETO DO USUÁRIO EM MAIÚSCULAS]

**concluiu com êxito a trilha de aprendizado:**

## [Nome da Trilha]

> *[Tecnologias da trilha separadas por " · "]*

---

| 📅 Data de Conclusão | ⏱️ Carga Horária | 🏆 XP Conquistado | 📊 Nível |
|---|---|---|---|
| [data de emissão] | [carga horária]h | [xp_total] XP | [nivel] |

---

### 🏅 Badges Conquistadas
[lista de badges como badges inline formatadas em negrito separadas por espaço]

---

### Conteúdo Abordado
[Lista com bullet points dos módulos sugeridos da trilha, no mínimo 5 tópicos gerados com base nas tecnologias]

---

**Instrutor Responsável:** [Nome do instrutor fictício]
**Plataforma:** [web.dio.me](https://web.dio.me/home)
**Trilha:** [Nome da Trilha]

---

🔐 **Código de Verificação:** `[XXXX-XXXX-XXXX-XXXX]`

*Este certificado é fictício e foi gerado para fins educacionais pelo IBM Bob.*
*Emitido digitalmente pela plataforma DIO em [data de emissão].*

</div>

---
```

### 5. Salvar o certificado (opcional)
Após exibir, pergunte ao usuário com `ask_followup_question` se deseja salvar o certificado como arquivo `.md` em `docs/certificados-emitidos/[nome-usuario]-[slug-trilha].md`. Se sim, use `write_file` para criar o arquivo (substitua espaços por hífens em minúsculas no nome do arquivo).

### 6. Encerrar
Parabenize o usuário pela conclusão da trilha com uma mensagem motivacional curta no estilo DIO.
