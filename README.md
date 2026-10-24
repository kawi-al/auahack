# auahack
A real-time oil well monitoring prototype built with Python. The system simulates oil well sensor data, monitors operating conditions, detects abnormal readings, and can send alerts to a Telegram bot @sornyak_bot . 

> **Note:** This project currently supports simulated sensor data. It is a demonstration prototype, not a system connected to real industrial equipment.

## 1. Clone or Download the Project

If the project is hosted in a Git repository:

```bash
git clone https://github.com/kawi-al/auahack.git
cd oil_well
```

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If virtual environment creation fails because `venv` is unavailable, install the appropriate Python venv package for your distribution and retry.

## 3. Install Dependencies

Install the dependencies required by the files you plan to run:

```bash
python -m pip install python-dotenv
```


For the local Flask dashboard, if `app.py` uses Flask:

```bash
python -m pip install flask
```


## 4. Run the Local Web Dashboard 

If `app.py` contains the Flask dashboard. run:

```bash
python app.py
```

Open the local address printed by Flask.
Start the Telegram bot @sornyak_bot , alerts should be sent there.
**Project:** Oil Well Monitoring System in Python  
**Purpose:** Educational prototype for oil well monitoring, anomaly detection, and remote visualization.
