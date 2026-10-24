import os
from dotenv import load_dotenv

# Load settings from the .env file.
load_dotenv()

# Telegram credentials.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

# Take a new reading every 2 seconds.
POLL_INTERVAL_SECONDS = float(
    os.getenv("POLL_INTERVAL_SECONDS", "2")
)

# Thresholds for the simulated oil well.
THRESHOLDS = {
    "pressure": {
        "min": 100,
        "max": 200,
    },
    "temperature": {
        "min": 20,
        "max": 85,
    },
    "oil_level": {
        "min": 10,
        "max": 100,
    },
    "pump_voltage": {
        "min": 350,
        "max": 410,
    },
}
