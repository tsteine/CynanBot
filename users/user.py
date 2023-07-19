from datetime import tzinfo
from typing import List, Optional
from urllib.parse import urlparse

import aiofiles
import aiofiles.ospath

import CynanBotCommon.utils as utils
from CynanBotCommon.cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBotCommon.users.userInterface import UserInterface
from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack


class User(UserInterface):

    def __init__(
        self,
        areRecurringActionsEnabled: bool,
        isCatJamMessageEnabled: bool,
        isChatBandEnabled: bool,
        isChatLoggingEnabled: bool,
        isCutenessEnabled: bool,
        isCynanSourceEnabled: bool,
        isDeerForceMessageEnabled: bool,
        isEnabled: bool,
        isEyesMessageEnabled: bool,
        isGiftSubscriptionThanksMessageEnabled: bool,
        isGiveCutenessEnabled: bool,
        isImytSlurpMessageEnabled: bool,
        isJamCatMessageEnabled: bool,
        isJishoEnabled: bool,
        isJokeTriviaRepositoryEnabled: bool,
        isLoremIpsumEnabled: bool,
        isPicOfTheDayEnabled: bool,
        isPkmnEnabled: bool,
        isPokepediaEnabled: bool,
        isRaceEnabled: bool,
        isRaidLinkMessagingEnabled: bool,
        isRatJamMessageEnabled: bool,
        isRewardIdPrintingEnabled: bool,
        isRoachMessageEnabled: bool,
        isSchubertWalkMessageEnabled: bool,
        isShinyTriviaEnabled: bool,
        isToxicTriviaEnabled: bool,
        isStarWarsQuotesEnabled: bool,
        isSubGiftThankingEnabled: bool,
        isSuperTriviaGameEnabled: bool,
        isTranslateEnabled: bool,
        isTriviaEnabled: bool,
        isTriviaGameEnabled: bool,
        isWeatherEnabled: bool,
        isWordOfTheDayEnabled: bool,
        superTriviaGamePoints: Optional[int],
        superTriviaGameShinyMultiplier: Optional[int],
        superTriviaGameToxicMultiplier: Optional[int],
        superTriviaGameToxicPunishmentMultiplier: Optional[int],
        superTriviaPerUserAttempts: Optional[int],
        triviaGamePoints: Optional[int],
        triviaGameShinyMultiplier: Optional[int],
        waitForSuperTriviaAnswerDelay: Optional[int],
        waitForTriviaAnswerDelay: Optional[int],
        discord: Optional[str],
        handle: str,
        instagram: Optional[str],
        locationId: str,
        picOfTheDayFile: str,
        picOfTheDayRewardId: str,
        pkmnBattleRewardId: str,
        pkmnEvolveRewardId: str,
        pkmnShinyRewardId: str,
        speedrunProfile: str,
        triviaGameRewardId: Optional[str],
        twitter: str,
        cutenessBoosterPacks: Optional[List[CutenessBoosterPack]],
        pkmnCatchBoosterPacks: Optional[List[PkmnCatchBoosterPack]],
        timeZones: Optional[List[tzinfo]]
    ):
        if not utils.isValidBool(areRecurringActionsEnabled):
            raise ValueError(f'areRecurringActionsEnabled argument is malformed: \"{areRecurringActionsEnabled}\"')
        elif not utils.isValidBool(isCatJamMessageEnabled):
            raise ValueError(f'isCatJamMessageEnabled argument is malformed: \"{isCatJamMessageEnabled}\"')
        elif not utils.isValidBool(isChatBandEnabled):
            raise ValueError(f'isChatBandEnabled argument is malformed: \"{isChatBandEnabled}\"')
        elif not utils.isValidBool(isChatLoggingEnabled):
            raise ValueError(f'isChatLoggingEnabled argument is malformed: \"{isChatLoggingEnabled}\"')
        elif not utils.isValidBool(isCutenessEnabled):
            raise ValueError(f'isCutenessEnabled argument is malformed: \"{isCutenessEnabled}\"')
        elif not utils.isValidBool(isCynanSourceEnabled):
            raise ValueError(f'isCynanSourceEnabled argument is malformed: \"{isCynanSourceEnabled}\"')
        elif not utils.isValidBool(isDeerForceMessageEnabled):
            raise ValueError(f'isDeerForceMessageEnabled argument is malformed: \"{isDeerForceMessageEnabled}\"')
        elif not utils.isValidBool(isEnabled):
            raise ValueError(f'isEnabled argument is malformed: \"{isEnabled}\"')
        elif not utils.isValidBool(isEyesMessageEnabled):
            raise ValueError(f'isEyesMessageEnabled argument is malformed: \"{isEyesMessageEnabled}\"')
        elif not utils.isValidBool(isGiftSubscriptionThanksMessageEnabled):
            raise ValueError(f'isGiftSubscriptionThanksMessageEnabled argument is malformed: \"{isGiftSubscriptionThanksMessageEnabled}\"')
        elif not utils.isValidBool(isGiveCutenessEnabled):
            raise ValueError(f'isGiveCutenessEnabled argument is malformed: \"{isGiveCutenessEnabled}\"')
        elif not utils.isValidBool(isImytSlurpMessageEnabled):
            raise ValueError(f'isImytSlurpMessageEnabled argument is malformed: \"{isImytSlurpMessageEnabled}\"')
        elif not utils.isValidBool(isJamCatMessageEnabled):
            raise ValueError(f'isJamCatMessageEnabled argument is malformed: \"{isJamCatMessageEnabled}\"')
        elif not utils.isValidBool(isJishoEnabled):
            raise ValueError(f'isJishoEnabled argument is malformed: \"{isJishoEnabled}\"')
        elif not utils.isValidBool(isJokeTriviaRepositoryEnabled):
            raise ValueError(f'isJokeTriviaRepositoryEnabled argument is malformed: \"{isJokeTriviaRepositoryEnabled}\"')
        elif not utils.isValidBool(isLoremIpsumEnabled):
            raise ValueError(f'isLoremIpsumEnabled argument is malformed: \"{isLoremIpsumEnabled}\"')
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
        elif not utils.isValidBool(isRatJamMessageEnabled):
            raise ValueError(f'isRatJamMessageEnabled argument is malformed: \"{isRatJamMessageEnabled}\"')
        elif not utils.isValidBool(isRewardIdPrintingEnabled):
            raise ValueError(f'isRewardIdPrintingEnabled argument is malformed: \"{isRewardIdPrintingEnabled}\"')
        elif not utils.isValidBool(isRoachMessageEnabled):
            raise ValueError(f'isRoachMessageEnabled argument is malformed: \"{isRoachMessageEnabled}\"')
        elif not utils.isValidBool(isSchubertWalkMessageEnabled):
            raise ValueError(f'isSchubertWalkMessageEnabled argument is malformed: \"{isSchubertWalkMessageEnabled}\"')
        elif not utils.isValidBool(isShinyTriviaEnabled):
            raise ValueError(f'isShinyTriviaEnabled argument is malformed: \"{isShinyTriviaEnabled}\"')
        elif not utils.isValidBool(isToxicTriviaEnabled):
            raise ValueError(f'isToxicTriviaEnabled argument is malformed: \"{isToxicTriviaEnabled}\"')
        elif not utils.isValidBool(isStarWarsQuotesEnabled):
            raise ValueError(f'isStarWarsQuotesEnabled argument is malformed: \"{isStarWarsQuotesEnabled}\"')
        elif not utils.isValidBool(isSubGiftThankingEnabled):
            raise ValueError(f'isSubGiftThankingEnabled argument is malformed: \"{isSubGiftThankingEnabled}\"')
        elif not utils.isValidBool(isSuperTriviaGameEnabled):
            raise ValueError(f'isSuperTriviaGameEnabled argument is malformed: \"{isSuperTriviaGameEnabled}\"')
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
        elif superTriviaGamePoints is not None and not utils.isValidInt(superTriviaGamePoints):
            raise ValueError(f'superTriviaGamePoints argument is malformed: \"{superTriviaGamePoints}\"')
        elif superTriviaGameShinyMultiplier is not None and not utils.isValidInt(superTriviaGameShinyMultiplier):
            raise ValueError(f'superTriviaGameShinyMultiplier argument is malformed: \"{superTriviaGameShinyMultiplier}\"')
        elif superTriviaGameToxicPunishmentMultiplier is not None and not utils.isValidInt(superTriviaGameToxicPunishmentMultiplier):
            raise ValueError(f'superTriviaGameToxicPunishmentMultiplier argument is malformed: \"{superTriviaGameToxicPunishmentMultiplier}\"')
        elif superTriviaPerUserAttempts is not None and not utils.isValidInt(superTriviaPerUserAttempts):
            raise ValueError(f'superTriviaPeruserAttempts argument is malformed: \"{superTriviaPerUserAttempts}\"')
        elif triviaGamePoints is not None and not utils.isValidInt(triviaGamePoints):
            raise ValueError(f'triviaGamePoints argument is malformed: \"{triviaGamePoints}\"')
        elif triviaGameShinyMultiplier is not None and not utils.isValidInt(triviaGameShinyMultiplier):
            raise ValueError(f'triviaGameShinyMultiplier argument is malformed: \"{triviaGameShinyMultiplier}\"')
        elif waitForSuperTriviaAnswerDelay is not None and not utils.isValidInt(waitForSuperTriviaAnswerDelay):
            raise ValueError(f'waitForSuperTriviaAnswerDelay argument is malformed: \"{waitForSuperTriviaAnswerDelay}\"')
        elif waitForTriviaAnswerDelay is not None and not utils.isValidInt(waitForTriviaAnswerDelay):
            raise ValueError(f'waitForTriviaAnswerDelay argument is malformed: \"{waitForTriviaAnswerDelay}\"')
        elif discord is not None and not isinstance(discord, str):
            raise ValueError(f'discord argument is malformed: \"{discord}\"')
        elif not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif isPicOfTheDayEnabled and not utils.isValidStr(picOfTheDayFile):
            raise ValueError(f'picOfTheDayFile argument is malformed: \"{picOfTheDayFile}\"')
        elif triviaGameRewardId is not None and not isinstance(triviaGameRewardId, str):
            raise ValueError(f'triviaGameRewardId argument is malformed: \"{triviaGameRewardId}\"')
        elif twitter is not None and not isinstance(twitter, str):
            raise ValueError(f'twitter argument is malformed: \"{twitter}\"')

        self.__areRecurringActionsEnabled: bool = areRecurringActionsEnabled
        self.__isCatJamMessageEnabled: bool = isCatJamMessageEnabled
        self.__isChatBandEnabled: bool = isChatBandEnabled
        self.__isChatLoggingEnabled: bool = isChatLoggingEnabled
        self.__isCutenessEnabled: bool = isCutenessEnabled
        self.__isCynanSourceEnabled: bool = isCynanSourceEnabled
        self.__isDeerForceMessageEnabled: bool = isDeerForceMessageEnabled
        self.__isEnabled: bool = isEnabled
        self.__isEyesMessageEnabled: bool = isEyesMessageEnabled
        self.__isGiftSubscriptionThanksMessageEnabled: bool = isGiftSubscriptionThanksMessageEnabled
        self.__isGiveCutenessEnabled: bool = isGiveCutenessEnabled
        self.__isImytSlurpMessageEnabled: bool = isImytSlurpMessageEnabled
        self.__isJamCatMessageEnabled: bool = isJamCatMessageEnabled
        self.__isJishoEnabled: bool = isJishoEnabled
        self.__isJokeTriviaRepositoryEnabled: bool = isJokeTriviaRepositoryEnabled
        self.__isLoremIpsumEnabled: bool = isLoremIpsumEnabled
        self.__isPicOfTheDayEnabled: bool = isPicOfTheDayEnabled
        self.__isPkmnEnabled: bool = isPkmnEnabled
        self.__isPokepediaEnabled: bool = isPokepediaEnabled
        self.__isRaceEnabled: bool = isRaceEnabled
        self.__isRaidLinkMessagingEnabled: bool = isRaidLinkMessagingEnabled
        self.__isRatJamMessageEnabled: bool = isRatJamMessageEnabled
        self.__isRewardIdPrintingEnabled: bool = isRewardIdPrintingEnabled
        self.__isRoachMessageEnabled: bool = isRoachMessageEnabled
        self.__isSchubertWalkMessageEnabled: bool = isSchubertWalkMessageEnabled
        self.__isShinyTriviaEnabled: bool = isShinyTriviaEnabled
        self.__isToxicTriviaEnabled: bool = isToxicTriviaEnabled
        self.__isStarWarsQuotesEnabled: bool = isStarWarsQuotesEnabled
        self.__isSubGiftThankingEnabled: bool = isSubGiftThankingEnabled
        self.__isSuperTriviaGameEnabled: bool = isSuperTriviaGameEnabled
        self.__isTranslateEnabled: bool = isTranslateEnabled
        self.__isTriviaEnabled: bool = isTriviaEnabled
        self.__isTriviaGameEnabled: bool = isTriviaGameEnabled
        self.__isWeatherEnabled: bool = isWeatherEnabled
        self.__isWordOfTheDayEnabled: bool = isWordOfTheDayEnabled
        self.__superTriviaGamePoints: Optional[int] = superTriviaGamePoints
        self.__superTriviaGameShinyMultiplier: Optional[int] = superTriviaGameShinyMultiplier
        self.__superTriviaGameToxicMultiplier: Optional[int] = superTriviaGameToxicMultiplier
        self.__superTriviaGameToxicPunishmentMultiplier: Optional[int] = superTriviaGameToxicPunishmentMultiplier
        self.__superTriviaPerUserAttempts: Optional[int] = superTriviaPerUserAttempts
        self.__triviaGamePoints: Optional[int] = triviaGamePoints
        self.__triviaGameShinyMultiplier: Optional[int] = triviaGameShinyMultiplier
        self.__waitForTriviaAnswerDelay: Optional[int] = waitForTriviaAnswerDelay
        self.__waitForSuperTriviaAnswerDelay: Optional[int] = waitForSuperTriviaAnswerDelay
        self.__discord: Optional[str] = discord
        self.__handle: str = handle
        self.__instagram: Optional[str] = instagram
        self.__locationId: str = locationId
        self.__picOfTheDayFile: str = picOfTheDayFile
        self.__picOfTheDayRewardId: str = picOfTheDayRewardId
        self.__pkmnBattleRewardId: str = pkmnBattleRewardId
        self.__pkmnEvolveRewardId: str = pkmnEvolveRewardId
        self.__pkmnShinyRewardId: str = pkmnShinyRewardId
        self.__speedrunProfile: str = speedrunProfile
        self.__triviaGameRewardId: Optional[str] = triviaGameRewardId
        self.__twitter: Optional[str] = twitter
        self.__cutenessBoosterPacks: Optional[List[CutenessBoosterPack]] = cutenessBoosterPacks
        self.__pkmnCatchBoosterPacks: Optional[List[PkmnCatchBoosterPack]] = pkmnCatchBoosterPacks
        self.__timeZones: Optional[List[tzinfo]] = timeZones

    def areRecurringActionsEnabled(self) -> bool:
        return self.__areRecurringActionsEnabled

    async def fetchPicOfTheDay(self) -> str:
        if not self.__isPicOfTheDayEnabled:
            raise RuntimeError(f'POTD is disabled for {self.__handle}!')

        if not await aiofiles.ospath.exists(self.__picOfTheDayFile):
            raise FileNotFoundError(f'POTD file for {self.__handle} not found: \"{self.__picOfTheDayFile}\"!')

        async with aiofiles.open(self.__picOfTheDayFile, 'r') as file:
            data = await file.read()
            potdText = utils.cleanStr(data)

        if not utils.isValidUrl(potdText):
            raise ValueError(f'POTD text for {self.__handle} is malformed: \"{potdText}\"!')

        potdParsed = urlparse(potdText)
        return potdParsed.geturl()

    def getCutenessBoosterPacks(self) -> Optional[List[CutenessBoosterPack]]:
        return self.__cutenessBoosterPacks

    def getDiscordUrl(self) -> Optional[str]:
        return self.__discord

    def getHandle(self) -> str:
        return self.__handle

    def getInstagramUrl(self) -> Optional[str]:
        return self.__instagram

    def getLocationId(self) -> str:
        return self.__locationId

    def getPicOfTheDayRewardId(self) -> str:
        return self.__picOfTheDayRewardId

    def getPkmnBattleRewardId(self) -> str:
        return self.__pkmnBattleRewardId

    def getPkmnCatchBoosterPacks(self) -> Optional[List[PkmnCatchBoosterPack]]:
        return self.__pkmnCatchBoosterPacks

    def getPkmnEvolveRewardId(self) -> str:
        return self.__pkmnEvolveRewardId

    def getPkmnShinyRewardId(self) -> str:
        return self.__pkmnShinyRewardId

    def getSpeedrunProfile(self) -> str:
        return self.__speedrunProfile

    def getSuperTriviaGamePoints(self) -> Optional[int]:
        return self.__superTriviaGamePoints

    def getSuperTriviaGameShinyMultiplier(self) -> Optional[int]:
        return self.__superTriviaGameShinyMultiplier

    def getSuperTriviaGameToxicMultiplier(self) -> Optional[int]:
        return self.__superTriviaGameToxicMultiplier

    def getSuperTriviaGameToxicPunishmentMultiplier(self) -> Optional[int]:
        return self.__superTriviaGameToxicPunishmentMultiplier

    def getSuperTriviaPerUserAttempts(self) -> Optional[int]:
        return self.__superTriviaPerUserAttempts

    def getTimeZones(self) -> Optional[List[tzinfo]]:
        return self.__timeZones

    def getTriviaGamePoints(self) -> Optional[int]:
        return self.__triviaGamePoints

    def getTriviaGameRewardId(self) -> Optional[str]:
        return self.__triviaGameRewardId

    def getTriviaGameShinyMultiplier(self) -> Optional[int]:
        return self.__triviaGameShinyMultiplier

    def getTwitchUrl(self) -> str:
        return f'https://twitch.tv/{self.__handle.lower()}'

    def getTwitterUrl(self) -> Optional[str]:
        return self.__twitter

    def getWaitForSuperTriviaAnswerDelay(self) -> Optional[int]:
        return self.__waitForSuperTriviaAnswerDelay

    def getWaitForTriviaAnswerDelay(self) -> Optional[int]:
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

    def hasSuperTriviaGamePoints(self) -> bool:
        return utils.isValidInt(self.__superTriviaGamePoints)

    def hasSuperTriviaGameShinyMultiplier(self) -> bool:
        return utils.isValidInt(self.__superTriviaGameShinyMultiplier)

    def hasSuperTriviaGameToxicMultiplier(self) -> bool:
        return utils.isValidInt(self.__superTriviaGameToxicMultiplier)

    def hasSuperTriviaGameToxicPunishmentMultiplier(self) -> bool:
        return utils.isValidInt(self.__superTriviaGameToxicPunishmentMultiplier)

    def hasSuperTriviaPerUserAttempts(self) -> bool:
        return utils.isValidInt(self.__superTriviaPerUserAttempts)

    def hasTimeZones(self) -> bool:
        return utils.hasItems(self.__timeZones)

    def hasTriviaGamePoints(self) -> bool:
        return utils.isValidInt(self.__triviaGamePoints)

    def hasTriviaGameShinyMultiplier(self) -> bool:
        return utils.isValidInt(self.__triviaGameShinyMultiplier)

    def hasTwitter(self) -> bool:
        return utils.isValidUrl(self.__twitter)

    def hasWaitForSuperTriviaAnswerDelay(self) -> bool:
        return utils.isValidInt(self.__waitForSuperTriviaAnswerDelay)

    def hasWaitForTriviaAnswerDelay(self) -> bool:
        return utils.isValidInt(self.__waitForTriviaAnswerDelay)

    def isCatJamMessageEnabled(self) -> bool:
        return self.__isCatJamMessageEnabled

    def isChatBandEnabled(self) -> bool:
        return self.__isChatBandEnabled

    def isChatLoggingEnabled(self) -> bool:
        return self.__isChatLoggingEnabled

    def isCutenessEnabled(self) -> bool:
        return self.__isCutenessEnabled

    def isCynanSourceEnabled(self) -> bool:
        return self.__isCynanSourceEnabled

    def isDeerForceMessageEnabled(self) -> bool:
        return self.__isDeerForceMessageEnabled

    def isEnabled(self) -> bool:
        return self.__isEnabled

    def isEyesMessageEnabled(self) -> bool:
        return self.__isEyesMessageEnabled

    def isGiftSubscriptionThanksMessageEnabled(self) -> bool:
        return self.__isGiftSubscriptionThanksMessageEnabled

    def isGiveCutenessEnabled(self) -> bool:
        return self.__isGiveCutenessEnabled

    def isImytSlurpMessageEnabled(self) -> bool:
        return self.__isImytSlurpMessageEnabled

    def isJamCatMessageEnabled(self) -> bool:
        return self.__isJamCatMessageEnabled

    def isJishoEnabled(self) -> bool:
        return self.__isJishoEnabled

    def isJokeTriviaRepositoryEnabled(self) -> bool:
        return self.__isJokeTriviaRepositoryEnabled

    def isLoremIpsumEnabled(self) -> bool:
        return self.__isLoremIpsumEnabled

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

    def isRatJamMessageEnabled(self) -> bool:
        return self.__isRatJamMessageEnabled

    def isRewardIdPrintingEnabled(self) -> bool:
        return self.__isRewardIdPrintingEnabled

    def isRoachMessageEnabled(self) -> bool:
        return self.__isRoachMessageEnabled

    def isSchubertWalkMessageEnabled(self) -> bool:
        return self.__isSchubertWalkMessageEnabled

    def isShinyTriviaEnabled(self) -> bool:
        return self.__isShinyTriviaEnabled

    def isStarWarsQuotesEnabled(self) -> bool:
        return self.__isStarWarsQuotesEnabled

    def isSubGiftThankingEnabled(self) -> bool:
        return self.__isSubGiftThankingEnabled

    def isSuperTriviaGameEnabled(self) -> bool:
        return self.__isSuperTriviaGameEnabled

    def isToxicTriviaEnabled(self) -> bool:
        return self.__isToxicTriviaEnabled

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

    def __str__(self) -> str:
        return self.getHandle()
