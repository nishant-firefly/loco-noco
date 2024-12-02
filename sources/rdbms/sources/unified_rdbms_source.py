from .postgres_source import PostgresSource
from .mysql_source import MySQLSource
from .oracle_source import OracleSource
from .mssql_source import MSSQLSource

class UnifiedRDBMSSource(PostgresSource, MySQLSource, OracleSource, MSSQLSource):
    def __init__(self, postgres_url=None, mysql_url=None, oracle_url=None, mssql_url=None):
        if postgres_url:
            PostgresSource.__init__(self, postgres_url)
        if mysql_url:
            MySQLSource.__init__(self, mysql_url)
        if oracle_url:
            OracleSource.__init__(self, oracle_url)
        if mssql_url:
            MSSQLSource.__init__(self, mssql_url)
