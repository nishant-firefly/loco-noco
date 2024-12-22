

import psycopg2
import json
import pytest
from tests.test_config import TEST_ENV_CONFIG

# Extract PostgreSQL environment configuration
DB_CONFIG = {
    "dbname": TEST_ENV_CONFIG["services"]["postgres"]["environment"]["POSTGRES_DB"],
    "user": TEST_ENV_CONFIG["services"]["postgres"]["environment"]["POSTGRES_USER"],
    "password": TEST_ENV_CONFIG["services"]["postgres"]["environment"]["POSTGRES_PASSWORD"],
    "host": "localhost",
    "port": TEST_ENV_CONFIG["services"]["postgres"]["ports"]["5432"],
}

# Load test input data
with open("D:\\workspace\\nishant\\loco_noco\\sources\\tests\\input_data.json") as f:
    TEST_DATA = json.load(f)

def execute_query(query, params=None):
    """
    Execute a query and return results.
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:  # If the query returns data (e.g., SELECT)
                return cur.fetchall()
            conn.commit()

def perform_operation(operation):
    """
    Perform a single database operation.
    """
    op_type = operation["operation"]
    table = operation["table"]
    data = operation.get("data")

    if op_type == "create":
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        execute_query(query, tuple(data.values()))

    elif op_type == "update":
        set_clause = ", ".join([f"{key} = %s" for key in data.keys() if key != "id"])
        query = f"UPDATE {table} SET {set_clause} WHERE id = %s"
        params = tuple(data[key] for key in data.keys() if key != "id") + (data["id"],)
        execute_query(query, params)

    elif op_type == "delete":
        query = f"DELETE FROM {table} WHERE id = %s"
        execute_query(query, (data["id"],))

    elif op_type == "read":
        # Read assertions are handled separately
        pass


@pytest.mark.parametrize("operation", TEST_DATA["operations"])
def test_crud_operations(operation):
    """
    Test CRUD operations using the input JSON.
    """
    if operation["operation"] != "read":
        perform_operation(operation)
    
    # Validate using expected assertions
    assertions = operation["expected_assertions"]
    actual_result = execute_query(assertions["query"])
    assert actual_result == [tuple(row.values()) for row in assertions["result"]], f"Assertion failed for {operation}"
