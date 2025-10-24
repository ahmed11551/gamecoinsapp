# 🚀 Быстрый старт - Турнирная платформа

## 📋 Что готово

✅ **MVP турнирной платформы полностью готов!**

- 🎮 3 игры на навыки (Кликер, Реакция, 2048)
- 🏆 Турнирная система (Дуэли, Групповые, Марафоны)
- 💰 Платежная система (Telegram Stars, карты, крипта)
- 👤 Система пользователей с рейтингами
- 🛡️ Анти-чит защита
- 🌐 Веб-интерфейс для игр

## 🚀 Развертывание за 5 минут

### 1. GitHub
```bash
# Создайте репозиторий на github.com
git remote add origin https://github.com/YOUR_USERNAME/tournament-platform-telegram.git
git branch -M main
git push -u origin main
```

### 2. Vercel
1. Перейдите на [vercel.com](https://vercel.com)
2. Импортируйте репозиторий с GitHub
3. Настройки: Framework Preset = Other
4. Добавьте переменные окружения

### 3. Переменные окружения
```env
BOT_TOKEN=your_bot_token_from_botfather
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port/0
SECRET_KEY=your-secret-key-here
WEBHOOK_URL=https://your-project.vercel.app
```

### 4. Telegram Webhook
```bash
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-project.vercel.app/webhook"}'
```

## 🎮 Результат

После развертывания:
- ✅ Telegram бот работает
- ✅ Веб-интерфейс игр доступен
- ✅ Турниры проводятся автоматически
- ✅ Платежи обрабатываются
- ✅ Призы выплачиваются

## 💰 Экономика

- Комиссия платформы: 10-20%
- Минимальный вывод: 500 ₽
- Комиссия на вывод: 3%
- Резервный фонд: 5%

## 🛡️ Легальность

✅ **Разрешено**: Игры на навыки (skill-based games)  
❌ **Запрещено**: Азартные игры (games of chance)

---

**🎉 Готово! Ваша турнирная платформа работает!**
