"""
Автоматическое развертывание на Vercel
"""
import subprocess
import os
import time
import json

def check_vercel_cli():
    """Проверка наличия Vercel CLI"""
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Vercel CLI найден: {result.stdout.strip()}")
            return True
        else:
            print("❌ Vercel CLI не установлен")
            return False
    except FileNotFoundError:
        print("❌ Vercel CLI не найден")
        return False

def install_vercel_cli():
    """Установка Vercel CLI"""
    print("📦 Установка Vercel CLI...")
    try:
        result = subprocess.run(['npm', 'i', '-g', 'vercel'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Vercel CLI успешно установлен")
            return True
        else:
            print(f"❌ Ошибка установки: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при установке: {e}")
        return False

def login_vercel():
    """Логин в Vercel"""
    print("🔐 Логин в Vercel...")
    try:
        result = subprocess.run(['vercel', 'login'], input='y\n', text=True, capture_output=True)
        if result.returncode == 0:
            print("✅ Успешный логин в Vercel")
            return True
        else:
            print(f"❌ Ошибка логина: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при логине: {e}")
        return False

def deploy_to_vercel(project_name=None):
    """Развертывание на Vercel"""
    print("🚀 Развертывание на Vercel...")
    
    cmd = ['vercel', '--prod']
    if project_name:
        cmd.extend(['--name', project_name])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Развертывание успешно завершено!")
            print(f"🌐 Результат: {result.stdout}")
            return True
        else:
            print(f"❌ Ошибка развертывания: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при развертывании: {e}")
        return False

def setup_environment_variables():
    """Инструкции по настройке переменных окружения"""
    print("\n🔧 Настройка переменных окружения:")
    print("1. Перейдите в Vercel Dashboard")
    print("2. Откройте ваш проект")
    print("3. Перейдите в Settings → Environment Variables")
    print("4. Добавьте следующие переменные:")
    print()
    print("BOT_TOKEN=your_bot_token_from_botfather")
    print("DATABASE_URL=postgresql://user:password@host:port/database")
    print("REDIS_URL=redis://host:port/0")
    print("SECRET_KEY=your-secret-key-here")
    print("ADMIN_USER_IDS=your_telegram_id")
    print("WEBHOOK_URL=https://your-project.vercel.app")
    print("WEBHOOK_PATH=/webhook")

def setup_telegram_webhook():
    """Инструкции по настройке Telegram webhook"""
    print("\n🤖 Настройка Telegram webhook:")
    print("1. Создайте бота через @BotFather")
    print("2. Получите токен бота")
    print("3. Установите webhook:")
    print()
    print('curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"url": "https://your-project.vercel.app/webhook"}\'')

def main():
    """Основная функция"""
    print("🎯 Автоматическое развертывание турнирной платформы на Vercel")
    print("=" * 70)
    
    # Проверяем Vercel CLI
    if not check_vercel_cli():
        print("\n📦 Установка Vercel CLI...")
        if not install_vercel_cli():
            print("❌ Не удалось установить Vercel CLI")
            print("💡 Установите вручную: npm i -g vercel")
            return False
    
    # Логин в Vercel
    print("\n🔐 Логин в Vercel...")
    if not login_vercel():
        print("❌ Не удалось войти в Vercel")
        return False
    
    # Выбор имени проекта
    print("\n📝 Выберите имя проекта:")
    print("1. tournament-platform-2024")
    print("2. telegram-games-bot")
    print("3. skill-tournament-app")
    print("4. games-platform-bot")
    print("5. Ввести свое имя")
    
    choice = input("\nВведите номер (1-5): ").strip()
    
    project_names = {
        "1": "tournament-platform-2024",
        "2": "telegram-games-bot", 
        "3": "skill-tournament-app",
        "4": "games-platform-bot"
    }
    
    if choice in project_names:
        project_name = project_names[choice]
    elif choice == "5":
        project_name = input("Введите имя проекта: ").strip()
    else:
        project_name = "tournament-platform-2024"
    
    print(f"\n🚀 Развертывание проекта: {project_name}")
    
    # Развертывание
    if deploy_to_vercel(project_name):
        print(f"\n🎉 Проект '{project_name}' успешно развернут!")
        
        # Инструкции по настройке
        setup_environment_variables()
        setup_telegram_webhook()
        
        print(f"\n🌐 URL проекта: https://{project_name}.vercel.app")
        print("📱 Веб-интерфейс: https://{project_name}.vercel.app/")
        print("🤖 Webhook: https://{project_name}.vercel.app/webhook")
        
        return True
    else:
        print("❌ Развертывание не удалось")
        return False

if __name__ == "__main__":
    main()
