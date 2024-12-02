from .generic_rdbms_source import GenericRDBMSSource

class PostgresSource(GenericRDBMSSource):
    def __init__(self, db_url):
        super().__init__(db_url)
        print("Initialized PostgreSQL Source.")
