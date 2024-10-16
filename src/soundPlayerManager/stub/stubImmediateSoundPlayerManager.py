from typing import Collection

from ..immediateSoundPlayerManagerInterface import ImmediateSoundPlayerManagerInterface
from ..soundAlert import SoundAlert
from ...chatBand.chatBandInstrument import ChatBandInstrument


class StubImmediateSoundPlayerManager(ImmediateSoundPlayerManagerInterface):

    async def playChatBandInstrument(
        self,
        instrument: ChatBandInstrument,
        volume: int | None = None
    ) -> bool:
        # this method is intentionally empty
        return False

    async def playPlaylist(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> bool:
        # this method is intentionally empty
        return False

    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None
    ) -> bool:
        # this method is intentionally empty
        return False

    async def playSoundFile(
        self,
        filePath: str |  None,
        volume: int | None = None
    ) -> bool:
        # this method is intentionally empty
        return False
