import pandas as pd
from sqlalchemy import create_engine, text
# Connect to your PostgreSQL database
engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/test3")


# Step 1 - Create schema
def setup_dq_schema():
    schema_sql = """
CREATE TABLE source_employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    age INTEGER,
    email TEXT,
    phone TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
  CREATE TABLE violations_log (
    id SERIAL PRIMARY KEY,
    row_id INTEGER,                 -- Refers to the source_employees.id
    column_name TEXT,
    rule_name TEXT,
    invalid_value TEXT,
    severity TEXT CHECK (severity IN ('low', 'medium', 'high')),
    message TEXT,
    detected_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE rules_catalog (
    id SERIAL PRIMARY KEY,
    rule_name TEXT UNIQUE,
    description TEXT,
    column_name TEXT,
    severity TEXT,
    is_active BOOLEAN DEFAULT TRUE
);
"""
    with engine.connect() as conn:
        for stmt in schema_sql.split(';'):
            if stmt.strip():
                conn.execute(text(stmt))
        conn.commit()
        print("✅ Schema created")

#to populate the rule caralogue table :
""" INSERT INTO rules_catalog (rule_name, description, column_name, severity, is_active) VALUES
('Age between 18-60', 'Age must be between 18 and 60 years', 'age', 'high', TRUE),
('Email must contain @', 'Email must contain @ symbol', 'email', 'medium', TRUE),
('Phone not null', 'Phone number cannot be null', 'phone', 'high', TRUE);"""