import json
import os
import logging

class QueryBuilder:
    def __init__(self, auth_rules_path="D:/workspace/query_builder_project/app/config/auth_rules.json", custom_conditions_path="D:/workspace/query_builder_project/app/config/custom_conditions.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script

        if auth_rules_path is None:
            auth_rules_path = "D:/workspace/query_builder_project/app/config/auth_rules.json"
        if custom_conditions_path is None:
            custom_conditions_path = "D:/workspace/query_builder_project/app/config/custom_conditions.json"

        # Check if files exist and load them
        if not os.path.exists(auth_rules_path):
            raise FileNotFoundError(f"Authorization rules file not found: {auth_rules_path}")
        if not os.path.exists(custom_conditions_path):
            raise FileNotFoundError(f"Custom conditions file not found: {custom_conditions_path}")

        # Load authorization rules and custom conditions
        with open(auth_rules_path, "r") as file:
            self.auth_rules = json.load(file)
        with open(custom_conditions_path, "r") as file:
            self.custom_conditions = json.load(file)

    def build_query(self, request: dict, persona: str):
        operation = request.get("operation", "").lower()
        table = request.get("table")
        columns = request.get("columns", ["*"])
        clause = request.get("clause", {})
        joins = request.get("joins", [])
        aggregate = request.get("aggregate", None)
        limit = request.get("limit", None)
        offset = request.get("offset", None)
        group_by = request.get("group_by", [])
        having = request.get("having", {})

        # Authorization and column filtering
        self._check_entity_permissions(persona, table)
        columns = self._filter_columns(persona, table, columns)

        if operation == "select":
            return self._build_select_query(table, columns, clause, joins, aggregate, group_by, having, limit, offset, persona)
        elif operation == "insert":
            values = request.get("values", {})
            return self._build_insert_query(table, values)
        elif operation == "update":
            values = request.get("values", {})
            return self._build_update_query(table, values, clause)
        elif operation == "delete":
            return self._build_delete_query(table, clause)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    def _check_entity_permissions(self, persona, table):
        if table not in self.auth_rules.get(persona, {}):
            raise PermissionError(f"Persona '{persona}' does not have access to table '{table}'")

    def _filter_columns(self, persona, table, columns):
        allowed_columns = self.auth_rules.get(persona, {}).get(table, [])
        if "*" in allowed_columns:
            return columns
        return [col for col in columns if col in allowed_columns]

    def _apply_custom_conditions(self, persona, table):
        return self.custom_conditions.get(persona, {}).get(table, "")

    def _build_select_query(self, table, columns, clause, joins, aggregate, group_by, having, limit, offset, persona):
        params = []  # List to hold parameterized values

        # Select columns or aggregate
        if aggregate:
            agg_func = aggregate["function"].upper()
            agg_col = aggregate["column"]
            alias = aggregate.get("alias", "result")
            select_clause = f"{agg_func}({agg_col}) AS {alias}"
        else:
            select_clause = ", ".join(columns)

        query = f"SELECT {select_clause} FROM {table}"

        # Add joins
        for join in joins:
            join_type = join["type"].upper()
            join_table = join["table"]
            on_condition = join["on"]
            query += f" {join_type} JOIN {join_table} ON {on_condition}"

        # Add where clause
        where_conditions, where_params = self._build_where_clause(clause)
        params.extend(where_params)
        custom_conditions = self._apply_custom_conditions(persona, table)
        if custom_conditions:
            where_conditions = f"({where_conditions}) AND ({custom_conditions})" if where_conditions else f"({custom_conditions})"
        if where_conditions:
            query += f" WHERE {where_conditions}"

        # Add GROUP BY
        if group_by:
            query += f" GROUP BY {', '.join(group_by)}"

        # Add HAVING clause
        if having:
            having_conditions, having_params = self._build_where_clause(having)
            params.extend(having_params)
            if having_conditions:
                query += f" HAVING {having_conditions}"

        # Add limit and offset
        if limit:
            query += f" LIMIT ?"
            params.append(limit)
        if offset:
            query += f" OFFSET ?"
            params.append(offset)

        return query, params

    def _build_where_clause(self, clause):
        def process_conditions(conditions):
            processed = []
            params = []
            for key, value in conditions.items():
                if key in ["AND", "OR"]:  # Handle logical operators
                    nested_conditions, nested_params = process_conditions(value)
                    processed.append(f"({nested_conditions})")
                    params.extend(nested_params)
                elif isinstance(value, dict):  # Handle operators like IN, >, etc.
                    operator = value.get("operator", "=").upper()
                    val = value.get("value")
                    if operator == "BETWEEN":
                        if isinstance(val, list) and len(val) == 2:
                            processed.append(f"{key} BETWEEN ? AND ?")
                            params.extend(val)
                        else:
                            raise ValueError("BETWEEN operator requires a list of two values")
                    elif operator == "LIKE":
                        processed.append(f"{key} LIKE ?")
                        params.append(val)
                    elif operator in ["IN", "NOT IN"]:
                        placeholders = ", ".join(["?" for _ in val])
                        processed.append(f"{key} {operator} ({placeholders})")
                        params.extend(val)
                    else:
                        processed.append(f"{key} {operator} ?")
                        params.append(val)
                else:
                    processed.append(f"{key} = ?")
                    params.append(value)
            return " AND ".join(processed) if conditions else None, params

        return process_conditions(clause)

    def _build_insert_query(self, table, values):
        keys = ", ".join(values.keys())
        placeholders = ", ".join(["?" for _ in values.values()])
        params = list(values.values())
        query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        return query, params

    def _build_update_query(self, table, values, clause):
        set_clause = ", ".join(f"{key} = ?" for key in values.keys())
        params = list(values.values())
        where_clause, where_params = self._build_where_clause(clause)
        params.extend(where_params)

        # Add is_active condition
        is_active_condition = "AND (is_active = 1)"  # You can adjust this condition as per your logic
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause} {is_active_condition}"
        return query, params

    def _build_delete_query(self, table, clause):
        where_clause, params = self._build_where_clause(clause)

        # Add is_active condition
        is_active_condition = "AND (is_active = 1)"  # You can adjust this condition as per your logic
        query = f"DELETE FROM {table} WHERE {where_clause} {is_active_condition}"
        return query, params



    @staticmethod
    def generate_query(persona, table, clause):
        qb = QueryBuilder()
        
        # Construct the request dictionary based on input
        request = {
            "operation": "select",
            "table": table,
            "columns": qb.auth_rules.get(persona, {}).get(table, ["*"]),  # Get authorized columns for persona
            "clause": clause
        }
        
        # Use the QueryBuilder class to build the query
        query, params = qb.build_query(request, persona)
        return query, params


if __name__ == "__main__":
    # Example usage
    try:
        qb = QueryBuilder()
        
        request = {
            "operation": "select",
            "table": "users",
            "columns": ["id", "name"],
            "clause": {
                "id": {"operator": ">", "value": 10},
                "name": {"operator": "LIKE", "value": "%John%"}
            },
            "limit": 5,
            "offset": 0
        }
        persona = "admin"

        query, params = qb.build_query(request, persona)
        print("Generated Query:", query)
        print("Parameters:", params)
    except Exception as e:
        print("Error:", e)








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













