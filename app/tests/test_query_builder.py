import unittest
import pandas as pd

from query_builder import QueryBuilder

from unittest.mock import patch, MagicMock

class TestQueryBuilder(unittest.TestCase):
    def setUp(self):
        # Paths to test Excel files
        self.mock_data_path = "D:/workspace/query_builder_project/app/config/mock_data.xlsx"
        self.operations_file_path = "D:/workspace/query_builder_project/app/config/operations.xlsx"
        self.qb = QueryBuilder(mock_data_path=self.mock_data_path, operations_file_path=self.operations_file_path)

    @patch("pandas.read_excel")
    def test_load_mock_data(self, mock_read_excel):
        # Mocking pandas.read_excel to simulate Excel data
        mock_read_excel.side_effect = [
            pd.DataFrame({"persona": ["admin"], "table": ["users"], "columns": [["id", "name"]]}),
            pd.DataFrame({"persona": ["admin"], "condition": ["status='active'"]}),
        ]

        auth_rules, custom_conditions = self.qb._load_mock_data()
        self.assertIn("admin", auth_rules)
        self.assertIn("admin", custom_conditions)

    @patch("pandas.read_excel")
    def test_load_operations_excel(self, mock_read_excel):
        # Mocking pandas.read_excel for operations
        mock_read_excel.return_value = pd.DataFrame([{"operation": "select", "table": "users"}])

        operations = self.qb._load_operations_excel()
        self.assertTrue(len(operations) > 0)
        self.assertEqual(operations[0]["operation"], "select")

    def test_build_select_query(self):
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

        with patch.object(self.qb, "_filter_columns", return_value=["id", "name"]):
            query, params = self.qb.build_query(request, persona)
            self.assertTrue("SELECT id, name FROM users" in query)
            self.assertEqual(params, [10, "%John%", 5, 0])

    def test_build_insert_query(self):
        request = {
            "operation": "insert",
            "table": "users",
            "values": {"id": 1, "name": "John Doe"}
        }

        query, params = self.qb._build_insert_query("users", request["values"])
        self.assertTrue("INSERT INTO users (id, name) VALUES (?, ?)" in query)
        self.assertEqual(params, [1, "John Doe"])

    def test_build_update_query(self):
        request = {
            "operation": "update",
            "table": "users",
            "values": {"name": "John Updated"},
            "clause": {"id": {"operator": "=", "value": 1}}
        }

        query, params = self.qb._build_update_query("users", request["values"], request["clause"])
        self.assertTrue("UPDATE users SET name = ? WHERE id = ?" in query)
        self.assertEqual(params, ["John Updated", 1])

    def test_build_delete_query(self):
        request = {
            "operation": "delete",
            "table": "users",
            "clause": {"id": {"operator": "=", "value": 1}}
        }

        query, params = self.qb._build_delete_query("users", request["clause"])
        self.assertTrue("DELETE FROM users WHERE id = ?" in query)
        self.assertEqual(params, [1])

    def test_generate_query(self):
        with patch.object(self.qb, "_filter_columns", return_value=["id", "name"]):
            query, params = self.qb.generate_query("admin", "users", {"id": {"operator": "=", "value": 1}})
            self.assertTrue("SELECT id, name FROM users WHERE id = ?" in query)
            self.assertEqual(params, [1])

    def test_check_entity_permissions(self):
        self.qb.auth_rules = {"admin": {"users": ["id", "name"]}}
        with self.assertRaises(PermissionError):
            self.qb._check_entity_permissions("guest", "users")

    def test_filter_columns(self):
        self.qb.auth_rules = {"admin": {"users": ["id", "name"]}}
        filtered_columns = self.qb._filter_columns("admin", "users", ["id", "name", "email"])
        self.assertEqual(filtered_columns, ["id", "name"])

if __name__ == "__main__":
    unittest.main()








# import json
# import pytest
# from app.query_builder import QueryBuilder

# # Mock Data for Testing
# auth_rules = {
#     "user": {
#         "product": ["id", "name", "price"],
#         "category": ["id", "name"]
#     },
#     "admin": {
#         "product": ["*"],  # admin can access all columns
#         "category": ["*"]
#     }
# }

# custom_conditions = {
#     "user": {
#         "product": "is_active = 1",
#         "category": "is_active = 1"
#     },
#     "admin": {
#         "product": "",
#         "category": ""
#     }
# }

# # Mock paths to pass when initializing QueryBuilder
# @pytest.fixture
# def query_builder():
#     # Use the mock data for testing purposes
#     query_builder = QueryBuilder(auth_rules_path=None, custom_conditions_path=None)
#     query_builder.auth_rules = auth_rules
#     query_builder.custom_conditions = custom_conditions
#     return query_builder



# def test_select_query_with_joins(query_builder):
#     # Test: SELECT query with JOIN
#     request = {
#         "operation": "select",
#         "table": "product",
#         "columns": ["id", "name", "price"],
#         "clause": {
#             "price": {"operator": ">", "value": 100},
#             "category_id": {"operator": "IN", "value": [1, 2, 3]}
#         },
#         "joins": [
#             {"type": "INNER", "table": "category", "on": "product.category_id = category.id"}
#         ],
#         "limit": 10,
#         "offset": 5
#     }
#     persona = "user"
#     query, params = query_builder.build_query(request, persona)

#     # Expected query structure with placeholders
#     expected_query = (
#         "SELECT id, name, price FROM product "
#         "INNER JOIN category ON product.category_id = category.id "
#         "WHERE (price > ? AND category_id IN (?, ?, ?)) AND (is_active = 1) "
#         "LIMIT ? OFFSET ?"
#     )
    
#     # Expected parameters for the query
#     expected_params = [100, 1, 2, 3, 10, 5]
    
#     # Check that the query matches the structure
#     assert query == expected_query, f"Expected query: {expected_query}, but got: {query}"
    
#     # Check that the parameters match the expected values
#     assert params == expected_params, f"Expected params: {expected_params}, but got: {params}"




  

# def test_insert_query(query_builder):
#     # Test: INSERT query
#     request = {
#         "operation": "insert",
#         "table": "product",
#         "values": {
#             "name": "New Product",
#             "price": 200,
#             "category_id": 1
#         }
#     }
#     persona = "user"
#     query, params = query_builder.build_query(request, persona)  # Assuming QueryBuilder returns (query, params)

#     expected_query = "INSERT INTO product (name, price, category_id) VALUES (?, ?, ?)"
#     expected_params = ["New Product", 200, 1]

#     # Validate query structure and parameter values
#     assert query == expected_query
#     assert params == expected_params





# def test_update_query(query_builder):
#     # Test: UPDATE query
#     request = {
#         "operation": "update",
#         "table": "product",
#         "values": {
#             "price": 250
#         },
#         "clause": {
#             "id": 1
#         }
#     }
#     persona = "user"
#     query, params = query_builder.build_query(request, persona)
#     expected_query = "UPDATE product SET price = ? WHERE id = ? AND (is_active = 1)"
#     expected_params = [250, 1]
#     assert query == expected_query
#     assert params == expected_params





    

# def test_delete_query(query_builder):
#     # Test: DELETE query
#     request = {
#         "operation": "delete",
#         "table": "product",
#         "clause": {
#             "id": 1
#         }
#     }
#     persona = "user"
#     query, params = query_builder.build_query(request, persona)  # Assuming QueryBuilder returns (query, params)

#     expected_query = "DELETE FROM product WHERE id = ? AND (is_active = 1)"
#     expected_params = [1]

#     # Validate query structure and parameter values
#     assert query == expected_query
#     assert params == expected_params




# def test_select_with_pagination(query_builder):
#     request = {
#         "operation": "select",
#         "table": "product",
#         "columns": ["id", "name"],
#         "limit": 5,
#         "offset": 10
#     }
#     persona = "user"
#     query, params = query_builder.build_query(request, persona)
    
#     expected_query = "SELECT id, name FROM product WHERE (is_active = 1) LIMIT ? OFFSET ?"
#     expected_params = [5, 10]

#     assert query == expected_query
#     assert params == expected_params











# def test_invalid_operation(query_builder):
#     request = {"operation": "unknown", "table": "product"}
#     persona = "user"
#     with pytest.raises(ValueError):
#         query_builder.build_query(request, persona)





# def test_select_query_with_advanced_clause(query_builder):
#     request = {
#         "operation": "select",
#         "table": "product",
#         "columns": ["id", "name", "price"],
#         "clause": {
#             "price": {"operator": ">", "value": 100},
#             "id": {"operator": "IN", "value": [1, 2, 3]}
#         },
#         "limit": 10,
#         "offset": 5
#     }
#     persona = "user"
#     query, params = query_builder.build_query(request, persona)
    
#     expected_query = (
#         "SELECT id, name, price FROM product "
#         "WHERE (price > ? AND id IN (?, ?, ?)) AND (is_active = 1) "
#         "LIMIT ? OFFSET ?"
#     )
#     expected_params = [100, 1, 2, 3, 10, 5]
    
#     assert query == expected_query
#     assert params == expected_params




# def generate_query(persona, table, clause):
#     qb = QueryBuilder()
    
#     # Construct the request dictionary based on input
#     request = {
#         "operation": "select",
#         "table": table,
#         "columns": qb.auth_rules.get(persona, {}).get(table, ["*"]),  # Get authorized columns for persona
#         "clause": clause
#     }
    
#     # Use the QueryBuilder class to build the query
#     query, params = qb.build_query(request, persona)
#     return query, params

# # Test function
# def test_user_access_to_users():
#     query, params = generate_query("user", "users", {"id": {"operator": ">", "value": 10}, "name": {"operator": "LIKE", "value": "%John%"}})
#     expected_parts = [
#         "SELECT id, name, email FROM users",
#         "id > ?",
#         "name LIKE ?",
#         "is_verified = 1",
#     ]
#     # Ensure all parts exist in the generated query, ignoring order
#     for part in expected_parts:
#         assert part in query
#     assert params == [10, "%John%"]




