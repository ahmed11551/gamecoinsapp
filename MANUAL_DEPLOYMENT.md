# 🚀 Ручное развертывание на Vercel

## ❌ Проблема
```
Error: Resource is limited - try again in 15 hours 
(more than 100, code: "api-deployments-free-per-day")
```

## ✅ Решение: Ручное развертывание через веб-интерфейс

### 1. Перейдите на [vercel.com](https://vercel.com)

### 2. Войдите в аккаунт (или зарегистрируйтесь)

### 3. Нажмите "New Project"

### 4. Импортируйте репозиторий
- Выберите **"Import Git Repository"**
- Найдите и выберите `ahmed11551/gamecoinsapp`
- Нажмите **"Import"**

### 5. Настройки проекта
- **Project Name**: `tournament-platform-2024` (или любое другое уникальное имя)
- **Framework Preset**: `Other`
- **Root Directory**: `./`
- **Build Command**: `pip install -r requirements.txt`
- **Output Directory**: `./`
- **Install Command**: `pip install -r requirements.txt`

### 6. Переменные окружения
В разделе **"Environment Variables"** добавьте:

```env
BOT_TOKEN=your_bot_token_from_botfather
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port/0
SECRET_KEY=your-secret-key-here
ADMIN_USER_IDS=your_telegram_id
WEBHOOK_URL=https://tournament-platform-2024.vercel.app
WEBHOOK_PATH=/webhook
```

### 7. Нажмите "Deploy"

## 🤖 Создание Telegram бота

### 1. Найдите [@BotFather](https://t.me/botfather) в Telegram

### 2. Создайте бота:
```
/newbot
```

### 3. Введите данные:
- **Имя бота**: `Tournament Platform Bot`
- **Username**: `your_tournament_bot` (должен заканчиваться на `bot`)

### 4. Скопируйте токен бота

### 5. Настройте команды:
```
/setcommands
```

Добавьте:
```
start - Начать работу с ботом
profile - Ваш профиль
balance - Баланс и транзакции
deposit - Пополнить баланс
withdraw - Вывести средства
tournaments - Активные турниры
help - Справка
```

## 🗄️ Настройка базы данных

### PostgreSQL (Supabase):
1. Перейдите на [supabase.com](https://supabase.com)
2. Создайте новый проект
3. Скопируйте **DATABASE_URL** из настроек
4. Добавьте в переменные окружения Vercel

### Redis (Upstash):
1. Перейдите на [upstash.com](https://upstash.com)
2. Создайте новый Redis database
3. Скопируйте **REDIS_URL** из настроек
4. Добавьте в переменные окружения Vercel

## 🔧 Настройка webhook

После развертывания на Vercel получите URL проекта и установите webhook:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-project-name.vercel.app/webhook"}'
```

## 🎯 Результат

После выполнения всех шагов у вас будет:

- ✅ **Работающий Telegram бот**
- ✅ **Веб-интерфейс**: `https://your-project.vercel.app/`
- ✅ **Webhook**: `https://your-project.vercel.app/webhook`
- ✅ **Игры**: Кликер, Реакция, 2048
- ✅ **Турниры**: Дуэли, Групповые, Марафоны
- ✅ **Платежи**: Telegram Stars, карты, крипта
- ✅ **Анти-чит защита**

## 📱 Тестирование

### 1. Найдите вашего бота в Telegram
### 2. Отправьте команду `/start`
### 3. Протестируйте меню и игры
### 4. Проверьте веб-интерфейс

## 💰 Экономическая модель

- **Комиссия платформы**: 10-20%
- **Минимальный вывод**: 500 ₽
- **Комиссия на вывод**: 3%
- **Резервный фонд**: 5%

## 🛡️ Легальность

✅ **Разрешено**: Игры на навыки (skill-based games)  
❌ **Запрещено**: Азартные игры (games of chance)

---

**🎉 После выполнения всех шагов ваша турнирная платформа будет работать!**

**⏰ Лимит Vercel восстановится через 15 часов, но ручное развертывание работает всегда!**
