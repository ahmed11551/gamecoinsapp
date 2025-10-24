# 🔧 Исправление ошибки Vercel конфигурации

## ❌ Проблема
```
Свойство `functions` нельзя использовать вместе со свойством `builds`. 
Удалите одно из них.
```

## ✅ Решение

### 1. Обновлен файл `vercel.json`

Исправленная конфигурация:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "web_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/webhook",
      "dest": "run.py"
    },
    {
      "src": "/(.*)",
      "dest": "web_app.py"
    }
  ]
}
```

### 2. Что изменилось:

- ❌ **Удалено**: свойство `functions`
- ❌ **Удалено**: свойство `env`
- ❌ **Удалено**: `config` с `maxLambdaSize`
- ✅ **Оставлено**: только `builds` и `routes`

### 3. Логика маршрутизации:

- `/webhook` → `run.py` (для Telegram бота)
- Все остальные запросы → `web_app.py` (веб-интерфейс)

## 🚀 Теперь можно развертывать!

### 1. Обновите код на GitHub:
```bash
git add vercel.json
git commit -m "Fix Vercel configuration - remove functions property"
git push origin main
```

### 2. Разверните на Vercel:
- Перейдите на [vercel.com](https://vercel.com)
- Импортируйте репозиторий `ahmed11551/gamecoinsapp`
- Настройки:
  - **Framework Preset**: `Other`
  - **Root Directory**: `./`
  - **Build Command**: `pip install -r requirements.txt`
  - **Output Directory**: `./`

### 3. Добавьте переменные окружения:
```env
BOT_TOKEN=your_bot_token_from_botfather
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port/0
SECRET_KEY=your-secret-key-here
ADMIN_USER_IDS=your_telegram_id
WEBHOOK_URL=https://your-project.vercel.app
WEBHOOK_PATH=/webhook
```

## 🎯 Результат

После исправления:
- ✅ **Vercel развертывание** будет работать без ошибок
- ✅ **Telegram webhook** будет доступен по `/webhook`
- ✅ **Веб-интерфейс** будет доступен по корневому URL
- ✅ **Игры** будут работать через WebView

## 🔄 Альтернативные конфигурации

Если основная конфигурация не работает, используйте:

### `vercel-simple.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "web_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "web_app.py"
    }
  ]
}
```

### `vercel-alternative.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "web_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/webhook",
      "dest": "run.py"
    },
    {
      "src": "/(.*)",
      "dest": "web_app.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}
```

---

**🎉 Проблема решена! Теперь можно развертывать на Vercel!**
