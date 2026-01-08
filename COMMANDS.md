# COMMANDS

## Canonical Commands for Knowledge OS (Cursor)

Этот файл — **единственный источник истины** для команд.  
Если команда не описана здесь — **она не существует**.

Команды намеренно **строгие**.  
Свободная речь ≠ действие.

---

## 🧠 Общие принципы

1. Команды **явные**
2. Команды **не угадываются**
3. Любое действие → через команду
4. Без команды → только обсуждение
5. `SUGGEST` никогда ничего не записывает

---

## 🔹 EXTRACT — извлечь знание (запись)

Создаёт **knowledge block**.  
Одна команда → один файл.

### Канонические команды (internal)

```
EXTRACT conclusion
EXTRACT framework
EXTRACT checklist
EXTRACT narrative
EXTRACT metaphor
```

### Русские алиасы

- ИЗВЛЕЧЬ вывод → EXTRACT conclusion
- ИЗВЛЕЧЬ фреймворк → EXTRACT framework
- ИЗВЛЕЧЬ чеклист → EXTRACT checklist
- ИЗВЛЕЧЬ рассказ → EXTRACT narrative
- ИЗВЛЕЧЬ метафору → EXTRACT metaphor

### Эффект

- создаётся файл в `knowledge/blocks/`
- знание становится переиспользуемым

### Запрещено

- интерпретировать разговорную речь как команду
- извлекать без явной команды

### Правила нормализации

- Matching is case-insensitive
- Commands must be exact (no declension, no extra words)
- Natural language requests MUST NOT be interpreted as commands

### Неверные примеры (должны игнорироваться)

- "извлеки чеклист"
- "давай сохраним это как вывод"
- "можно сделать из этого фреймворк?"

If a command is ambiguous or malformed, the Extractor MUST ask for clarification.

---

## 🔹 MARK — отметить контент-кандидат (запись)

Создаёт **content candidate** (не текст).

### Канонические команды

```
MARK as book_chapter candidate
MARK as book_section candidate
MARK as article candidate
MARK as blog_post candidate
```

### Русские алиасы

- ОТМЕТИТЬ как главу → MARK as book_chapter candidate
- ОТМЕТИТЬ как раздел → MARK as book_section candidate
- ОТМЕТИТЬ как статью → MARK as article candidate
- ОТМЕТИТЬ как пост → MARK as blog_post candidate

### Эффект

- создаётся файл в `knowledge/candidates/`
- фиксируется намерение, не контент

---

## 🔹 ORGANIZE — навести порядок (предложение / правка)

Никогда не пишет контент.

### Канонические команды

```
ORGANIZE knowledge blocks
ORGANIZE themes
ORGANIZE duplicates
```

### Русские алиасы

- ОРГАНИЗОВАТЬ блоки → ORGANIZE knowledge blocks
- ОРГАНИЗОВАТЬ темы → ORGANIZE themes
- ОРГАНИЗОВАТЬ дубликаты → ORGANIZE duplicates

### Эффект

- предложения merge / deprecate
- правки только с подтверждением

### Правила нормализации

- Commands must be explicit and imperative
- Organizer never runs automatically on vague requests
- If scope is unclear, ask which dimension to organize

### Неверные примеры

- "наведи порядок"
- "кажется тут хаос"
- "проверь всё"

Organizer MUST propose changes, never apply destructive actions automatically.

---

## 🔹 ASSEMBLE — собрать контент (запись)

Собирает текст **ТОЛЬКО** из blocks / candidates.

### Канонические команды

```
ASSEMBLE blog
ASSEMBLE article
ASSEMBLE book
ASSEMBLE email
```

### Русские алиасы

- СОБРАТЬ пост → ASSEMBLE blog
- СОБРАТЬ статью → ASSEMBLE article
- СОБРАТЬ книгу → ASSEMBLE book
- СОБРАТЬ письмо → ASSEMBLE email

### Параметры (опционально)

- `theme:` — одна тема
- `themes:` — несколько тем
- `from: candidate` — собрать из кандидата
- `length: short | medium | long` — длина контента

### Эффект

- создаётся файл в `output/`
- добавляется Sources

### Правила нормализации

- Assembly MUST follow `knowledge/pipelines/pipeline.yaml` strictly
- Assembler may ONLY use existing blocks and candidates
- If required blocks are missing, stop and report

### Неверные примеры

- "напиши статью"
- "давай сделаем главу"
- "сгенерируй письмо"

Assembler MUST NOT invent ideas or rewrite blocks.

---

## 🔹 SUGGEST — предложить (БЕЗ записи)

Никогда не создаёт файлов.  
Используется при сомнении.

### Канонические команды

```
SUGGEST extract
SUGGEST organization
SUGGEST assembly
```

### Русские алиасы

- ПРЕДЛОЖИ извлечение → SUGGEST extract
- ПРЕДЛОЖИ организацию → SUGGEST organization
- ПРЕДЛОЖИ сборку → SUGGEST assembly
- ПРЕДЛОЖИ что извлечь → SUGGEST extract
- ПРЕДЛОЖИ порядок → SUGGEST organization
- ПРЕДЛОЖИ контент → SUGGEST assembly

### Эффект

- предложения форм
- предложения структур
- запрос подтверждения

### SUGGEST extract

**Что Extractor может предложить:**

- block type (conclusion / checklist / framework / narrative / metaphor)
- tentative filename
- primary theme
- confidence level

**Формат вывода:**

Suggestions MUST be listed explicitly, for example:

```
Suggested extractions:
1. conclusion — "jira-workflows-vs-ai-protocols"
2. framework — "executable-protocols"
3. checklist — "when-to-replace-jira"
```

**Follow-up:**

Extractor MUST ask: "Confirm EXTRACT <type> (yes/no)?"

### SUGGEST organization

**Что Organizer может предложить:**

- potential duplicates
- theme misalignment
- possible merges
- candidate promotion or deprecation

**Формат вывода:**

Suggestions MUST be non-destructive and include rationale.

### SUGGEST assembly

**Что Assembler может предложить:**

- content type (blog / article / book_chapter / email)
- suitable candidates
- missing blocks
- best pipeline

**Формат вывода:**

Suggestions MUST include:
- proposed output
- required blocks
- estimated completeness (low/medium/high)

Assembler MUST NOT assemble in SUGGEST mode.

### Правила SUGGEST mode

SUGGEST is an advisory mode.  
It MUST NOT create or modify any files.

**SUGGEST may:**
- analyze the current context
- propose block types
- propose candidate types
- suggest titles and themes

**SUGGEST must:**
- clearly label suggestions as non-persistent
- ask for explicit confirmation before any EXTRACT or MARK

If user does not confirm, nothing is written.

---

## 🔹 STATUS — управление состоянием кандидатов

### Канонические команды

```
SET status: draft
SET status: solid
SET status: used
SET status: deprecated
```

### Русские алиасы

- УСТАНОВИТЬ статус: draft → SET status: draft
- УСТАНОВИТЬ статус: solid → SET status: solid
- УСТАНОВИТЬ статус: used → SET status: used
- УСТАНОВИТЬ статус: deprecated → SET status: deprecated

---

## 🔐 Глобальные правила

- ❌ Команды в свободной форме игнорируются
- ❌ Вопрос ≠ команда
- ❌ Вежливость ≠ действие
- ✅ Только формы из этого файла
- ✅ Строгость — это фича

---

## 🧩 Золотое правило

> **Сомневаешься → SUGGEST  
> Решил → EXTRACT / MARK / ASSEMBLE**

Если команда не написана — ничего не происходит.


## 🔹 SEARCH — поиск по архиву ChatGPT (read-only)

Поиск по экспортированным чатам ChatGPT  
с автоматической FTS5-индексацией при необходимости.

SEARCH **никогда не создаёт knowledge blocks**.  
Он только находит сырьё для последующего `SUGGEST` / `EXTRACT`.

---

### Каноническая команда (internal)

```
SEARCH archive
```

### Поддерживаемые параметры

```
export_path=<path/to/conversations.json>  # обязательно при первом запуске
query="<fts query>"                       # обязательно
limit=<int>                               # опционально, default 20
reindex=<true|false>                      # опционально, default false
```

**Пример:**
```
SEARCH archive export_path=/Users/me/Downloads/conversations.json query="jira NEAR/5 workflow" limit=20
```

### Русские алиасы

- ПОИСК архив → SEARCH archive
- НАЙТИ в архиве → SEARCH archive

---

### Поведение команды

1. Проверяет наличие индекса:
   - `index/chats.sqlite`
2. Если индекс отсутствует или устарел:
   - автоматически запускает ingest (FTS5)
3. Выполняет поиск по FTS5
4. Возвращает:
   - отсортированные результаты
   - conversation_id
   - короткий snippet
   - подсказки следующих шагов

---

### Разрешённые действия
- Создание / обновление:
  - `index/chats.sqlite`
  - `archive/normalized/*`
- Чтение `conversations.json`

---

### Запрещённые действия
- ❌ Изменять `knowledge/blocks/`
- ❌ Создавать candidates
- ❌ Запускать EXTRACT автоматически
- ❌ Сохранять результаты поиска

---

### Типовой workflow

```
SEARCH archive ...
↓
(просмотр результатов)
↓
python3 tools/extract_snippet.py --id <conversation_id>
↓
SUGGEST extract
↓
ИЗВЛЕЧЬ вывод / чеклист / фреймворк
```

---

### Подсказки по запросам (FTS5)
- Точная фраза:
  `"executable protocols"`
- Логика:
  `jira OR confluence`
- Близость:
  `jira NEAR/5 workflow`
- Исключение:
  `jira NOT datacenter`

---

### Гарантии
- SEARCH безопасен
- SEARCH обратим
- SEARCH не загрязняет knowledge base

Если есть сомнение — использовать SEARCH, а не EXTRACT.