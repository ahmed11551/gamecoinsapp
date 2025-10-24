"""
Быстрое развертывание на Vercel
"""
import subprocess
import sys

def quick_deploy():
    """Быстрое развертывание"""
    print("🚀 Быстрое развертывание турнирной платформы на Vercel")
    print("=" * 60)
    
    # Проверяем наличие Vercel CLI
    try:
        subprocess.run(['vercel', '--version'], check=True, capture_output=True)
        print("✅ Vercel CLI найден")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Vercel CLI не найден")
        print("📦 Установка Vercel CLI...")
        try:
            subprocess.run(['npm', 'i', '-g', 'vercel'], check=True)
            print("✅ Vercel CLI установлен")
        except subprocess.CalledProcessError:
            print("❌ Не удалось установить Vercel CLI")
            print("💡 Установите вручную: npm i -g vercel")
            return False
    
    # Список доступных имен проектов
    project_names = [
        "tournament-platform-2024",
        "telegram-games-bot",
        "skill-tournament-app", 
        "games-platform-bot",
        "tournament-bot-v2",
        "skill-games-platform-v2"
    ]
    
    print("\n📝 Доступные имена проектов:")
    for i, name in enumerate(project_names, 1):
        print(f"{i}. {name}")
    
    # Выбираем имя проекта
    while True:
        try:
            choice = int(input(f"\nВыберите номер (1-{len(project_names)}): "))
            if 1 <= choice <= len(project_names):
                project_name = project_names[choice - 1]
                break
            else:
                print("❌ Неверный номер")
        except ValueError:
            print("❌ Введите число")
    
    print(f"\n🚀 Развертывание проекта: {project_name}")
    
    # Развертывание
    try:
        result = subprocess.run([
            'vercel', '--prod', '--name', project_name, '--yes'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Развертывание успешно завершено!")
            print(f"🌐 URL: https://{project_name}.vercel.app")
            
            print("\n🔧 Следующие шаги:")
            print("1. Добавьте переменные окружения в Vercel Dashboard")
            print("2. Создайте Telegram бота через @BotFather")
            print("3. Настройте webhook:")
            print(f'   curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \\')
            print(f'        -H "Content-Type: application/json" \\')
            print(f'        -d \'{{"url": "https://{project_name}.vercel.app/webhook"}}\'')
            
            return True
        else:
            print(f"❌ Ошибка развертывания: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при развертывании: {e}")
        return False

if __name__ == "__main__":
    quick_deploy()
