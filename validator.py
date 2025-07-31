import pandas as pd

class Rule:
    def __init__(self, name, func, column, severity="low"):
        self.name = name
        self.func = func
        self.column = column
        self.severity = severity
    
    def apply(self, df):
        invalid_mask = ~df[self.column].apply(self.func)
        violations = df[invalid_mask].copy()
        violations["row_id"] = df[invalid_mask].index
        violations["column_name"] = self.column
        violations["rule_name"] = self.name
        violations["invalid_value"] = df[invalid_mask][self.column]
        violations["severity"] = self.severity
        violations["message"] = f"{self.name} failed on column '{self.column}'"
        return violations[["row_id", "column_name", "rule_name", "invalid_value", "severity", "message"]]