# 🚀 Автоматическое развертывание на Vercel

## 📋 Инструкция по развертыванию

### 1. Создание проекта с новым именем

Поскольку проект «skill-games-platform» уже существует, используйте одно из этих имен:

**Рекомендуемые имена:**
- `tournament-platform-2024`
- `telegram-games-bot`
- `skill-tournament-app`
- `games-platform-bot`
- `tournament-bot-v2`

### 2. Развертывание через Vercel CLI

```bash
# Установка Vercel CLI (если не установлен)
npm i -g vercel

# Логин в Vercel
vercel login

# Развертывание с новым именем
vercel --name tournament-platform-2024
```

### 3. Настройка переменных окружения

После развертывания добавьте переменные в Vercel Dashboard:

```env
BOT_TOKEN=your_bot_token_from_botfather
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port/0
SECRET_KEY=your-secret-key-here
ADMIN_USER_IDS=your_telegram_id
WEBHOOK_URL=https://tournament-platform-2024.vercel.app
WEBHOOK_PATH=/webhook
```

### 4. Настройка Telegram webhook

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://tournament-platform-2024.vercel.app/webhook"}'
```

## 🎯 Результат

После развертывания у вас будет:
- ✅ Работающий Telegram бот
- ✅ Веб-интерфейс для игр
- ✅ Автоматические турниры
- ✅ Платежная система
- ✅ Система рейтингов
- ✅ Анти-чит защита

---

**🎉 Проект готов к развертыванию с новым именем!**
