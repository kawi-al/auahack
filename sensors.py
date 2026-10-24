import random
from datetime import datetime


class VirtualWellSensors:
    """Generate simulated oil well sensor readings."""

    def get_readings(self):
        # Normal operating values with small fluctuations.
        readings = {
            "timestamp": datetime.now().astimezone().isoformat(
                timespec="seconds"
            ),
            "pressure": round(random.uniform(145, 155), 2),
            "temperature": round(random.uniform(63, 67), 2),
            "oil_level": round(random.uniform(78, 82), 2),
            "pump_voltage": round(random.uniform(375, 385), 2),
        }

        # Introduce an occasional abnormal reading.
        if random.random() < 0.05:
            anomaly = random.choice([
                "pressure",
                "temperature",
                "oil_level",
                "pump_voltage",
            ])

            if anomaly == "pressure":
                readings["pressure"] = round(
                    random.uniform(205, 225), 2
                )

            elif anomaly == "temperature":
                readings["temperature"] = round(
                    random.uniform(88, 96), 2
                )

            elif anomaly == "oil_level":
                readings["oil_level"] = round(
                    random.uniform(3, 9), 2
                )

            elif anomaly == "pump_voltage":
                readings["pump_voltage"] = round(
                    random.uniform(420, 435), 2
                )

        return readings
