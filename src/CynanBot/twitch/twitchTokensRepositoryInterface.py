from abc import abstractmethod

from CynanBot.misc.clearable import Clearable
from CynanBot.twitch.api.twitchTokensDetails import TwitchTokensDetails


class TwitchTokensRepositoryInterface(Clearable):

    @abstractmethod
    async def addUser(self, code: str, twitchChannel: str, twitchChannelId: str):
        pass

    @abstractmethod
    async def getAccessToken(self, twitchChannel: str) -> str | None:
        pass

    @abstractmethod
    async def getAccessTokenById(self, twitchChannelId: str) -> str | None:
        pass

    @abstractmethod
    async def hasAccessToken(self, twitchChannel: str) -> bool:
        pass

    @abstractmethod
    async def hasAccessTokenById(self, twitchChannelId: str) -> bool:
        pass

    @abstractmethod
    async def removeUser(self, twitchChannel: str):
        pass

    @abstractmethod
    async def removeUserById(self, twitchChannelId: str):
        pass

    @abstractmethod
    async def requireAccessToken(self, twitchChannel: str) -> str:
        pass

    @abstractmethod
    async def requireAccessTokenById(self, twitchChannelId: str) -> str:
        pass

    @abstractmethod
    async def requireTokensDetails(
        self,
        twitchChannel: str
    ) -> TwitchTokensDetails:
        pass
