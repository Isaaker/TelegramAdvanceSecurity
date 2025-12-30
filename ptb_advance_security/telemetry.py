# Telegram Advance Security (TAS) - Telemetry Module
from ptb_advance_security import load_config_main
def telemetry_log(event_type, details):
    ##LOAD CONFIGURATION##
    import json
    logging_config = load_config_main().get("logging_config", None)

    Security_Log = logging_config.get("Security_Log", None)
    Security_Log_enabled = logging_config.get("enabled", None)
    if Security_Log_enabled:
        log_file = logging_config.get("log_file", None)
    
    forze_https = logging_config.get("forze_https", None)
    allowed_domains = logging_config.get("allowed_domains", None)
    blacklisted_domains = logging_config.get("blacklisted_domains", None)
    owasp_implementation = logging_config.get("owasp_implementation", None)
    logging = logging_config.get("logging", None)
    ##LOAD CONFIGURATION##