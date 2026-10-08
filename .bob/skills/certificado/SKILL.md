---
name: certificado
description: Use quando o usuário digitar /certificado. Gera um certificado fictício de conclusão em markdown com o nome do usuário e a trilha concluída, no estilo DIO.
metadata:
  argument-hint: "[seu nome] | [nome da trilha]"
  disable-model-invocation: true
---

# /certificado — Gerador de Certificado DIO

## O que este comando faz
Recebe o nome do usuário e o nome (ou tecnologia) de uma trilha concluída, e gera um certificado fictício de conclusão em markdown no estilo da plataforma DIO.

## Passos de execução

### 1. Coletar nome do usuário e trilha
Extraia do argumento do usuário:
- **Nome completo** do usuário
- **Nome ou tecnologia** da trilha concluída

Se algum dado estiver ausente, use `ask_followup_question`.

### 2. Buscar a trilha no JSON
Use `read_file` para carregar `data/trilhas_dio.json`. Localize a trilha pelo nome ou tecnologia (busca case-insensitive por substring). Se mais de uma for encontrada, use `ask_followup_question` para o usuário escolher.

### 3. Calcular dados do certificado
- **Data de emissão**: data atual no formato DD/MM/AAAA
- **Código de verificação**: string fictícia alfanumérica de 16 caracteres em maiúsculas, separada por hífens a cada 4 (ex: `A3F2-K9LM-7TQX-B6WZ`)
- **Carga horária**: `modulos × 8` horas
- **XP conquistado**: valor `xp_total` da trilha
- **Badges**: lista todas as badges da trilha
- **Instrutor fictício**: gere um nome de instrutor plausível

### 4. Exibir o certificado no seguinte formato

```markdown
---

<div align="center">

# 🎓 CERTIFICADO DE CONCLUSÃO

### Digital Innovation One — DIO

---

**Certificamos que**

# [NOME COMPLETO EM MAIÚSCULAS]

**concluiu com êxito a trilha de aprendizado:**

## [Nome da Trilha]

> *[Tecnologias separadas por " · "]*

---

| 📅 Conclusão     | ⏱️ Carga Horária | 🏆 XP         | 📊 Nível  |
|------------------|-----------------|---------------|-----------|
| [DD/MM/AAAA]     | [N]h            | [xp_total] XP | [nivel]   |

---

### 🏅 Badges Conquistadas
**[badge1]** · **[badge2]** · **[badge3]** ...

---

### 📖 Conteúdo Abordado
Gere uma lista com bullet points de pelo menos 5 tópicos que descrevem o conteúdo coberto na trilha, com base nas tecnologias e no nome da trilha.

---

**Instrutor Responsável:** [Nome fictício]
**Plataforma:** [web.dio.me](https://web.dio.me/home)

---

🔐 **Código de Verificação:** `[XXXX-XXXX-XXXX-XXXX]`

*Este certificado é fictício e foi gerado para fins educacionais pelo IBM Bob.*
*Emitido digitalmente pela plataforma DIO em [DD/MM/AAAA].*

</div>

---
```

### 5. Oferecer salvar o certificado
Após exibir, use `ask_followup_question` perguntando se o usuário deseja salvar o certificado como arquivo `.md` em `docs/certificados-emitidos/`. Se sim, use `write_file` para criar o arquivo com o caminho `docs/certificados-emitidos/[nome-usuario-slug]-[trilha-slug].md` (espaços substituídos por hífens, tudo em minúsculas).

### 6. Encerrar
Parabenize o usuário com uma mensagem motivacional curta no estilo DIO.
