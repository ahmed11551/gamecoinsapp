# 🤖 Создание Telegram бота - Пошаговая инструкция

## 📋 Что нужно сделать

### 1. Создание бота через BotFather

1. **Откройте Telegram** и найдите [@BotFather](https://t.me/botfather)
2. **Отправьте команду** `/start`
3. **Отправьте команду** `/newbot`
4. **Введите имя бота**: `Tournament Platform Bot`
5. **Введите username**: `your_tournament_bot` (должен заканчиваться на `bot`)
6. **Скопируйте токен** бота (выглядит как `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Настройка бота

#### Команды бота:
```
/setcommands
```

Добавьте команды:
```
start - Начать работу с ботом
profile - Ваш профиль
balance - Баланс и транзакции
deposit - Пополнить баланс
withdraw - Вывести средства
tournaments - Активные турниры
help - Справка
```

#### Описание бота:
```
/setdescription
```

Добавьте описание:
```
🏆 Турнирная платформа для игр на навыки

✅ Игры на навыки (Кликер, Реакция, 2048)
✅ Реальные денежные призы
✅ Честные соревнования
✅ Быстрые выплаты

🎮 Участвуйте в турнирах и выигрывайте!
```

#### Короткое описание:
```
/setshortdescription
```

Добавьте:
```
🏆 Турниры в играх на навыки с реальными призами
```

### 3. Настройка webhook

После развертывания на Vercel получите URL вашего проекта и установите webhook:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-project.vercel.app/webhook"}'
```

### 4. Проверка webhook

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

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
```

## 🗄️ Настройка базы данных

### PostgreSQL (рекомендуется Supabase):

1. **Перейдите на [supabase.com](https://supabase.com)**
2. **Создайте новый проект**
3. **Скопируйте DATABASE_URL** из настроек проекта
4. **Добавьте в переменные окружения Vercel**

### Redis (рекомендуется Upstash):

1. **Перейдите на [upstash.com](https://upstash.com)**
2. **Создайте новый Redis database**
3. **Скопируйте REDIS_URL** из настроек
4. **Добавьте в переменные окружения Vercel**

## 🎮 Тестирование бота

### 1. Проверка бота

1. **Найдите вашего бота** в Telegram по username
2. **Отправьте команду** `/start`
3. **Проверьте ответ** бота

### 2. Проверка меню

1. **Нажмите на кнопку меню** в боте
2. **Проверьте все команды**
3. **Протестируйте навигацию**

### 3. Проверка игр

1. **Нажмите "🎮 Игры"**
2. **Выберите игру**
3. **Проверьте загрузку WebView**

## 🚨 Возможные проблемы

### Проблема: Бот не отвечает
**Решение**: 
- Проверьте webhook: `curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"`
- Проверьте токен бота
- Проверьте переменные окружения в Vercel

### Проблема: Ошибка базы данных
**Решение**: 
- Проверьте DATABASE_URL
- Проверьте подключение к Supabase
- Проверьте права доступа

### Проблема: Ошибка Redis
**Решение**: 
- Проверьте REDIS_URL
- Проверьте подключение к Upstash
- Проверьте лимиты запросов

### Проблема: WebView не загружается
**Решение**: 
- Проверьте URL проекта в Vercel
- Проверьте настройки CORS
- Проверьте логи в Vercel Functions

## 📊 Мониторинг

### В Vercel Dashboard:
- **Analytics** - статистика посещений
- **Functions** - логи выполнения
- **Deployments** - история развертываний

### В Telegram:
- **BotFather** - статистика бота
- **@BotSupport** - поддержка ботов

## 🔄 Автоматическое развертывание

После настройки каждое изменение в GitHub будет автоматически развертываться на Vercel.

### Workflow:
1. Вносите изменения в код
2. Коммитите и пушите в GitHub
3. Vercel автоматически развернет обновления
4. Бот автоматически обновится

## 🎯 Результат

После выполнения всех шагов у вас будет:

- ✅ **Работающий Telegram бот**
- ✅ **Веб-интерфейс для игр**
- ✅ **База данных PostgreSQL**
- ✅ **Кэширование Redis**
- ✅ **Автоматические выплаты**
- ✅ **Система рейтингов**
- ✅ **Анти-чит защита**

---

**🎉 Поздравляем! Ваша турнирная платформа готова к работе!**
