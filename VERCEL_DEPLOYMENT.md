# 🚀 Развертывание на Vercel - Пошаговая инструкция

## 📋 Что нужно сделать

### 1. Создание проекта на Vercel

1. **Перейдите на [vercel.com](https://vercel.com)**
2. **Войдите в аккаунт** (или зарегистрируйтесь)
3. **Нажмите "New Project"**
4. **Импортируйте репозиторий** `ahmed11551/gamecoinsapp`

### 2. Настройки проекта

**Framework Preset**: `Other`  
**Root Directory**: `./`  
**Build Command**: `pip install -r requirements.txt`  
**Output Directory**: `./`  
**Install Command**: `pip install -r requirements.txt`

### 3. Переменные окружения

В разделе "Environment Variables" добавьте:

```env
BOT_TOKEN=your_bot_token_from_botfather
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port/0
SECRET_KEY=your-secret-key-here
ADMIN_USER_IDS=your_telegram_id
WEBHOOK_URL=https://your-project.vercel.app
WEBHOOK_PATH=/webhook
```

### 4. Развертывание

Нажмите **"Deploy"** и дождитесь завершения.

## 🤖 Настройка Telegram бота

### 1. Создание бота

1. **Откройте Telegram** и найдите [@BotFather](https://t.me/botfather)
2. **Отправьте команду** `/newbot`
3. **Введите имя бота**: `Tournament Platform Bot`
4. **Введите username**: `your_tournament_bot` (должен заканчиваться на `bot`)
5. **Скопируйте токен** бота

### 2. Настройка webhook

После развертывания на Vercel получите URL вашего проекта и установите webhook:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-project.vercel.app/webhook"}'
```

### 3. Проверка webhook

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

## 🗄️ Настройка базы данных

### Рекомендуемые сервисы:

#### PostgreSQL:
- **[Supabase](https://supabase.com)** - бесплатно до 500MB
- **[Neon](https://neon.tech)** - бесплатно до 3GB
- **[PlanetScale](https://planetscale.com)** - бесплатно до 1GB

#### Redis:
- **[Upstash](https://upstash.com)** - бесплатно до 10K запросов/день
- **[Redis Cloud](https://redis.com/redis-enterprise-cloud/)** - бесплатно до 30MB

## 🔧 Настройка переменных окружения

### В Vercel Dashboard:

1. **Перейдите в Settings → Environment Variables**
2. **Добавьте переменные**:

```env
# Telegram Bot
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Database
DATABASE_URL=postgresql://postgres:password@db.supabase.co:5432/postgres
REDIS_URL=redis://default:password@redis.upstash.io:6379

# Security
SECRET_KEY=your-super-secret-key-here
ADMIN_USER_IDS=123456789

# Webhook
WEBHOOK_URL=https://your-project.vercel.app
WEBHOOK_PATH=/webhook

# Payment Systems (опционально)
TELEGRAM_STARS_API_KEY=your_telegram_stars_api_key
YOO_KASSA_SHOP_ID=your_yookassa_shop_id
YOO_KASSA_SECRET_KEY=your_yookassa_secret_key
```

## 🎮 Тестирование

### 1. Проверка бота

1. **Найдите вашего бота** в Telegram по username
2. **Отправьте команду** `/start`
3. **Проверьте ответ** бота

### 2. Проверка веб-интерфейса

1. **Откройте** `https://your-project.vercel.app/`
2. **Проверьте** загрузку главной страницы
3. **Протестируйте** игры

### 3. Проверка логов

1. **Перейдите в Vercel Dashboard**
2. **Откройте Functions**
3. **Проверьте логи** выполнения

## 🚨 Возможные проблемы

### Проблема: Бот не отвечает
**Решение**: Проверьте webhook и токен бота

### Проблема: Ошибка базы данных
**Решение**: Проверьте DATABASE_URL и подключение

### Проблема: Ошибка Redis
**Решение**: Проверьте REDIS_URL и подключение

### Проблема: Ошибка развертывания
**Решение**: Проверьте requirements.txt и переменные окружения

## 📊 Мониторинг

### В Vercel Dashboard:
- **Analytics** - статистика посещений
- **Functions** - логи выполнения
- **Deployments** - история развертываний

### Логи бота:
- Доступны в Vercel Functions
- Можно настроить внешний мониторинг

## 🔄 Автоматическое развертывание

После настройки каждое изменение в GitHub будет автоматически развертываться на Vercel.

### Workflow:
1. Вносите изменения в код
2. Коммитите и пушите в GitHub
3. Vercel автоматически развернет обновления

---

**🎉 После выполнения всех шагов ваша турнирная платформа будет работать в продакшене!**
