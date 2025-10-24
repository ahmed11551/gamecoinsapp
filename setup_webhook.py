"""
Скрипт для настройки Telegram webhook
"""
import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def setup_webhook():
    """Настройка webhook для Telegram бота"""
    
    # Получаем переменные окружения
    bot_token = os.getenv('BOT_TOKEN')
    webhook_url = os.getenv('WEBHOOK_URL')
    webhook_path = os.getenv('WEBHOOK_PATH', '/webhook')
    
    if not bot_token:
        print("❌ BOT_TOKEN не найден в переменных окружения")
        return False
    
    if not webhook_url:
        print("❌ WEBHOOK_URL не найден в переменных окружения")
        return False
    
    # Формируем полный URL webhook
    full_webhook_url = f"{webhook_url}{webhook_path}"
    
    print(f"🤖 Настройка webhook для бота...")
    print(f"📡 URL: {full_webhook_url}")
    
    # Устанавливаем webhook
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    data = {
        "url": full_webhook_url,
        "allowed_updates": ["message", "callback_query"]
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Webhook успешно установлен!")
            print(f"📋 Описание: {result.get('description', 'Нет описания')}")
            return True
        else:
            print(f"❌ Ошибка установки webhook: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при установке webhook: {e}")
        return False

def check_webhook():
    """Проверка статуса webhook"""
    
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ BOT_TOKEN не найден в переменных окружения")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    
    try:
        response = requests.get(url)
        result = response.json()
        
        if result.get('ok'):
            webhook_info = result.get('result', {})
            print("📊 Информация о webhook:")
            print(f"   URL: {webhook_info.get('url', 'Не установлен')}")
            print(f"   Статус: {'✅ Активен' if webhook_info.get('url') else '❌ Не установлен'}")
            print(f"   Ошибки: {webhook_info.get('last_error_message', 'Нет ошибок')}")
            return True
        else:
            print(f"❌ Ошибка получения информации: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при проверке webhook: {e}")
        return False

def delete_webhook():
    """Удаление webhook (для переключения на polling)"""
    
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ BOT_TOKEN не найден в переменных окружения")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    
    try:
        response = requests.post(url)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Webhook успешно удален!")
            return True
        else:
            print(f"❌ Ошибка удаления webhook: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при удалении webhook: {e}")
        return False

def get_bot_info():
    """Получение информации о боте"""
    
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ BOT_TOKEN не найден в переменных окружения")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    
    try:
        response = requests.get(url)
        result = response.json()
        
        if result.get('ok'):
            bot_info = result.get('result', {})
            print("🤖 Информация о боте:")
            print(f"   Имя: {bot_info.get('first_name')}")
            print(f"   Username: @{bot_info.get('username')}")
            print(f"   ID: {bot_info.get('id')}")
            print(f"   Может присоединяться к группам: {'✅ Да' if bot_info.get('can_join_groups') else '❌ Нет'}")
            print(f"   Может читать сообщения группы: {'✅ Да' if bot_info.get('can_read_all_group_messages') else '❌ Нет'}")
            return True
        else:
            print(f"❌ Ошибка получения информации: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при получении информации о боте: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Утилита для настройки Telegram бота")
    print("=" * 50)
    
    while True:
        print("\nВыберите действие:")
        print("1. Установить webhook")
        print("2. Проверить webhook")
        print("3. Удалить webhook")
        print("4. Информация о боте")
        print("5. Выход")
        
        choice = input("\nВведите номер (1-5): ").strip()
        
        if choice == "1":
            setup_webhook()
        elif choice == "2":
            check_webhook()
        elif choice == "3":
            delete_webhook()
        elif choice == "4":
            get_bot_info()
        elif choice == "5":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
