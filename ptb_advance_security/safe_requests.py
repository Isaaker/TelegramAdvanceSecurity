# Telegram Advance Security (TAS) - Safe Requests Module
import requests
from ptb_advance_security import load_config_main
from drheader import Drheader

def request_url(url, headers, timeout):
    ##LOAD CONFIGURATION##
    import json
    safe_requests = load_config_main().get("safe_requests", None)
    
    enabled = safe_requests.get("enabled", None)
    user_agent = safe_requests.get("user_agent", None)
    forze_https = safe_requests.get("forze_https", None)
    allowed_domains = safe_requests.get("allowed_domains", None)
    blacklisted_domains = safe_requests.get("blacklisted_domains", None)
    owasp_implementation = safe_requests.get("owasp_implementation", None)
    logging = safe_requests.get("logging", None)
    ##LOAD CONFIGURATION##
    if not enabled:
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    else:
        # Apply security checks and return the response
        if forze_https and not url.startswith("https://"):
            print("HTTPS is required.")
            return None

        if allowed_domains and not any(domain in url for domain in allowed_domains):
            print("Domain is not allowed.")
            return None

        if blacklisted_domains and any(domain in url for domain in blacklisted_domains):
            print("Domain is blacklisted.")
            return None
        
        if owasp_implementation:
            # LOAD OWASP RULES
            restricted_files = owasp_load_rules("restricted_files")

            if any(restricted_file in url for restricted_file in restricted_files):
                print("Access to restricted file is blocked.")
                return None

        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()

            # SCAN RESPONSE HEADERS USING DRHEADER
            drheader = Drheader()
            drheader.scan_response(response)

            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None