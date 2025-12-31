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

    manual_settings = safe_requests.get("manual_settings", None)
    manual_settings_enabled = manual_settings.get("enabled", None)
    if manual_settings:
        X_XSS_Protection = manual_settings.get("X-XSS-Protection", None)
        mode = manual_settings.get("mode", None)
        cross_origin_isolated = manual_settings.get("cross_origin_isolated", None)
        Cache_Control = manual_settings.get("Cache-Control:", None)
        Content_Security_Policy = manual_settings.get("Content-Security-Policy", None)
        Referrer_Policy = manual_settings.get("Referrer-Policy", None)
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

            if manual_settings_enabled:
                if X_XSS_Protection and mode:
                    drheader.analyze(x_xss_protection=X_XSS_Protection, mode=mode)
                if Cache_Control:
                    drheader.analyze(cache_control=Cache_Control)
                if Content_Security_Policy:
                    drheader.analyze(content_security_policy=Content_Security_Policy)
                if Referrer_Policy:
                    drheader.analyze(referrer_policy=Referrer_Policy)
            else:
                drheader.analyze(cross_origin_isolated=True)
                drheader.analyze(x_xss_protection=X_XSS_Protection, mode="block")
                drheader.analyze(cache_control="no-cache")
                drheader.analyze(content_security_policy="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'")
                drheader.analyze(referrer_policy="strict-origin-when-cross-origin")
            report = drheader.report()
            if logging:
                print("Security Headers Analysis Report:")
                print(report)
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None