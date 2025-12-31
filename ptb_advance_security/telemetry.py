# Telegram Advance Security (TAS) - Telemetry Module
from ptb_advance_security import load_config_main
import os

def telemetry_log(event_type, user_id, details):
    ##LOAD CONFIGURATION##
    import json
    logging_config = load_config_main().get("logging_config", None)

    #Security Log Configuration
    Security_Log = logging_config.get("Security_Log", None)
    Security_Log_enabled = logging_config.get("enabled", None)
    if Security_Log_enabled:
        log_file = logging_config.get("log_file", None)
    
    #Telegram Bot Telemetry Configuration
    telegram_bot_telemetry = logging_config.get("telegram_bot_telemetry", None)
    telegram_bot_telemetry_enabled = telegram_bot_telemetry.get("enabled", None)
    if telegram_bot_telemetry_enabled:
        bot_token_env = telegram_bot_telemetry.get("bot_VARIABLE_TOKEN", None)
        bot_token = os.getenv(bot_token_env)
        chat_id_admin = telegram_bot_telemetry.get("chat_id_admin", None)
    
    #Telemetry Services Configuration
    telemetry_services = logging_config.get("telemetry_services", None)
    telemetry_services_enabled = telemetry_services.get("enabled", None)
    if telemetry_services_enabled:
        service_name = telemetry_services.get("service_name", None)
        auth = telemetry_services.get("auth", None)
        if service_name == "grafana":
            grafana_url = auth.get("endpoint", None)
            grafana_api_key_env = auth.get("grafana_api_key", None)
            grafana_api_key = os.getenv(grafana_api_key_env)
        elif service_name == "prometheus":
            prometheus_url = auth.get("endpoint", None)
        elif service_name == "datadog":
            datadog_api_key_env = auth.get("datadog_api_key", None)
            datadog_api_key = os.getenv(datadog_api_key_env)
            datadog_application_key_env = auth.get("datadog_application_key", None)
            datadog_application_key = os.getenv(datadog_application_key_env)

    #Telemetry Connection Failure
    on_failure = logging_config.get("on_failure", None)
    on_failure_enabled = on_failure.get("enabled", None)
    if on_failure_enabled:
        stop_bot = on_failure.get("stop_bot", None)
        max_retries = on_failure.get("max_retries", None)
        retry_interval_seconds = on_failure.get("retry_interval_seconds", None)
    ##LOAD CONFIGURATION##

    ##LOAD EVENT DATA##
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] - {event_type} - {details}\n"
    ##LOAD EVENT DATA##

    ##LOG TO FILE##
    if Security_Log_enabled:
        Security_Log_tries = 0
        while True:
            try:
                with open(log_file, "a") as f:
                    f.write(log_entry)
                break
            except Exception as e:
                print(f"Error logging to file: {e}")
                if on_failure_enabled and max_retries > 0:
                    Security_Log_tries += 1
                    if Security_Log_tries >= max_retries:
                        if stop_bot:
                            raise SystemExit("Max retries reached. Stopping bot.")
                        break
                    import time
                    time.sleep(retry_interval_seconds)
                else:
                    if stop_bot:
                        raise SystemExit("Logging failed. Stopping bot.")
    ##LOG TO FILE##

    ##TELEGRAM BOT TELEMETRY##
    if telegram_bot_telemetry_enabled:
        while True:
            Security_Telegram_tries = 0
            try:
                import requests
                telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                if user_id is not None:
                    message = f"Telemetry Event - {user_id}\n{event_type}:\n{details}"
                else:
                    message = f"Telemetry Event\n{event_type}:\n{details}"
                headers = {
                    "Content-Type": "application/json"
                }
                payload = {
                    "chat_id": chat_id_admin,
                    "text": message
                }
                response = requests.post(telegram_api_url, headers=headers, json=payload)
                response.raise_for_status()
                break
            except Exception as e:
                print(f"Error sending telemetry to Telegram bot: {e}")
                if on_failure_enabled and max_retries > 0:
                    Security_Telegram_tries += 1
                    if Security_Telegram_tries >= max_retries:
                        if stop_bot:
                            raise SystemExit("Max retries reached. Stopping bot.")
                        break
                    import time
                    time.sleep(retry_interval_seconds)
                else:
                    if stop_bot:
                        raise SystemExit("Logging failed. Stopping bot.")
    ##TELEGRAM BOT TELEMETRY##

    ##TELEMETRY SERVICES##
    if telemetry_services_enabled:
        while True:
            Security_Service_tries = 0
            try:
                import requests
                if service_name == "grafana":
                    grafana_api_url = f"{grafana_url}/api/annotations"
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {grafana_api_key}"
                    }
                    payload = {
                        "time": int(datetime.now().timestamp() * 1000),
                        "tags": [event_type],
                        "text": details
                    }
                    response = requests.post(grafana_api_url, headers=headers, json=payload)
                elif service_name == "prometheus":
                    prometheus_api_url = f"{prometheus_url}/api/v1/annotations"
                    headers = {
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "time": int(datetime.now().timestamp()),
                        "tags": [event_type],
                        "text": details
                    }
                    response = requests.post(prometheus_api_url, headers=headers, json=payload)
                elif service_name == "datadog":
                    datadog_api_url = "https://api.datadoghq.com/api/v1/events"
                    headers = {
                        "Content-Type": "application/json",
                        "DD-API-KEY": datadog_api_key,
                        "DD-APPLICATION-KEY": datadog_application_key
                    }
                    payload = {
                        "title": f"Telemetry Event - {event_type}",
                        "text": details,
                        "tags": [event_type]
                    }
                    response = requests.post(datadog_api_url, headers=headers, json=payload)
                response.raise_for_status()
                break
            except Exception as e:
                print(f"Error sending telemetry to {service_name}: {e}")
                if on_failure_enabled and max_retries > 0:
                    Security_Service_tries += 1
                    if Security_Service_tries >= max_retries:
                        if stop_bot:
                            raise SystemExit("Max retries reached. Stopping bot.")
                        break
                    import time
                    time.sleep(retry_interval_seconds)
                else:
                    if stop_bot:
                        raise SystemExit("Logging failed. Stopping bot.")
    