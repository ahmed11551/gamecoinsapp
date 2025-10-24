"""
Быстрое развертывание на Vercel
"""
import subprocess
import os
import json

def deploy_to_vercel():
    """Развертывание проекта на Vercel"""
    
    print("🚀 Развертывание турнирной платформы на Vercel...")
    
    # Проверяем наличие Vercel CLI
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Vercel CLI не установлен")
            print("📦 Установите Vercel CLI: npm i -g vercel")
            return False
        else:
            print(f"✅ Vercel CLI найден: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Vercel CLI не найден")
        print("📦 Установите Vercel CLI: npm i -g vercel")
        return False
    
    # Проверяем наличие .env файла
    if not os.path.exists('.env'):
        print("⚠️  Файл .env не найден")
        print("📝 Создайте .env файл с переменными окружения")
        return False
    
    # Развертывание
    try:
        print("🔄 Начинаем развертывание...")
        result = subprocess.run(['vercel', '--prod'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Развертывание успешно завершено!")
            print(f"🌐 URL: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ошибка при развертывании:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при развертывании: {e}")
        return False

def setup_environment():
    """Настройка переменных окружения"""
    
    print("🔧 Настройка переменных окружения...")
    
    env_vars = {
        'BOT_TOKEN': 'Токен вашего Telegram бота',
        'DATABASE_URL': 'URL базы данных PostgreSQL',
        'REDIS_URL': 'URL Redis сервера',
        'SECRET_KEY': 'Секретный ключ для безопасности',
        'ADMIN_USER_IDS': 'ID администраторов (через запятую)',
        'WEBHOOK_URL': 'URL вашего Vercel проекта',
        'WEBHOOK_PATH': '/webhook'
    }
    
    print("\n📋 Необходимые переменные окружения:")
    for key, description in env_vars.items():
        print(f"   {key}: {description}")
    
    print("\n💡 Добавьте эти переменные в Vercel Dashboard:")
    print("   Settings → Environment Variables")
    
    return True

def create_env_example():
    """Создание примера .env файла"""
    
    env_example = """# Конфигурация для турнирной платформы
# Скопируйте этот файл в .env и заполните значения

# Telegram Bot
BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your-project.vercel.app
WEBHOOK_PATH=/webhook

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/tournament_bot
REDIS_URL=redis://localhost:6379/0

# Payment Systems
TELEGRAM_STARS_API_KEY=your_telegram_stars_api_key
YOO_KASSA_SHOP_ID=your_yookassa_shop_id
YOO_KASSA_SECRET_KEY=your_yookassa_secret_key
BINANCE_API_KEY=your_binance_api_key

# Security
SECRET_KEY=your-secret-key-here-change-this
ADMIN_USER_IDS=123456789,987654321

# Tournament Settings
MIN_WITHDRAWAL_AMOUNT=500.0
WITHDRAWAL_COMMISSION=0.03
RESERVE_PERCENTAGE=0.05

# Commission Rates
COMMISSION_RATES_LOW=0.20
COMMISSION_RATES_MEDIUM=0.15
COMMISSION_RATES_HIGH=0.10

# Game Settings
DUEL_TIMEOUT=1800
GROUP_TOURNAMENT_TIMEOUT=3600
MARATHON_TIMEOUT=86400
"""
    
    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(env_example)
    
    print("✅ Создан файл .env.example")
    print("📝 Скопируйте его в .env и заполните значения")

if __name__ == "__main__":
    print("🎯 Турнирная платформа - Развертывание на Vercel")
    print("=" * 60)
    
    while True:
        print("\nВыберите действие:")
        print("1. Развернуть на Vercel")
        print("2. Настроить переменные окружения")
        print("3. Создать .env.example")
        print("4. Выход")
        
        choice = input("\nВведите номер (1-4): ").strip()
        
        if choice == "1":
            deploy_to_vercel()
        elif choice == "2":
            setup_environment()
        elif choice == "3":
            create_env_example()
        elif choice == "4":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
