import os
import sys
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def get_news_from_deepseek():
    """Получает новости через OpenRouter"""
    
    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY не найден")
        return None
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/tAiT_plus",
        "X-Title": "tAiT Plus Bot"
    }
    
    # ЗДЕСЬ МЕНЯЕМ НАЗВАНИЕ МОДЕЛИ
    MODEL_NAME = "deepseek/deepseek-r1:free"  # работающая бесплатная модель
    
    prompt = """Ты — редактор новостного канала об искусственном интеллекте.
Найди 5 самых свежих и важных новостей об ИИ за последние 24 часа.

Для каждой новости укажи:
1. Заголовок
2. Краткое описание (1 предложение)
3. Ссылку на источник

Оформи ответ в таком формате:

**1. [Заголовок]**
[Описание]
🔗 [Источник]

В конце добавь: 📱 Подпишись: @tAiT_plus

Отвечай только на русском языке. Используй эмодзи."""
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    
    try:
        print(f"🔍 Запрос к модели: {MODEL_NAME}")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print("✅ DeepSeek ответил")
            return content
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"Ответ: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def send_to_telegram(message):
    """Отправляет сообщение в Telegram"""
    if not message:
        message = "🤖 Новостей не найдено.\n\n📱 Подпишись: @tAiT_plus"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "disable_web_page_preview": True
    }
    
    try:
        result = requests.post(url, json=payload, timeout=30).json()
        if result.get('ok'):
            print("✅ Сообщение отправлено")
            return True
        else:
            print(f"❌ Ошибка Telegram: {result}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🚀 Запуск бота на OpenRouter...")
    print(f"📡 Канал: {CHANNEL_ID}")
    
    if not BOT_TOKEN or not CHANNEL_ID or not OPENROUTER_API_KEY:
        print("❌ Ошибка: не хватает секретов")
        sys.exit(1)
    
    news = get_news_from_deepseek()
    success = send_to_telegram(news)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
