from abc import ABC, abstractmethod
from typing import Any

from .databaseType import DatabaseType


class StorageJsonMapperInterface(ABC):

    @abstractmethod
    def parseDatabaseType(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType:
        pass

    @abstractmethod
    async def parseDatabaseTypeAsync(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType:
        pass
