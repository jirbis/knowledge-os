# knowledge/blocks/checklists/repository-readiness-knowledge-os.md

---
type: checklist
themes:
  - knowledge-os
  - automation
confidence: high
reuse:
  - blog
  - book
  - consulting
source: chat
tags:
  - checklist
  - repository
  - cursor
  - agents
  - workflow
---

## Repository Readiness Checklist — Knowledge OS

### Базовая структура
- README.md существует
- AGENTS.md существует
- COMMANDS.md существует
- Папка `knowledge/` создана
- В `knowledge/` есть: blocks / candidates / pipelines

### Агенты
- Есть AGENTS/Extractor.md
- Есть AGENTS/Organizer.md
- Есть AGENTS/Assembler.md
- В каждом агенте есть `Command normalization`
- В каждом агенте описан `SUGGEST` режим

### Командная дисциплина
- Все команды определены в COMMANDS.md
- Русские алиасы задокументированы
- Нет “скрытых” или устных команд
- Разговорная речь не вызывает действий

### Knowledge blocks
- 1 файл = 1 идея
- Нет дат в именах файлов
- Есть frontmatter
- Указан type
- Есть минимум 1 theme
- Указан reuse
- Блок читаем вне контекста

### Content candidates
- Папка `knowledge/candidates/` существует
- Есть хотя бы один candidate
- Candidate не дублирует blocks
- Есть status
- Есть source_blocks
- Ясно, чем кандидат может стать (глава / статья / пост)

### Pipelines
- `knowledge/pipelines/pipeline.yaml` существует
- Описаны blog / book / email
- Есть min_confidence
- Есть reuse_must_include
- Ассемблер ограничен правилами pipeline

### Output
- Папка `output/` существует
- Output не редактируется вручную
- В output есть секция Sources
- Sources указывают на blocks / candidates

### SUGGEST режим
- `ПРЕДЛОЖИ извлечение` не создаёт файлов
- `ПРЕДЛОЖИ сборку` не создаёт output
- После SUGGEST требуется явное подтверждение
- Без команды ничего не происходит

### Git и обратимость
- Репозиторий под git
- Коммиты маленькие и осмысленные
- Любое действие можно откатить
- Нет изменений без коммита

### Финальный тест
- Понятно, какие идеи существуют
- Понятно, что из них — кандидаты
- Видно, что уже использовано
- Можно быстро собрать контент без генерации заново
