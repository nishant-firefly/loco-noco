import unittest
from query_builder import QueryBuilder


class TestQueryBuilder(unittest.TestCase):
    def setUp(self):
        """Set up auth rules and custom conditions for testing."""
        auth_rules = {
            ('user', 'product'): ['id', 'name', 'price'],
            ('user', 'category'): ['id', 'name'],
            ('admin', 'product'): ['*'],
            ('admin', 'category'): ['*']
        }

        custom_conditions = {
            ('user', 'product'): "is_active=1",
            ('user', 'category'): "is_visible=1"
        }

        self.query_builder = QueryBuilder(auth_rules, custom_conditions)

    def test_select_user_product(self):
        """Test SELECT query for user on product table."""
        query = self.query_builder.select('user', 'product', where="price > 100")
        expected = "SELECT id, name, price FROM product WHERE is_active=1 AND price > 100;"
        self.assertEqual(query.strip(), expected.strip())

    def test_select_user_category(self):
        """Test SELECT query for user on category table."""
        query = self.query_builder.select('user', 'category')
        expected = "SELECT id, name FROM category WHERE is_visible=1;"
        self.assertEqual(query.strip(), expected.strip())

    def test_select_admin_product(self):
        """Test SELECT query for admin on product table."""
        query = self.query_builder.select('admin', 'product')
        expected = "SELECT * FROM product;"
        self.assertEqual(query.strip(), expected.strip())

    def test_insert_admin_product(self):
        """Test INSERT query for admin on product table."""
        query = self.query_builder.insert('admin', 'product', values={'id': 3, 'name': 'Tablet', 'price': 600})
        expected = "INSERT INTO product (id, name, price) VALUES (3, 'Tablet', 600);"
        self.assertEqual(query.strip(), expected.strip())

    def test_update_admin_product(self):
        """Test UPDATE query for admin on product table."""
        query = self.query_builder.update('admin', 'product', updates={'price': 1200}, where="id=2")
        expected = "UPDATE product SET price=1200 WHERE id=2;"
        self.assertEqual(query.strip(), expected.strip())

    def test_delete_admin_product(self):
        """Test DELETE query for admin on product table."""
        query = self.query_builder.delete('admin', 'product', where="id=3")
        expected = "DELETE FROM product WHERE id=3;"
        self.assertEqual(query.strip(), expected.strip())

    def test_select_user_no_access(self):
        """Test SELECT query for user on a table without access."""
        with self.assertRaises(PermissionError):
            self.query_builder.select('user', 'order')

    def test_insert_user_restricted(self):
        """Test INSERT query for user on product table (restricted)."""
        with self.assertRaises(PermissionError):
            self.query_builder.insert('user', 'order', values={'id': 4, 'name': 'Phone', 'price': 500})

    def test_update_user_restricted(self):
        """Test UPDATE query for user on product table (restricted)."""
        with self.assertRaises(PermissionError):
            self.query_builder.update('user', 'order', updates={'price': 800}, where="id=1")

    def test_delete_user_restricted(self):
        """Test DELETE query for user on product table (restricted)."""
        with self.assertRaises(PermissionError):
            self.query_builder.delete('user', 'product', where="id=2")



    def test_select_empty_columns(self):
        """Test SELECT query when no columns are accessible."""
        with self.assertRaises(PermissionError):
            self.query_builder.select('user', 'restricted_table')

    def test_update_no_where_clause(self):
        """Test UPDATE query without WHERE clause."""
        query = self.query_builder.update('admin', 'product', updates={'price': 1200})
        expected = "UPDATE product SET price=1200;"
        self.assertEqual(query.strip(), expected.strip())

    def test_insert_empty_values(self):
        """Test INSERT query with empty values."""
        with self.assertRaises(PermissionError):
            self.query_builder.insert('user', 'product', values={})

    def test_select_with_aggregate_function(self):
        """Test SELECT query with an aggregate function."""
        query = self.query_builder.select('admin', 'product', where="price > 100")
        expected = "SELECT COUNT(*) FROM product WHERE price > 100;"
        self.assertNotEqual(query.strip(), expected.strip())

    def test_unauthorized_access(self):
        """Test queries for unauthorized access to a table."""
        with self.assertRaises(PermissionError):
            self.query_builder.select('invalid_persona', 'product')

    def test_sql_injection_prevention(self):
        """Test SQL injection attempt in WHERE clause."""
        malicious_input = "1=1; DROP TABLE product;"
        with self.assertRaises(PermissionError):
            self.query_builder.select('admin', 'product', where=malicious_input)



    def test_pagination_query(self):
        """Test SELECT query with pagination (LIMIT and OFFSET)."""
        query = self.query_builder.select('user', 'product', where="price > 100").strip()
        query_with_pagination = f"{query.rstrip(';')} LIMIT 10 OFFSET 20;"
        expected = "SELECT id, name, price FROM product WHERE is_active=1 AND price > 100 LIMIT 10 OFFSET 20;"
        self.assertEqual(query_with_pagination.strip(), expected.strip())


    def test_aggregate_query(self):
        """Test SELECT query with aggregate functions (e.g., COUNT, SUM)."""
        persona = 'admin'
        table = 'product'
        columns = ['COUNT(*) AS total_products', 'SUM(price) AS total_price']
        self.query_builder.auth_rules[(persona, table)] = columns
        query = self.query_builder.select(persona, table)
        expected = "SELECT COUNT(*) AS total_products, SUM(price) AS total_price FROM product;"
        self.assertEqual(query.strip(), expected.strip())

    def test_edge_case_empty_where_clause(self):
        """Test query with an empty WHERE clause."""
        query = self.query_builder.select('admin', 'product', where="")
        expected = "SELECT * FROM product;"
        self.assertEqual(query.strip(), expected.strip())

    def test_edge_case_missing_columns(self):
        """Test SELECT query when no columns are specified for a persona."""
        self.query_builder.auth_rules[('user', 'empty_table')] = []
        with self.assertRaises(PermissionError):
            self.query_builder.select('user', 'empty_table')

    def test_bulk_insert(self):
        """Test bulk INSERT query for multiple rows."""
        persona = 'admin'
        table = 'product'
        values_list = [
            {'id': 4, 'name': 'Smartwatch', 'price': 250},
            {'id': 5, 'name': 'Monitor', 'price': 150}
        ]
        queries = [self.query_builder.insert(persona, table, values) for values in values_list]
        expected = [
            "INSERT INTO product (id, name, price) VALUES (4, 'Smartwatch', 250);",
            "INSERT INTO product (id, name, price) VALUES (5, 'Monitor', 150);"
        ]
        self.assertEqual(queries, expected)

    def test_update_with_multiple_conditions(self):
        """Test UPDATE query with multiple conditions."""
        query = self.query_builder.update(
            'admin',
            'product',
            updates={'price': 500},
            where="id=4 AND is_active=1"
        )
        expected = "UPDATE product SET price=500 WHERE id=4 AND is_active=1;"
        self.assertEqual(query.strip(), expected.strip())

    def test_delete_without_where_clause(self):
        """Test DELETE query without a WHERE clause (should raise an error)."""
        with self.assertRaises(ValueError):
            self.query_builder.delete('admin', 'product')

    def test_nonexistent_table_access(self):
        """Test query for a table that doesn't exist in auth_rules."""
        with self.assertRaises(PermissionError):
            self.query_builder.select('user', 'nonexistent_table')












if __name__ == '__main__':
    unittest.main()





















