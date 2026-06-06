# Changelog

## [2.0.0] — 2026-06-06

### Переписан с нуля

- Миграция с Python (aiogram + SQLite) на TypeScript + Deno + Grammy
- База данных переехала с SQLite на Supabase PostgreSQL
- Хостинг переехал на Supabase Edge Functions (serverless, webhook-based)
- Секреты вынесены из кода в Supabase Secrets
- Поле `date` (TEXT) заменено на `created_at` (timestamptz)

## [1.0.0] — 2026-06-03

### Первоначальная версия (Python)

- Telegram бот на aiogram 3.7.0
- SQLite база данных (requests.db)
- Приём заявок на совместный блог
- Уведомление создателя о новых заявках
- Просмотр всех заявок для создателя
