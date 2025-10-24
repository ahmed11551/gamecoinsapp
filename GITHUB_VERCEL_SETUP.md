# 🚀 Инструкция по развертыванию на GitHub и Vercel

## 📋 Шаги для добавления на GitHub

### 1. Инициализация Git репозитория
```bash
git init
git add .
git commit -m "Initial commit: Tournament platform MVP"
```

### 2. Создание репозитория на GitHub
1. Перейдите на [github.com](https://github.com)
2. Нажмите "New repository"
3. Название: `tournament-platform-telegram`
4. Описание: `Легальная турнирная платформа в Telegram для игр на навыки`
5. Выберите "Public" или "Private"
6. НЕ добавляйте README, .gitignore, лицензию (они уже есть)

### 3. Подключение к GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/tournament-platform-telegram.git
git branch -M main
git push -u origin main
```

## 🌐 Развертывание на Vercel

### 1. Подготовка для Vercel
Проект уже настроен для Vercel:
- ✅ `vercel.json` - конфигурация Vercel
- ✅ `web_app.py` - Flask приложение для веб-интерфейса
- ✅ `requirements.txt` - зависимости Python
- ✅ HTML шаблоны для игр

### 2. Развертывание через Vercel CLI
```bash
# Установка Vercel CLI
npm i -g vercel

# Логин в Vercel
vercel login

# Развертывание
vercel

# Продакшен развертывание
vercel --prod
```

### 3. Развертывание через веб-интерфейс Vercel
1. Перейдите на [vercel.com](https://vercel.com)
2. Нажмите "New Project"
3. Импортируйте репозиторий с GitHub
4. Настройки:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: ./
5. Добавьте переменные окружения:
   ```
   BOT_TOKEN=your_bot_token
   DATABASE_URL=your_database_url
   REDIS_URL=your_redis_url
   SECRET_KEY=your_secret_key
   ```

## 🔧 Настройка переменных окружения

### В Vercel Dashboard:
1. Перейдите в Settings → Environment Variables
2. Добавьте переменные:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port/0
SECRET_KEY=your-secret-key-here
ADMIN_USER_IDS=123456789
WEBHOOK_URL=https://your-project.vercel.app
WEBHOOK_PATH=/webhook
```

## 📱 Настройка Telegram Webhook

### После развертывания на Vercel:
1. Получите URL вашего проекта: `https://your-project.vercel.app`
2. Установите webhook для бота:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-project.vercel.app/webhook"}'
```

## 🎮 Веб-интерфейс игр

После развертывания игры будут доступны по адресам:
- `https://your-project.vercel.app/` - главная страница
- `https://your-project.vercel.app/game/clicker` - игра Кликер
- `https://your-project.vercel.app/game/reaction` - тест на реакцию
- `https://your-project.vercel.app/game/2048` - игра 2048

## 🔄 Автоматическое развертывание

После настройки каждое изменение в GitHub будет автоматически развертываться на Vercel.

### Workflow:
1. Вносите изменения в код
2. Коммитите и пушите в GitHub:
   ```bash
   git add .
   git commit -m "Update: описание изменений"
   git push origin main
   ```
3. Vercel автоматически развернет обновления

## 📊 Мониторинг

### В Vercel Dashboard:
- **Analytics** - статистика посещений
- **Functions** - логи выполнения
- **Deployments** - история развертываний

### Логи бота:
- Доступны в Vercel Functions
- Можно настроить внешний мониторинг (Sentry, LogRocket)

## 🚨 Важные замечания

### Ограничения Vercel:
- **Timeout**: 30 секунд для функций
- **Memory**: 1GB максимум
- **Cold starts**: возможны задержки при первом запуске

### Рекомендации:
1. **База данных**: Используйте внешний PostgreSQL (Supabase, Neon, PlanetScale)
2. **Redis**: Используйте внешний Redis (Upstash, Redis Cloud)
3. **Мониторинг**: Настройте внешний мониторинг
4. **Backup**: Регулярно создавайте бэкапы БД

## 🎯 Результат

После выполнения всех шагов у вас будет:
- ✅ Репозиторий на GitHub
- ✅ Развернутое приложение на Vercel
- ✅ Работающий Telegram бот
- ✅ Веб-интерфейс для игр
- ✅ Автоматическое развертывание

---

**🚀 Ваша турнирная платформа готова к работе в облаке!**
