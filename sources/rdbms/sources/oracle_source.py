from .generic_rdbms_source import GenericRDBMSSource

class OracleSource(GenericRDBMSSource):
    def __init__(self, db_url):
        """
        Initialize the Oracle source.
        Args:
            db_url (str): SQLAlchemy connection URL for Oracle.
        """
        super().__init__(db_url)
        print("Initialized Oracle Source")

    def connect(self):
        """
        Additional connection logic for Oracle, if required.
        """
        print("Connected to Oracle database.")
