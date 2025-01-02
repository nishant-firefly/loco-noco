import pandas as pd


class QueryBuilder:
    def __init__(self, auth_rules, custom_conditions):
        self.auth_rules = auth_rules
        self.custom_conditions = custom_conditions

    def get_columns(self, persona, table):
        """Retrieve accessible columns for a persona on a table."""
        return self.auth_rules.get((persona, table), [])

    def get_conditions(self, persona, table):
        """Retrieve custom conditions for a persona on a table."""
        return self.custom_conditions.get((persona, table), '')



    def sanitize_input(self, input_value):
        """Sanitize input to prevent SQL injection."""
        if any(char in input_value for char in (';', '--', "'", '"')):
            raise PermissionError("Potential SQL injection detected.")
        return input_value

    def select(self, persona, table, where=None):
        """Build a SELECT query."""
        columns = self.get_columns(persona, table)
        if not columns:
            raise PermissionError(f"No access to table: {table} for persona: {persona}")

        column_str = ', '.join(columns) if '*' not in columns else '*'
        condition = self.get_conditions(persona, table)

        if where:
            where = self.sanitize_input(where)

        where_clause = f"WHERE {condition}" if condition else ''
        if where:
            where_clause += f" AND {where}" if where_clause else f"WHERE {where}"

        query = f"SELECT {column_str} FROM {table} {where_clause}".strip() + ';'
        return query

    # Other methods (update, delete) should also call `sanitize_input` for `where` and similar fields.


    def insert(self, persona, table, values):
        """Build an INSERT query."""
        columns = self.get_columns(persona, table)
        if not columns:
            raise PermissionError(f"Insert not allowed on table: {table} for persona: {persona}")

        if '*' in columns:
            keys = ', '.join(values.keys())
            vals = ', '.join([repr(v) for v in values.values()])
            query = f"INSERT INTO {table} ({keys}) VALUES ({vals})".strip() + ';'
            return query

        # For non-admins, restrict keys to allowed columns
        keys = ', '.join([k for k in values.keys() if k in columns])
        vals = ', '.join([repr(values[k]) for k in values.keys() if k in columns])
        if not keys:
            raise PermissionError(f"No columns allowed for insert on table: {table} for persona: {persona}")

        query = f"INSERT INTO {table} ({keys}) VALUES ({vals})".strip() + ';'
        return query

    def update(self, persona, table, updates, where=None):
        """Build an UPDATE query."""
        columns = self.get_columns(persona, table)

        if '*' in columns:
            set_clause = ', '.join([f"{k}={repr(v)}" for k, v in updates.items()])
        else:
            set_clause = ', '.join([f"{k}={repr(v)}" for k, v in updates.items() if k in columns])
            if not set_clause:
                raise PermissionError(f"No valid columns to update for persona: {persona}")

        condition = self.get_conditions(persona, table)
        where_clause = f"WHERE {condition}" if condition else ''
        if where:
            where_clause += f" AND {where}" if where_clause else f"WHERE {where}"

        query = f"UPDATE {table} SET {set_clause} {where_clause}".strip() + ';'
        return query


    def delete(self, persona, table, where=None):
        """
        Build a DELETE query.
        :param persona: The user's role or persona.
        :param table: The name of the table.
        :param where: Conditions for the delete operation.
        :return: The constructed DELETE SQL query.
        """
        # Check if the persona has access to the table
        columns = self.get_columns(persona, table)
        if not columns or '*' not in columns:
            raise PermissionError(f"Delete not allowed on table '{table}' for persona '{persona}'.")

        # Ensure a WHERE clause is provided
        if not where or where.strip() == "":
            raise ValueError("DELETE queries must include a WHERE clause to prevent accidental data loss.")

        # Apply custom conditions if any
        condition = self.get_conditions(persona, table)
        where_clause = f"WHERE {condition}" if condition else ''
        if where:
            where_clause += f" AND {where}" if where_clause else f"WHERE {where}"

        # Construct the query
        query = f"DELETE FROM {table} {where_clause}".strip() + ';'
        return query


# Load Excel data
data_path = r"D:\workspace\query_builder_project\app\config\mnt\data\mock_data.xlsx"
auth_rules_df = pd.read_excel(data_path, sheet_name='auth_rules')
custom_conditions_df = pd.read_excel(data_path, sheet_name='custom_conditions')

# Process auth_rules into a dictionary
auth_rules = {
    (row['persona'], row['table']): row['columns'].split(', ') if row['columns'] != '*' else ['*']
    for _, row in auth_rules_df.iterrows() if pd.notna(row['columns'])
}

# Process custom_conditions into a dictionary
custom_conditions = {
    (row['persona'], row['table']): row['columns'] if pd.notna(row['columns']) else ''
    for _, row in custom_conditions_df.iterrows()
}

# Initialize QueryBuilder
query_builder = QueryBuilder(auth_rules, custom_conditions)

# Debugging Prints
print("Auth Rules Loaded:", auth_rules)
print("Custom Conditions Loaded:", custom_conditions)

# Examples
print(query_builder.select('user', 'product', where="price > 100"))
print(query_builder.insert('admin', 'product', values={'id': 3, 'name': 'Tablet', 'price': 600}))
print(query_builder.update('admin', 'product', updates={'price': 1200}, where="id=2"))
print(query_builder.delete('admin', 'product', where="id=3"))











# import json
# import os
# import logging

# class QueryBuilder:
#     def __init__(self, 
#                  auth_rules_path="D:/workspace/query_builder_project/app/config/auth_rules.json", 
#                  custom_conditions_path="D:/workspace/query_builder_project/app/config/custom_conditions.json", 
#                  input_data_path="D:/workspace/query_builder_project/app/config/input_data.json"):
#         base_dir = os.path.dirname(os.path.abspath(__file__))

#         if auth_rules_path is None:
#             auth_rules_path = "D:/workspace/query_builder_project/app/config/auth_rules.json"
#         if custom_conditions_path is None:
#             custom_conditions_path = "D:/workspace/query_builder_project/app/config/custom_conditions.json"
#         if input_data_path is None:
#             input_data_path = "D:/workspace/query_builder_project/app/config/input_data.json"

#         # Check if files exist and load them
#         if not os.path.exists(auth_rules_path):
#             raise FileNotFoundError(f"Authorization rules file not found: {auth_rules_path}")
#         if not os.path.exists(custom_conditions_path):
#             raise FileNotFoundError(f"Custom conditions file not found: {custom_conditions_path}")
#         if not os.path.exists(input_data_path):
#             raise FileNotFoundError(f"Input data file not found: {input_data_path}")

#         # Load authorization rules, custom conditions, and input data
#         with open(auth_rules_path, "r") as file:
#             self.auth_rules = json.load(file)
#         with open(custom_conditions_path, "r") as file:
#             self.custom_conditions = json.load(file)
#         with open(input_data_path, "r") as file:
#             self.input_data = json.load(file)

#     def build_query(self, request: dict, persona: str):
#         operation = request.get("operation", "").lower()
#         table = request.get("table")
#         columns = request.get("columns", ["*"])
#         clause = request.get("clause", {})
#         joins = request.get("joins", [])
#         aggregate = request.get("aggregate", None)
#         limit = request.get("limit", None)
#         offset = request.get("offset", None)
#         group_by = request.get("group_by", [])
#         having = request.get("having", {})

#         # Authorization and column filtering
#         self._check_entity_permissions(persona, table)
#         columns = self._filter_columns(persona, table, columns)

#         if operation == "select":
#             return self._build_select_query(table, columns, clause, joins, aggregate, group_by, having, limit, offset, persona)
#         elif operation == "insert":
#             values = request.get("values", {})
#             return self._build_insert_query(table, values)
#         elif operation == "update":
#             values = request.get("values", {})
#             return self._build_update_query(table, values, clause)
#         elif operation == "delete":
#             return self._build_delete_query(table, clause)
#         else:
#             raise ValueError(f"Unsupported operation: {operation}")

#     def _check_entity_permissions(self, persona, table):
#         if table not in self.auth_rules.get(persona, {}):
#             raise PermissionError(f"Persona '{persona}' does not have access to table '{table}'")

#     def _filter_columns(self, persona, table, columns):
#         allowed_columns = self.auth_rules.get(persona, {}).get(table, [])
#         if "*" in allowed_columns:
#             return columns
#         return [col for col in columns if col in allowed_columns]

#     def _apply_custom_conditions(self, persona, table):
#         return self.custom_conditions.get(persona, {}).get(table, "")

#     def _build_select_query(self, table, columns, clause, joins, aggregate, group_by, having, limit, offset, persona):
#         params = []  # List to hold parameterized values

#         # Select columns or aggregate
#         if aggregate:
#             agg_func = aggregate["function"].upper()
#             agg_col = aggregate["column"]
#             alias = aggregate.get("alias", "result")
#             select_clause = f"{agg_func}({agg_col}) AS {alias}"
#         else:
#             select_clause = ", ".join(columns)

#         query = f"SELECT {select_clause} FROM {table}"

#         # Add joins
#         for join in joins:
#             join_type = join["type"].upper()
#             join_table = join["table"]
#             on_condition = join["on"]
#             query += f" {join_type} JOIN {join_table} ON {on_condition}"

#         # Add where clause
#         where_conditions, where_params = self._build_where_clause(clause)
#         params.extend(where_params)
#         custom_conditions = self._apply_custom_conditions(persona, table)
#         if custom_conditions:
#             where_conditions = f"({where_conditions}) AND ({custom_conditions})" if where_conditions else f"({custom_conditions})"
#         if where_conditions:
#             query += f" WHERE {where_conditions}"

#         # Add GROUP BY
#         if group_by:
#             query += f" GROUP BY {', '.join(group_by)}"

#         # Add HAVING clause
#         if having:
#             having_conditions, having_params = self._build_where_clause(having)
#             params.extend(having_params)
#             if having_conditions:
#                 query += f" HAVING {having_conditions}"

#         # Add limit and offset
#         if limit:
#             query += f" LIMIT ?"
#             params.append(limit)
#         if offset:
#             query += f" OFFSET ?"
#             params.append(offset)

#         return query, params

#     def _build_where_clause(self, clause):
#         def process_conditions(conditions):
#             processed = []
#             params = []
#             for key, value in conditions.items():
#                 if key in ["AND", "OR"]:  # Handle logical operators
#                     nested_conditions, nested_params = process_conditions(value)
#                     processed.append(f"({nested_conditions})")
#                     params.extend(nested_params)
#                 elif isinstance(value, dict):  # Handle operators like IN, >, etc.
#                     operator = value.get("operator", "=").upper()
#                     val = value.get("value")
#                     if operator == "BETWEEN":
#                         if isinstance(val, list) and len(val) == 2:
#                             processed.append(f"{key} BETWEEN ? AND ?")
#                             params.extend(val)
#                         else:
#                             raise ValueError("BETWEEN operator requires a list of two values")
#                     elif operator == "LIKE":
#                         processed.append(f"{key} LIKE ?")
#                         params.append(val)
#                     elif operator in ["IN", "NOT IN"]:
#                         placeholders = ", ".join(["?" for _ in val])
#                         processed.append(f"{key} {operator} ({placeholders})")
#                         params.extend(val)
#                     else:
#                         processed.append(f"{key} {operator} ?")
#                         params.append(val)
#                 else:
#                     processed.append(f"{key} = ?")
#                     params.append(value)
#             return " AND ".join(processed) if conditions else None, params

#         return process_conditions(clause)

#     def _build_insert_query(self, table, values):
#         keys = ", ".join(values.keys())
#         placeholders = ", ".join(["?" for _ in values.values()])
#         params = list(values.values())
#         query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
#         return query, params

#     def _build_update_query(self, table, values, clause):
#         set_clause = ", ".join(f"{key} = ?" for key in values.keys())
#         params = list(values.values())
#         where_clause, where_params = self._build_where_clause(clause)
#         params.extend(where_params)

#         # Ensure there is a valid WHERE clause
#         if where_clause:
#             query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
#         else:
#             query = f"UPDATE {table} SET {set_clause}"  # Optional: Decide how to handle no WHERE condition

#         # Add is_active condition if needed
#         query += " AND (is_active = 1)"  # You can adjust this as needed
#         return query, params

#     def _build_delete_query(self, table, clause):
#         where_clause, params = self._build_where_clause(clause)

#         # Ensure there is a valid WHERE clause
#         if where_clause:
#             query = f"DELETE FROM {table} WHERE {where_clause}"
#         else:
#             query = f"DELETE FROM {table}"  # Optional: Decide how to handle no WHERE condition

#         # Add is_active condition if needed
#         query += " AND (is_active = 1)"  # You can adjust this as needed
#         return query, params


#     def process_operations(self):
#         results = []
#         for operation_data in self.input_data.get("operations", []):
#             try:
#                 operation = operation_data.get("operation")
#                 table = operation_data.get("table")
#                 data = operation_data.get("data", {})
#                 expected_assertions = operation_data.get("expected_assertions", {})

#                 request = {
#                     "operation": operation,
#                     "table": table,
#                     "values": data,
#                     "clause": data.get("clause", {})
#                 }

#                 # Generate query based on request
#                 persona = "admin"  # Example persona
#                 query, params = self.build_query(request, persona)

#                 results.append({
#                     "query": query,
#                     "params": params,
#                     "expected_assertions": expected_assertions
#                 })

#             except Exception as e:
#                 results.append({
#                     "error": str(e),
#                     "operation_data": operation_data
#                 })

#         return results

# if __name__ == "__main__":
#     try:
#         qb = QueryBuilder()
#         results = qb.process_operations()

#         for result in results:
#             print(json.dumps(result, indent=4))

#     except Exception as e:
#         print("Error:", e)













