import asyncio

from telegram import Bot

from config import (
    TELEGRAM_TOKEN,
    CHAT_ID,
    POLL_INTERVAL_SECONDS,
    THRESHOLDS,
)
from sensors import VirtualWellSensors


LABELS = {
    "pressure": "Pressure",
    "temperature": "Temperature",
    "oil_level": "Oil level",
    "pump_voltage": "Pump voltage",
}

UNITS = {
    "pressure": "bar",
    "temperature": "°C",
    "oil_level": "%",
    "pump_voltage": "V",
}


class WellMonitor:
    def __init__(self):
        self.sensors = VirtualWellSensors()

        # Shared with app.py.
        self.latest_readings = None
        self.current_alerts = []

        # Telegram is optional while setting up the dashboard.
        self.bot = (
            Bot(token=TELEGRAM_TOKEN)
            if TELEGRAM_TOKEN and CHAT_ID
            else None
        )

    def find_alerts(self, readings):
        """Return messages for measurements outside their limits."""
        alerts = []

        for key, limits in THRESHOLDS.items():
            value = readings[key]

            if not limits["min"] <= value <= limits["max"]:
                message = (
                    f"⚠️ {LABELS[key]}: {value} {UNITS[key]} "
                    f"(allowed range: {limits['min']}–"
                    f"{limits['max']} {UNITS[key]})"
                )
                alerts.append(message)

        return alerts

    async def monitor_loop(self):
        """Continuously collect readings and check for alerts."""
        if self.bot is not None:
            try:
                await self.bot.initialize()
            except Exception as error:
                print(f"Telegram initialization failed: {error}")
                print("Continuing in console-only mode.")
                self.bot = None
            else:
                try:
                    await self._run_forever()
                finally:
                    await self.bot.shutdown()
                return

        await self._run_forever()

    async def _run_forever(self):
        while True:
            readings = self.sensors.get_readings()

            # Publish the latest readings for the dashboard.
            self.latest_readings = readings

            # Calculate the current alert status.
            self.current_alerts = self.find_alerts(readings)

            print(
                f"[{readings['timestamp']}] "
                f"Pressure: {readings['pressure']} bar | "
                f"Temperature: {readings['temperature']} °C | "
                f"Oil: {readings['oil_level']}% | "
                f"Voltage: {readings['pump_voltage']} V"
            )

            if self.current_alerts:
                message = (
                    "🚨 WELL MONITORING ALERT\n\n"
                    + "\n".join(self.current_alerts)
                    + f"\n\nTime: {readings['timestamp']}"
                )

                print(message)

                if self.bot is not None:
                    try:
                        await self.bot.send_message(
                            chat_id=CHAT_ID,
                            text=message,
                        )
                        print("Telegram alert sent successfully.")
                    except Exception as error:
                        print(f"Failed to send Telegram alert: {error}")
                else:
                    print("Telegram is not configured; no message sent.")

            await asyncio.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(WellMonitor().monitor_loop())
