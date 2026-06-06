# Правила для Claude в этом проекте

## Git и GitHub
- После каждого изменения кода: `git add`, `git commit` с понятным сообщением, `git push`
- Формат коммита: `type: описание` (feat, fix, docs, refactor, chore)
- Никогда не коммитить `.env` и секреты — они в `.gitignore`

## Документация — поддерживать актуальной
- `CHANGELOG.md` — обновлять при каждом изменении (новый раздел сверху)
- `docs/BACKLOG.md` — отмечать задачи выполненными, добавлять новые
- `docs/ARCHITECTURE.md` — обновлять при изменении структуры проекта

## Проект
- Стек: TypeScript + Deno, Grammy, Supabase Edge Functions + PostgreSQL
- Секреты хранятся в Supabase Secrets (`BOT_TOKEN`, `CREATOR_ID`)
- `SUPABASE_URL` и `SUPABASE_SERVICE_ROLE_KEY` инжектируются автоматически в Edge Functions
- Перед деплоем: `supabase link --project-ref pxbaslzsumuyvahdkspv`
