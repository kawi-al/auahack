import asyncio
import threading

from flask import Flask, jsonify

from monitor import WellMonitor


app = Flask(__name__)
monitor = WellMonitor()


@app.route("/")
@app.route("/dashboard")
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Oil Well Monitor</title>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 24px;
                background: #15191f;
                color: #f3f4f6;
                font-family: Arial, sans-serif;
            }

            main {
                max-width: 1100px;
                margin: 0 auto;
            }

            header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 16px;
                margin-bottom: 24px;
            }

            h1 {
                margin-bottom: 8px;
            }

            .subtitle {
                color: #aab2bf;
            }

            .status {
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
            }

            .normal {
                background: #153d30;
                color: #6ee7b7;
            }

            .alert {
                background: #512323;
                color: #fca5a5;
            }

            .grid {
                display: grid;
                grid-template-columns:
                    repeat(auto-fit, minmax(210px, 1fr));
                gap: 16px;
            }

            .card {
                background: #222831;
                border: 1px solid #343b46;
                border-radius: 12px;
                padding: 20px;
            }

            .label {
                color: #b7c0ce;
                font-size: 14px;
            }

            .value {
                margin-top: 14px;
                font-size: 32px;
                font-weight: bold;
                overflow-wrap: anywhere;
            }

            .unit {
                color: #aab2bf;
                font-size: 14px;
                margin-left: 5px;
            }

            .panel {
                margin-top: 20px;
                background: #222831;
                border: 1px solid #343b46;
                border-radius: 12px;
                padding: 20px;
            }

            #alert-list {
                white-space: pre-line;
                color: #fca5a5;
                line-height: 1.7;
            }

            #chart {
                max-height: 350px;
            }

            footer {
                margin-top: 20px;
                color: #aab2bf;
                font-size: 12px;
            }

            @media (max-width: 600px) {
                body {
                    padding: 14px;
                }
            }
        </style>
    </head>

    <body>
        <main>
            <header>
                <div>
                    <h1>🛢️ Oil Well Monitor</h1>
                    <div class="subtitle">
                        Virtual sensors and real-time monitoring
                    </div>
                </div>

                <div id="status" class="status normal">
                    Connecting...
                </div>
            </header>

            <section class="grid">
                <article class="card">
                    <div class="label">Pressure</div>
                    <div class="value">
                        <span id="pressure">--</span>
                        <span class="unit">bar</span>
                    </div>
                </article>

                <article class="card">
                    <div class="label">Temperature</div>
                    <div class="value">
                        <span id="temperature">--</span>
                        <span class="unit">°C</span>
                    </div>
                </article>

                <article class="card">
                    <div class="label">Oil Level</div>
                    <div class="value">
                        <span id="oil_level">--</span>
                        <span class="unit">%</span>
                    </div>
                </article>

                <article class="card">
                    <div class="label">Pump Voltage</div>
                    <div class="value">
                        <span id="pump_voltage">--</span>
                        <span class="unit">V</span>
                    </div>
                </article>
            </section>

            <section class="panel">
                <h2>Pressure History</h2>
                <canvas id="pressureChart"></canvas>
            </section>

            <section class="panel">
                <h2>Current Alerts</h2>
                <div id="alert-list">
                    Waiting for sensor data...
                </div>
            </section>

            <footer>
                Simulation only — all sensor readings are generated
                by software, not physical equipment.
                <div id="last-updated"></div>
            </footer>
        </main>

        <script>
            // Create the chart once, then update it with new data.
            const pressureChart = new Chart(
                document.getElementById("pressureChart"),
                {
                    type: "line",

                    data: {
                        labels: [],
                        datasets: [{
                            label: "Pressure (bar)",
                            data: [],
                            tension: 0.25,
                            fill: false
                        }]
                    },

                    options: {
                        responsive: true,
                        animation: false,

                        scales: {
                            x: {
                                ticks: { color: "#cbd5e1" },
                                grid: { color: "#343b46" }
                            },

                            y: {
                                ticks: { color: "#cbd5e1" },
                                grid: { color: "#343b46" }
                            }
                        },

                        plugins: {
                            legend: {
                                labels: { color: "#f3f4f6" }
                            }
                        }
                    }
                }
            );

            async function fetchData() {
                try {
                    const response = await fetch(
                        "/api/readings",
                        { cache: "no-store" }
                    );

                    if (!response.ok) {
                        throw new Error(
                            "Waiting for the first sensor reading"
                        );
                    }

                    const payload = await response.json();
                    const readings = payload.readings;

                    // Update the measurement cards.
                    document.getElementById("pressure").textContent =
                        readings.pressure.toFixed(2);

                    document.getElementById("temperature").textContent =
                        readings.temperature.toFixed(2);

                    document.getElementById("oil_level").textContent =
                        readings.oil_level.toFixed(2);

                    document.getElementById("pump_voltage").textContent =
                        readings.pump_voltage.toFixed(2);

                    // Update system status.
                    const statusElement =
                        document.getElementById("status");

                    if (payload.status === "ALERT") {
                        statusElement.textContent = "⚠ ALERT";
                        statusElement.className = "status alert";
                    } else {
                        statusElement.textContent = "✓ NORMAL";
                        statusElement.className = "status normal";
                    }

                    // Display the current alert messages.
                    document.getElementById("alert-list").textContent =
                        payload.alerts.length
                            ? payload.alerts.join("\\n")
                            : "All readings are within configured limits.";

                    document.getElementById("last-updated").textContent =
                        "Last reading: " +
                        new Date(readings.timestamp).toLocaleTimeString();

                    // Add this reading to the chart.
                    pressureChart.data.labels.push(
                        new Date(readings.timestamp)
                            .toLocaleTimeString()
                    );

                    pressureChart.data.datasets[0].data.push(
                        readings.pressure
                    );

                    // Retain only the latest 20 readings.
                    if (pressureChart.data.labels.length > 20) {
                        pressureChart.data.labels.shift();
                        pressureChart.data.datasets[0].data.shift();
                    }

                    pressureChart.update("none");

                } catch (error) {
                    document.getElementById("status").textContent =
                        "Connecting...";

                    document.getElementById("alert-list").textContent =
                        error.message;
                }
            }

            // Fetch new readings immediately and every two seconds.
            fetchData();
            setInterval(fetchData, 2000);
        </script>
    </body>
    </html>
    """


@app.route("/api/readings")
def api_readings():
    # The monitoring thread may need a moment to start.
    if monitor.latest_readings is None:
        return jsonify({
            "status": "STARTING",
            "readings": None,
            "alerts": [],
        }), 503

    alerts = monitor.current_alerts

    return jsonify({
        "status": "ALERT" if alerts else "NORMAL",
        "readings": monitor.latest_readings,
        "alerts": alerts,
    })


def run_monitor():
    """Run the asynchronous monitoring loop in a background thread."""
    asyncio.run(monitor.monitor_loop())


if __name__ == "__main__":
    # Start monitoring without blocking the web server.
    worker = threading.Thread(
        target=run_monitor,
        daemon=True,
    )
    worker.start()

    # Disable the reloader to prevent duplicate monitoring threads.
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False,
    )
