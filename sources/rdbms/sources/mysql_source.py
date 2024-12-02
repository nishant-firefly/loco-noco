from .generic_rdbms_source import GenericRDBMSSource

class MySQLSource(GenericRDBMSSource):
    def __init__(self, db_url):
        """
        Initialize the MySQL source.
        Args:
            db_url (str): SQLAlchemy connection URL for MySQL.
        """
        super().__init__(db_url)
        print("Initialized MySQL Source")

    def connect(self):
        """
        Additional connection logic for MySQL, if required.
        """
        print("Connected to MySQL database.")
