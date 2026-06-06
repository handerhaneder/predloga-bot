# Архитектура предлога-бот

## Стек

| Слой | Технология |
|---|---|
| Язык | TypeScript + Deno |
| Бот-фреймворк | Grammy 1.34 |
| Хостинг | Supabase Edge Functions |
| База данных | Supabase PostgreSQL |

## Структура проекта

```
predloga-bot/
├── supabase/
│   ├── functions/
│   │   └── telegram-bot/
│   │       ├── index.ts     # Webhook entry point
│   │       ├── bot.ts       # Grammy роутинг и хэндлеры
│   │       └── db.ts        # Запросы к Supabase
│   └── migrations/
│       └── 20260606000000_create_requests.sql
├── docs/
│   ├── ARCHITECTURE.md
│   └── BACKLOG.md
├── CHANGELOG.md
├── CLAUDE.md
├── .env.example
└── .gitignore
```

## Поток данных

```
Telegram → POST webhook → Edge Function (index.ts)
                               ↓
                          Grammy (bot.ts)
                         ↙           ↘
              addRequest()        getAllRequests()
                  ↓                     ↓
           Supabase INSERT         Supabase SELECT
                               ↓
                      Ответ пользователю
```

## База данных

```sql
requests (
  id          bigint  PK autoincrement
  user_id     bigint  NOT NULL
  full_name   text
  username    text
  created_at  timestamptz  DEFAULT now()
)
```

## Переменные окружения

| Переменная | Откуда | Описание |
|---|---|---|
| `BOT_TOKEN` | Supabase Secrets | Токен бота от @BotFather |
| `CREATOR_ID` | Supabase Secrets | Telegram ID создателя |
| `SUPABASE_URL` | Авто (Edge Functions) | URL проекта |
| `SUPABASE_SERVICE_ROLE_KEY` | Авто (Edge Functions) | Service role ключ |

## Деплой

```bash
supabase link --project-ref pxbaslzsumuyvahdkspv
supabase db push
supabase secrets set BOT_TOKEN=... CREATOR_ID=...
supabase functions deploy telegram-bot
```

Webhook регистрируется через Telegram Bot API:
```
POST https://api.telegram.org/bot<TOKEN>/setWebhook
body: { url: "https://pxbaslzsumuyvahdkspv.supabase.co/functions/v1/telegram-bot" }
```
