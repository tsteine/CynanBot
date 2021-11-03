import os
import urllib
from datetime import tzinfo
from typing import List

import CynanBotCommon.utils as utils
from cutenessBoosterPack import CutenessBoosterPack
from pkmnBoosterPacks import PkmnCatchBoosterPack


class User():

    def __init__(
        self,
        isAnalogueEnabled: bool,
        isCatJamEnabled: bool,
        isChatBandEnabled: bool,
        isCutenessEnabled: bool,
        isCynanMessageEnabled: bool,
        isCynanSourceEnabled: bool,
        isDeerForceMessageEnabled: bool,
        isDiccionarioEnabled: bool,
        isGiveCutenessEnabled: bool,
        isJamCatEnabled: bool,
        isJishoEnabled: bool,
        isJokesEnabled: bool,
        isLocalTriviaRepositoryEnabled: bool,
        isPicOfTheDayEnabled: bool,
        isPkmnEnabled: bool,
        isPokepediaEnabled: bool,
        isRaceEnabled: bool,
        isRaidLinkMessagingEnabled: bool,
        isRatJamEnabled: bool,
        isRewardIdPrintingEnabled: bool,
        isStarWarsQuotesEnabled: bool,
        isTamalesEnabled: bool,
        isTranslateEnabled: bool,
        isTriviaEnabled: bool,
        isTriviaGameEnabled: bool,
        isWeatherEnabled: bool,
        isWordOfTheDayEnabled: bool,
        triviaGamePoints: int,
        triviaGameTutorialCutenessThreshold: int,
        waitForTriviaAnswerDelay: int,
        discord: str,
        handle: str,
        increaseCutenessDoubleRewardId: str,
        instagram: str,
        locationId: str,
        picOfTheDayFile: str,
        picOfTheDayRewardId: str,
        pkmnBattleRewardId: str,
        pkmnEvolveRewardId: str,
        pkmnShinyRewardId: str,
        speedrunProfile: str,
        triviaGameRewardId: str,
        twitter: str,
        cutenessBoosterPacks: List[CutenessBoosterPack],
        pkmnCatchBoosterPacks: List[PkmnCatchBoosterPack],
        timeZones: List[tzinfo]
    ):
        if not utils.isValidBool(isAnalogueEnabled):
            raise ValueError(f'isAnalogueEnabled argument is malformed: \"{isAnalogueEnabled}\"')
        elif not utils.isValidBool(isCatJamEnabled):
            raise ValueError(f'isCatJamEnabled argument is malformed: \"{isCatJamEnabled}\"')
        elif not utils.isValidBool(isChatBandEnabled):
            raise ValueError(f'isChatBandEnabled argument is malformed: \"{isChatBandEnabled}\"')
        elif not utils.isValidBool(isCutenessEnabled):
            raise ValueError(f'isCutenessEnabled argument is malformed: \"{isCutenessEnabled}\"')
        elif not utils.isValidBool(isCynanMessageEnabled):
            raise ValueError(f'isCynanMessageEnabled argument is malformed: \"{isCynanMessageEnabled}\"')
        elif not utils.isValidBool(isCynanSourceEnabled):
            raise ValueError(f'isCynanSourceEnabled argument is malformed: \"{isCynanSourceEnabled}\"')
        elif not utils.isValidBool(isDeerForceMessageEnabled):
            raise ValueError(f'isDeerForceMessageEnabled argument is malformed: \"{isDeerForceMessageEnabled}\"')
        elif not utils.isValidBool(isDiccionarioEnabled):
            raise ValueError(f'isDiccionarioEnabled argument is malformed: \"{isDiccionarioEnabled}\"')
        elif not utils.isValidBool(isGiveCutenessEnabled):
            raise ValueError(f'isGiveCutenessEnabled argument is malformed: \"{isGiveCutenessEnabled}\"')
        elif not utils.isValidBool(isJamCatEnabled):
            raise ValueError(f'isJamCatEnabled argument is malformed: \"{isJamCatEnabled}\"')
        elif not utils.isValidBool(isJishoEnabled):
            raise ValueError(f'isJishoEnabled argument is malformed: \"{isJishoEnabled}\"')
        elif not utils.isValidBool(isJokesEnabled):
            raise ValueError(f'isJokesEnabled argument is malformed: \"{isJokesEnabled}\"')
        elif not utils.isValidBool(isLocalTriviaRepositoryEnabled):
            raise ValueError(f'isLocalTriviaRepositoryEnabled argument is malformed: \"{isLocalTriviaRepositoryEnabled}\"')
        elif not utils.isValidBool(isPicOfTheDayEnabled):
            raise ValueError(f'isPicOfTheDayEnabled argument is malformed: \"{isPicOfTheDayEnabled}\"')
        elif not utils.isValidBool(isPkmnEnabled):
            raise ValueError(f'isPkmnEnabled argument is malformed: \"{isPkmnEnabled}\"')
        elif not utils.isValidBool(isPokepediaEnabled):
            raise ValueError(f'isPokepediaEnabled argument is malformed: \"{isPokepediaEnabled}\"')
        elif not utils.isValidBool(isRaceEnabled):
            raise ValueError(f'isRaceEnabled argument is malformed: \"{isRaceEnabled}\"')
        elif not utils.isValidBool(isRaidLinkMessagingEnabled):
            raise ValueError(f'isRaidLinkMessagingEnabled argument is malformed: \"{isRaidLinkMessagingEnabled}\"')
        elif not utils.isValidBool(isRatJamEnabled):
            raise ValueError(f'isRatJamEnabled argument is malformed: \"{isRatJamEnabled}\"')
        elif not utils.isValidBool(isRewardIdPrintingEnabled):
            raise ValueError(f'isRewardIdPrintingEnabled argument is malformed: \"{isRewardIdPrintingEnabled}\"')
        elif not utils.isValidBool(isStarWarsQuotesEnabled):
            raise ValueError(f'isStarWarsQuotesEnabled argument is malformed: \"{isStarWarsQuotesEnabled}\"')
        elif not utils.isValidBool(isTamalesEnabled):
            raise ValueError(f'isTamalesEnabled argument is malformed: \"{isTamalesEnabled}\"')
        elif not utils.isValidBool(isTranslateEnabled):
            raise ValueError(f'isTranslateEnabled argument is malformed: \"{isTranslateEnabled}\"')
        elif not utils.isValidBool(isTriviaEnabled):
            raise ValueError(f'isTriviaEnabled argument is malformed: \"{isTriviaEnabled}\"')
        elif not utils.isValidBool(isTriviaGameEnabled):
            raise ValueError(f'isTriviaGameEnabled argument is malformed: \"{isTriviaGameEnabled}\"')
        elif not utils.isValidBool(isWeatherEnabled):
            raise ValueError(f'isWeatherEnabled argument is malformed: \"{isWeatherEnabled}\"')
        elif not utils.isValidBool(isWordOfTheDayEnabled):
            raise ValueError(f'isWordOfTheDayEnabled argument is malformed: \"{isWordOfTheDayEnabled}\"')
        elif triviaGamePoints is not None and not utils.isValidNum(triviaGamePoints):
            raise ValueError(f'triviaGamePoints argument is malformed: \"{triviaGamePoints}\"')
        elif waitForTriviaAnswerDelay is not None and not utils.isValidNum(waitForTriviaAnswerDelay):
            raise ValueError(f'waitForTriviaAnswerDelay argument is malformed: \"{waitForTriviaAnswerDelay}\"')
        elif not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif isPicOfTheDayEnabled and not utils.isValidStr(picOfTheDayFile):
            raise ValueError(f'picOfTheDayFile argument is malformed: \"{picOfTheDayFile}\"')

        self.__isAnalogueEnabled: bool = isAnalogueEnabled
        self.__isCatJamEnabled: bool = isCatJamEnabled
        self.__isChatBandEnabled: bool = isChatBandEnabled
        self.__isCutenessEnabled: bool = isCutenessEnabled
        self.__isCynanMessageEnabled: bool = isCynanMessageEnabled
        self.__isCynanSourceEnabled: bool = isCynanSourceEnabled
        self.__isDeerForceMessageEnabled: bool = isDeerForceMessageEnabled
        self.__isDiccionarioEnabled: bool = isDiccionarioEnabled
        self.__isGiveCutenessEnabled: bool = isGiveCutenessEnabled
        self.__isJamCatEnabled: bool = isJamCatEnabled
        self.__isJishoEnabled: bool = isJishoEnabled
        self.__isJokesEnabled: bool = isJokesEnabled
        self.__isLocalTriviaRepositoryEnabled: bool = isLocalTriviaRepositoryEnabled
        self.__isPicOfTheDayEnabled: bool = isPicOfTheDayEnabled
        self.__isPkmnEnabled: bool = isPkmnEnabled
        self.__isPokepediaEnabled: bool = isPokepediaEnabled
        self.__isRaceEnabled: bool = isRaceEnabled
        self.__isRaidLinkMessagingEnabled: bool = isRaidLinkMessagingEnabled
        self.__isRatJamEnabled: bool = isRatJamEnabled
        self.__isRewardIdPrintingEnabled: bool = isRewardIdPrintingEnabled
        self.__isStarWarsQuotesEnabled: bool = isStarWarsQuotesEnabled
        self.__isTamalesEnabled: bool = isTamalesEnabled
        self.__isTranslateEnabled: bool = isTranslateEnabled
        self.__isTriviaEnabled: bool = isTriviaEnabled
        self.__isTriviaGameEnabled: bool = isTriviaGameEnabled
        self.__isWeatherEnabled: bool = isWeatherEnabled
        self.__isWordOfTheDayEnabled: bool = isWordOfTheDayEnabled
        self.__triviaGamePoints: int = triviaGamePoints
        self.__triviaGameTutorialCutenessThreshold: int = triviaGameTutorialCutenessThreshold
        self.__waitForTriviaAnswerDelay: int = waitForTriviaAnswerDelay
        self.__discord: str = discord
        self.__handle: str = handle
        self.__increaseCutenessDoubleRewardId: str = increaseCutenessDoubleRewardId
        self.__instagram: str = instagram
        self.__locationId: str = locationId
        self.__picOfTheDayFile: str = picOfTheDayFile
        self.__picOfTheDayRewardId: str = picOfTheDayRewardId
        self.__pkmnBattleRewardId: str = pkmnBattleRewardId
        self.__pkmnEvolveRewardId: str = pkmnEvolveRewardId
        self.__pkmnShinyRewardId: str = pkmnShinyRewardId
        self.__speedrunProfile: str = speedrunProfile
        self.__triviaGameRewardId: str = triviaGameRewardId
        self.__twitter: str = twitter
        self.__cutenessBoosterPacks: List[CutenessBoosterPack] = cutenessBoosterPacks
        self.__pkmnCatchBoosterPacks: List[PkmnCatchBoosterPack] = pkmnCatchBoosterPacks
        self.__timeZones: List[tzinfo] = timeZones

    def fetchPicOfTheDay(self) -> str:
        if not self.__isPicOfTheDayEnabled:
            raise RuntimeError(f'POTD is disabled for {self.__handle}')
        elif not os.path.exists(self.__picOfTheDayFile):
            raise FileNotFoundError(f'POTD file for {self.__handle} not found: \"{self.__picOfTheDayFile}\"')

        with open(self.__picOfTheDayFile, 'r') as file:
            potdText = utils.cleanStr(file.read())

        if not utils.isValidUrl(potdText):
            raise ValueError(f'POTD text for {self.__handle} is malformed: \"{potdText}\"')

        potdParsed = urllib.parse.urlparse(potdText)
        return potdParsed.geturl()

    def getCutenessBoosterPacks(self) -> List[CutenessBoosterPack]:
        return self.__cutenessBoosterPacks

    def getDiscordUrl(self) -> str:
        return self.__discord

    def getHandle(self) -> str:
        return self.__handle

    def getIncreaseCutenessDoubleRewardId(self) -> str:
        return self.__increaseCutenessDoubleRewardId

    def getInstagramUrl(self) -> str:
        return self.__instagram

    def getLocationId(self) -> str:
        return self.__locationId

    def getPicOfTheDayRewardId(self) -> str:
        return self.__picOfTheDayRewardId

    def getPkmnBattleRewardId(self) -> str:
        return self.__pkmnBattleRewardId

    def getPkmnCatchBoosterPacks(self) -> List[PkmnCatchBoosterPack]:
        return self.__pkmnCatchBoosterPacks

    def getPkmnEvolveRewardId(self) -> str:
        return self.__pkmnEvolveRewardId

    def getPkmnShinyRewardId(self) -> str:
        return self.__pkmnShinyRewardId

    def getSpeedrunProfile(self) -> str:
        return self.__speedrunProfile

    def getTimeZones(self) -> List[tzinfo]:
        return self.__timeZones

    def getTriviaGameRewardId(self) -> str:
        return self.__triviaGameRewardId

    def getTriviaGamePoints(self) -> int:
        return self.__triviaGamePoints

    def getTriviaGameTutorialCutenessThreshold(self) -> int:
        return self.__triviaGameTutorialCutenessThreshold

    def getTwitchUrl(self) -> str:
        return f'https://twitch.tv/{self.__handle.lower()}'

    def getTwitterUrl(self) -> str:
        return self.__twitter

    def getWaitForTriviaAnswerDelay(self) -> int:
        return self.__waitForTriviaAnswerDelay

    def hasCutenessBoosterPacks(self) -> bool:
        return utils.hasItems(self.__cutenessBoosterPacks)

    def hasDiscord(self) -> bool:
        return utils.isValidUrl(self.__discord)

    def hasInstagram(self) -> str:
        return utils.isValidUrl(self.__instagram)

    def hasLocationId(self) -> bool:
        return utils.isValidStr(self.__locationId)

    def hasPkmnCatchBoosterPacks(self) -> bool:
        return utils.hasItems(self.__pkmnCatchBoosterPacks)

    def hasSpeedrunProfile(self) -> bool:
        return utils.isValidUrl(self.__speedrunProfile)

    def hasTimeZones(self) -> bool:
        return utils.hasItems(self.__timeZones)

    def hasTriviaGamePoints(self) -> bool:
        return utils.isValidNum(self.__triviaGamePoints)

    def hasTriviaGameTutorialCutenessThreshold(self) -> bool:
        return utils.isValidNum(self.__triviaGameTutorialCutenessThreshold)

    def hasTwitter(self) -> bool:
        return utils.isValidUrl(self.__twitter)

    def hasWaitForTriviaAnswerDelay(self) -> bool:
        return utils.isValidNum(self.__waitForTriviaAnswerDelay)

    def isAnalogueEnabled(self) -> bool:
        return self.__isAnalogueEnabled

    def isCatJamEnabled(self) -> bool:
        return self.__isCatJamEnabled

    def isChatBandEnabled(self) -> bool:
        return self.__isChatBandEnabled

    def isCutenessEnabled(self) -> bool:
        return self.__isCutenessEnabled

    def isCynanMessageEnabled(self) -> bool:
        return self.__isCynanMessageEnabled

    def isCynanSourceEnabled(self) -> bool:
        return self.__isCynanSourceEnabled

    def isDeerForceMessageEnabled(self) -> bool:
        return self.__isDeerForceMessageEnabled

    def isDiccionarioEnabled(self) -> bool:
        return self.__isDiccionarioEnabled

    def isGiveCutenessEnabled(self) -> bool:
        return self.__isGiveCutenessEnabled

    def isJamCatEnabled(self) -> bool:
        return self.__isJamCatEnabled

    def isJishoEnabled(self) -> bool:
        return self.__isJishoEnabled

    def isJokesEnabled(self) -> bool:
        return self.__isJokesEnabled

    def isLocalTriviaRepositoryEnabled(self) -> bool:
        return self.__isLocalTriviaRepositoryEnabled

    def isPicOfTheDayEnabled(self) -> bool:
        return self.__isPicOfTheDayEnabled

    def isPkmnEnabled(self) -> bool:
        return self.__isPkmnEnabled

    def isPokepediaEnabled(self) -> bool:
        return self.__isPokepediaEnabled

    def isRaceEnabled(self) -> bool:
        return self.__isRaceEnabled

    def isRaidLinkMessagingEnabled(self) -> bool:
        return self.__isRaidLinkMessagingEnabled

    def isRatJamEnabled(self) -> bool:
        return self.__isRatJamEnabled

    def isRewardIdPrintingEnabled(self) -> bool:
        return self.__isRewardIdPrintingEnabled

    def isStarWarsQuotesEnabled(self) -> bool:
        return self.__isStarWarsQuotesEnabled

    def isTamalesEnabled(self) -> bool:
        return self.__isTamalesEnabled

    def isTranslateEnabled(self) -> bool:
        return self.__isTranslateEnabled

    def isTriviaEnabled(self) -> bool:
        return self.__isTriviaEnabled

    def isTriviaGameEnabled(self) -> bool:
        return self.__isTriviaGameEnabled

    def isWeatherEnabled(self) -> bool:
        return self.__isWeatherEnabled

    def isWordOfTheDayEnabled(self) -> bool:
        return self.__isWordOfTheDayEnabled
