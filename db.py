import psycopg2
import pandas as pd

def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="test3",
        user="postgres",
        password="admin"
    )

def load_table(table_name):
    conn = get_connection()
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def load_active_rules():
    """Load active rules from the rules_catalog table"""
    conn = get_connection()
    query = "SELECT * FROM rules_catalog WHERE is_active = TRUE;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def insert_violations(violations_df, table_name="violations_log"):
    conn = get_connection()
    cursor = conn.cursor()
    for _, row in violations_df.iterrows():
        cursor.execute(
            f"""
            INSERT INTO {table_name} (row_id, column_name, rule_name, invalid_value, severity, message)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (row['row_id'], row['column_name'], row['rule_name'], row['invalid_value'], row['severity'], row['message'])
        )
    conn.commit()
    cursor.close()
    conn.close()
