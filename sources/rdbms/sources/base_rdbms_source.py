# Abstract base class for RDBMS operations
from abc import ABC, abstractmethod

class BaseRDBMSSource(ABC):
    @abstractmethod
    def auth(self, *args, **kwargs):
        """Authenticate connection or access."""
        pass

    @abstractmethod
    def filter(self, *args, **kwargs):
        """Filter data based on criteria."""
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """Update existing data."""
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """Delete data."""
        pass
