from .generic_rdbms_source import GenericRDBMSSource

class MSSQLSource(GenericRDBMSSource):
    def __init__(self, db_url):
        """
        Initialize the MSSQL source.
        Args:
            db_url (str): SQLAlchemy connection URL for MSSQL.
        """
        super().__init__(db_url)
        print("Initialized MSSQL Source")

    def connect(self):
        """
        Additional connection logic for MSSQL, if required.
        """
        print("Connected to MSSQL database.")
