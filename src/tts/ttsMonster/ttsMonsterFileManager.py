import re
import uuid
from dataclasses import dataclass
from typing import Pattern, Collection

import aiofiles
import aiofiles.os
import aiofiles.ospath
from frozenlist import FrozenList

from .ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TtsMonsterFileManager(TtsMonsterFileManagerInterface):

    @dataclass(frozen = True)
    class FetchAndSaveSoundDataTask:
        index: int
        fileName: str
        ttsUrl: str

    def __init__(
        self,
        timber: TimberInterface,
        directory: str = 'temp',
        fileExtension: str = 'wav'
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__timber: TimberInterface = timber
        self.__directory: str = directory
        self.__fileExtension: str = fileExtension

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __fetchTtsSoundData(self, ttsUrl: str):
        if not utils.isValidStr(ttsUrl):
            raise TypeError(f'ttsUrl argument is malformed: \"{ttsUrl}\"')

        # TODO
        return None

    async def __generateFileNames(self, size: int) -> FrozenList[str]:
        if not utils.isValidInt(size):
            raise TypeError(f'size argument is malformed: \"{size}\"')
        elif size < 1 or size > utils.getIntMaxSafeSize():
            raise ValueError(f'size argument is out of bounds: {size}')

        if not await aiofiles.ospath.exists(self.__directory):
            await aiofiles.os.makedirs(self.__directory)

        fileNames: set[str] = set()

        while len(fileNames) < size:
            fileName: str | None = None

            while not utils.isValidStr(fileName) or await aiofiles.ospath.exists(fileName):
                randomUuid = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
                fileName = utils.cleanPath(f'{self.__directory}/ttsmonster-{randomUuid}.{self.__fileExtension}')

            fileNames.add(fileName)

        frozenFileNames: FrozenList[str] = FrozenList(fileNames)
        frozenFileNames.freeze()

        return frozenFileNames

    async def saveTtsUrlToNewFile(self, ttsUrl: str) -> str | None:
        if not utils.isValidStr(ttsUrl):
            raise TypeError(f'ttsUrl argument is malformed: \"{ttsUrl}\"')

        ttsUrls: FrozenList[str] = FrozenList()
        ttsUrls.append(ttsUrl)
        ttsUrls.freeze()

        ttsFileNames = await self.saveTtsUrlsToNewFiles(ttsUrls)

        if ttsFileNames is None or len(ttsFileNames) == 0:
            return None

        return ttsFileNames[0]

    async def saveTtsUrlsToNewFiles(self, ttsUrls: Collection[str]) -> FrozenList[str] | None:
        if not isinstance(ttsUrls, Collection):
            raise TypeError(f'ttsUrls argument is malformed: \"{ttsUrls}\"')

        frozenTtsUrls: FrozenList[str] = FrozenList(ttsUrls)
        frozenTtsUrls.freeze()

        if len(frozenTtsUrls) == 0:
            return None

        fileNames = await self.__generateFileNames(len(frozenTtsUrls))

        for index, ttsUrl in enumerate(frozenTtsUrls):
            soundData = await self.__fetchTtsSoundData(ttsUrl)

            await self.__writeTtsSoundDataToLocalFile(
                soundData = soundData,
                fileName = fileNames[index]
            )

        # TODO fetch files and save them to the above file names

        return None

    async def __writeTtsSoundDataToLocalFile(
        self,
        soundData,
        fileName: str
    ):
        # TODO
        pass
