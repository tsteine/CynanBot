import traceback
from typing import Any, Collection

import aiofiles.ospath
import vlc
from frozenlist import FrozenList

from ..soundAlert import SoundAlert
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class VlcSoundPlayerManager(SoundPlayerManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber

        self.__mediaPlayer: vlc.MediaListPlayer | None = None

    async def isPlaying(self) -> bool:
        mediaPlayer = self.__mediaPlayer
        return mediaPlayer is not None and mediaPlayer.is_playing()

    async def playPlaylist(self, filePaths: Collection[str]) -> bool:
        if not isinstance(filePaths, Collection):
            raise TypeError(f'filePaths argument is malformed: \"{filePaths}\"')

        frozenFilePaths: FrozenList[str] = FrozenList(filePaths)
        frozenFilePaths.freeze()

        if len(frozenFilePaths) == 0:
            self.__timber.log('VlcSoundPlayerManager', f'filePaths argument has no elements: \"{filePaths}\"')
            return False

        for index, filePath in enumerate(frozenFilePaths):
            if not utils.isValidStr(filePath):
                self.__timber.log('VlcSoundPlayerManager', f'The given file path at index {index} is not a valid string: \"{filePath}\"')
                return False
            elif not await aiofiles.ospath.exists(filePath):
                self.__timber.log('VlcSoundPlayerManager', f'The given file path at index {index} does not exist: \"{filePath}\"')
                return False
            elif not await aiofiles.ospath.isfile(filePath):
                self.__timber.log('VlcSoundPlayerManager', f'The given file path at index {index} is not a file: \"{filePath}\"')
                return False

        mediaList: vlc.MediaList | None = None
        addResults: dict[str, int] = dict()
        exception: Exception | None = None

        try:
            mediaList = vlc.MediaList()
            mediaList.lock()

            for filePath in frozenFilePaths:
                addResult = mediaList.add_media(filePath)
                addResults[filePath] = addResult
        except Exception as e:
            exception = e

        if mediaList is None or exception is not None:
            self.__timber.log('VlcSoundPlayerManager', f'Failed to load sounds from file paths: \"{filePaths}\" ({mediaList=}) ({exception=})', exception, traceback.format_exc())
            return False

        for filePath, addResult in addResults.items():
            if addResult != 0:
                self.__timber.log('VlcSoundPlayerManager', f'Encountered bad result code ({addResult}) when trying to add sound \"{filePath}\" from file paths: \"{filePaths}\" ({mediaList=}) ({exception=})', exception, traceback.format_exc())
                return False

        mediaPlayer = await self.__retrieveMediaPlayer()

        try:
            mediaPlayer.set_media_list(mediaList)
            mediaPlayer.play()
        except Exception as e:
            self.__timber.log('VlcSoundPlayerManager', f'Failed to play sounds from file paths: \"{filePaths}\" ({mediaList=}) ({mediaPlayer=}) ({exception=})', exception, traceback.format_exc())
            return False

        self.__timber.log('VlcSoundPlayerManager', f'Started playing playlist ({filePaths=}) ({mediaList=}) ({mediaPlayer=})')
        return True

    async def playSoundAlert(self, alert: SoundAlert) -> bool:
        if not isinstance(alert, SoundAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')

        if not await self.__soundPlayerSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('VlcSoundPlayerManager', f'There is already an ongoing sound!')
            return False

        filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(alert)

        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'No file path available for sound alert ({alert=}) ({filePath=})')
            return False

        return await self.playSoundFile(filePath)

    async def playSoundFile(self, filePath: str | None) -> bool:
        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'filePath argument is malformed: \"{filePath}\"')
            return False
        elif not await self.__soundPlayerSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('VlcSoundPlayerManager', f'There is already an ongoing sound!')
            return False

        filePaths: FrozenList[str] = FrozenList()
        filePaths.append(filePath)
        filePaths.freeze()

        return await self.playPlaylist(filePaths)

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    async def __retrieveMediaPlayer(self) -> vlc.MediaListPlayer:
        mediaPlayer = self.__mediaPlayer

        if mediaPlayer is None:
            mediaPlayer = vlc.MediaListPlayer()
            self.__mediaPlayer = mediaPlayer
            self.__timber.log('VlcSoundPlayerManager', f'Created new vlc.MediaPlayer instance: \"{mediaPlayer}\"')

        if not isinstance(mediaPlayer, vlc.MediaListPlayer):
            # this scenario should definitely be impossible, but the Python type checking was
            # getting angry without this check
            exception = RuntimeError(f'Failed to instantiate vlc.MediaPlayer: \"{mediaPlayer}\"')
            self.__timber.log('VlcSoundPlayerManager', f'Failed to instantiate vlc.MediaPlayer: \"{mediaPlayer}\" ({exception=})', exception, traceback.format_exc())
            raise exception

        return mediaPlayer

    def toDictionary(self) -> dict[str, Any]:
        return {
            'mediaPlayer': self.__mediaPlayer
        }
