import os
import sys
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def get_news_from_deepseek():
    """Получает свежие новости об ИИ через OpenRouter."""
    
    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY не найден")
        return None

    # 1. Используем стабильную бесплатную модель Google Gemini
    model_name = "google/gemini-2.0-flash-exp:free"
    
    # 2. Улучшенный промпт, явно требующий поиска в интернете
    prompt = """Ты — редактор новостного канала об искусственном интеллекте.
Твоя задача — найти 5 САМЫХ СВЕЖИХ (за последние 24 часа) и важных мировых новостей об ИИ и нейросетях.
ОБЯЗАТЕЛЬНО используй инструмент 'web_search' в интернете, чтобы найти актуальную информацию.
Если поиск не дал результатов, так и напиши.

Для каждой новости строго соблюдай следующий формат:

**1. [Заголовок новости]**
[Краткое описание, 1 предложение]
🔗 [Источник]

В конце добавь строку: 📱 Подпишись: @tAiT_plus

Отвечай строго на русском языке. Используй эмодзи."""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/tAiT_plus",
        "X-Title": "tAiT Plus Bot"
    }

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.7# Ниже среднего для более фактологичных ответов
    }
    
    try:
        print(f"🔍 Запрос к модели: {model_name}")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            # Извлекаем текст ответа
            message_content = result['choices'][0]['message']['content']
            print("✅ Модель успешно ответила")
            return message_content
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"Ответ: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
        return None

def send_to_telegram(message):
    """Отправляет сообщение в Telegram канал."""
    if not message:
        message = "🤖 Новостей не найдено. Попробуйте позже.\n\n📱 Подпишись: @tAiT_plus"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        # КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: убираем parse_mode, чтобы избежать ошибок с форматированием
        "disable_web_page_preview": True
    }
    
    try:
        result = requests.post(url, json=payload, timeout=30).json()
        if result.get('ok'):
            print("✅ Сообщение отправлено в Telegram")
            return True
        else:
            print(f"❌ Ошибка Telegram: {result}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🚀 Запуск обновлённого бота tAiT Plus...")
    print(f"📡 Канал: {CHANNEL_ID}")
    
    if not BOT_TOKEN or not CHANNEL_ID or not OPENROUTER_API_KEY:
        print("❌ Ошибка: не хватает секретов")
        sys.exit(1)
    
    news = get_news_from_deepseek()
    success = send_to_telegram(news)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
