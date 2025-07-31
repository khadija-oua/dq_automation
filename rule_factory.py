from validator import Rule
import pandas as pd

def create_rule_function(rule_name):
    """Create validation functions based on rule names"""
    rule_functions = {
        "Age between 18-60": lambda x: 18 <= x <= 60 if pd.notnull(x) else False,
        "Email must contain @": lambda x: "@" in str(x) if pd.notnull(x) else False,
        "Phone not null": lambda x: pd.notnull(x),
        "Name not empty": lambda x: len(str(x).strip()) > 0 if pd.notnull(x) else False,
        "Valid email format": lambda x: "@" in str(x) and "." in str(x) if pd.notnull(x) else False,
    }
    return rule_functions.get(rule_name, lambda x: True)  # Default to always pass if rule not found

def create_rules_from_catalog(rules_df):
    """Convert database rules to Rule objects"""
    rules = []
    for _, row in rules_df.iterrows():
        func = create_rule_function(row['rule_name'])
        rule = Rule(
            name=row['rule_name'],
            func=func,
            column=row['column_name'],
            severity=row['severity']
        )
        rules.append(rule)
    return rules