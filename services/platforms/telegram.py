import os
import httpx
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BASE_URL=os.getenv("TELEGRAM_BASE_URL")
TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")


async def send_telegram_alert(message: str, chat_id: str):
    bot_token = TELEGRAM_BOT_TOKEN
    url = f"{TELEGRAM_BASE_URL}/bot{bot_token}/sendMessage"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                data={
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'Markdown',
                },
                timeout=10.0
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            print(f"❌ Telegram error: {exc}")
