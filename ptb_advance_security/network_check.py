# Telegram Advance Security (TAS) - Network Check Module
import requests
from ptb_advance_security import load_config_main, telemetry_log
def check_connection():
    ##LOAD CONFIGURATION##
    import json
    logging_config = load_config_main().get("logging_config", None)
    #Network Check Configuration
    network_checks = logging_config.get("network_checks", None)
    warp_vpn_check = network_checks.get("warp_vpn_check", None)
    warp_vpn_check_enabled = warp_vpn_check.get("enabled", None)
    if warp_vpn_check_enabled:
        on_failure = warp_vpn_check.get("on_failure", None)
        stop_bot = on_failure.get("stop_bot", None)
        send_alert = on_failure.get("send_alert", None)
        network_config = warp_vpn_check.get("network_config", None)
        type = network_config.get("type", None)
        ASN = network_config.get("ASN", None)
        IP_ranges = network_config.get("IP_ranges", None)
    ##LOAD CONFIGURATION##
        try:
            #Fetch network data from Cloudflare trace endpoint
            response = requests.get("https://www.cloudflare.com/cdn-cgi/trace")
            data = response.text
            lines = data.split("\n")
            ip_address = None
            for line in lines:
                if line.startswith("ip="):
                    ip_address = line.split("=")[1]
                    break
                if line.startswith("warp="):
                    warp_status = line.split("=")[1]
                if line.startswith("gateway="):
                    gateway_status = line.split("=")[1]
            #Fetch ASN data from ipapi.co
            asn_number = None
            if ip_address:
                asn_response = requests.get(f"https://ipapi.co/{ip_address}/json/")
                asn_data = asn_response.json()
                asn_number = asn_data.get("asn", None)
                asn_org = asn_data.get("org", None)
            #Check conditions
            if type == "warp":
                if warp_status == "off" and gateway_status == "off":
                    if send_alert:
                        telemetry_log(event_type="Warp VPN Disabled", user_id=None, details=f"Warp VPN is disabled. IP: {ip_address}")
                    if stop_bot:
                        raise SystemExit("Stopping bot due to Warp VPN being disabled.")
                if warp_status is not "off" or gateway_status is not "off":
                    if "CLOUDFLARENET" != asn_data.get("org", None):
                        if send_alert:
                            telemetry_log(event_type="Warp enabled but ASN is not Cloudflare", user_id=None, details=f"Warp VPN detected. IP: {ip_address}")
                        if stop_bot:
                            raise SystemExit("Stopping bot due to Warp VPN detection.")
            elif type == "vpn":
                if ASN is not None:
                    if asn_number and str(asn_number) == str(ASN):
                        if send_alert:
                            telemetry_log(event_type="VPN Detected", user_id=None, details=f"VPN detected with ASN: {asn_number}")
                        if stop_bot:
                            raise SystemExit("Stopping bot due to VPN detection.")
                else:
                    if ip_address:
                        for ip_range in IP_ranges:
                            if ip_address.startswith(ip_range):
                                if send_alert:
                                    telemetry_log(event_type="VPN Detected", user_id=None, details=f"VPN detected with IP: {ip_address}")
                                if stop_bot:
                                    raise SystemExit("Stopping bot due to VPN detection.")

        except Exception as e:
            print(f"Error fetching network data: {e}")
            if send_alert:
                telemetry_log(event_type="Network Check Failure", user_id=None, details=f"Error fetching network data: {e}")
            if stop_bot:
                raise SystemExit("Stopping bot due to network check failure.")
            return