from db import load_table, insert_violations, load_active_rules
from rule_factory import create_rules_from_catalog
import pandas as pd

def run_validation():
    # Load data and active rules from database
    df = load_table("source_employees")
    rules_df = load_active_rules()
    
    if rules_df.empty:
        print("No active rules found in rules_catalog table.")
        return
    
    # Create Rule objects from database
    rules = create_rules_from_catalog(rules_df)
    
    all_violations = []
    
    for rule in rules:
        violations = rule.apply(df)
        if not violations.empty:
            all_violations.append(violations)
    
    if all_violations:
        final_df = pd.concat(all_violations, ignore_index=True)
        insert_violations(final_df)
        print(f"{len(final_df)} violations found and logged.")
    else:
        print("No violations found.")

if __name__ == "__main__":
    run_validation()