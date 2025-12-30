# Telegram Advance Security (TAS) - OWASP Rules Module
def owasp_load_rules(rule):
    # Load OWASP rules here
    rules_name = {"restricted_files": "restricted-files.data", "sql_errors": "sql-errors.data"}
    rule_file = rules_name.get(rule, None)
    if rule_file:
        with open(f"ptb_advance_security/owasp_data/{rule_file}", "r") as f:
            rules = f.read().splitlines()
            for rules in rules:
                if rules.startswith("#") or not rules.strip():
                    rules.remove(rules)
        return rules