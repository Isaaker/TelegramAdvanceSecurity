# Telegram Advance Security (TAS) - Load Configuration Module
import json

def read_config_quarantine():
    #The config file loaded here SHOULD NOT be trusted by the system
    with open("config.json", "r") as file:
        config_data = json.load(file)
    return config_data

def load_config_main():
    with open("config.json", "r") as file:
        config_data = json.load(file)
    return config_data