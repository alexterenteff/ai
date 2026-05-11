import requests
import os
import sys
from openai import OpenAI

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def get_news_from_deepseek():
    """Получает свежие новости об ИИ через OpenRouter (DeepSeek V4 Flash бесплатно)"""
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    prompt = """Ты — редактор новостного канала об искусственном интеллекте.
Найди 5 самых свежих и важных новостей об ИИ, AI, нейросетях за последние 24 часа.
Используй поиск в интернете, если нужно.

Для каждой новости укажи:
1. Заголовок
2. Краткое описание (1 предложение)
3. Ссылку на источник

Оформи ответ в таком формате:

**1. [Заголовок]**
[Краткое описание]
🔗 [Источник]

**2. [Заголовок]**
[Краткое описание]
🔗 [Источник]

В конце добавь: 📱 Подпишись: @tAiT_plus

Используй эмодзи 🤖🧠💡. Ответь только на русском языке."""
    
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-v4-flash:free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7,
            extra_headers={
                "HTTP-Referer": "https://t.me/tAiT_plus",
                "X-Title": "tAiT Plus Bot"
            }
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Ошибка OpenRouter: {e}")
        return None

def send_to_telegram(message):
    """Отправляет сообщение в Telegram канал"""
    if not message:
        message = "🤖 Новостей не найдено. Попробуй позже.\n\n📱 Подпишись: @tAiT_plus"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    try:
        result = requests.post(url, json=payload, timeout=30).json()
        if result.get('ok'):
            print("✅ Сообщение отправлено в Telegram")
        else:
            print(f"❌ Ошибка Telegram: {result}")
        return result.get('ok', False)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🚀 Запуск бота tAiT Plus на OpenRouter...")
    print(f"📡 Канал: {CHANNEL_ID}")
    
    if not BOT_TOKEN or not CHANNEL_ID:
        print("❌ Ошибка: нет TELEGRAM_BOT_TOKEN или CHANNEL_ID")
        sys.exit(1)
    if not OPENROUTER_API_KEY:
        print("❌ Ошибка: нет OPENROUTER_API_KEY")
        sys.exit(1)
    
    news = get_news_from_deepseek()
    success = send_to_telegram(news)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
