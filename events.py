import locale
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from typing import Any, Dict

from twitchio.channel import Channel

import CynanBotCommon.utils as utils
from authRepository import AuthRepository
from CynanBotCommon.chatLogger.chatLogger import ChatLogger
from CynanBotCommon.timber.timber import Timber
from generalSettingsRepository import GeneralSettingsRepository
from twitch.twitchUtils import TwitchUtils
from users.user import User


class AbsEvent(ABC):

    @abstractmethod
    async def handleEvent(self, channel: Channel, user: User, tags: Dict[str, Any]) -> bool:
        pass


class RaidLogEvent(AbsEvent):

    def __init__(
        self,
        chatLogger: ChatLogger,
        timber: Timber
    ):
        if not isinstance(chatLogger, ChatLogger):
            raise ValueError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__chatLogger: ChatLogger = chatLogger
        self.__timber: Timber = timber

    async def handleEvent(self, channel: Channel, user: User, tags: Dict[str, Any]) -> bool:
        if not user.isChatLoggingEnabled():
            return False

        raidedByName = tags.get('msg-param-displayName')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('display-name')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('login')

        if not utils.isValidStr(raidedByName):
            self.__timber.log('RaidLogEvent', f'{user.getHandle()} was raided, but the tags dictionary seems to have strange values: {tags}')
            return False

        raidSize = utils.getIntFromDict(tags, 'msg-param-viewerCount', 0)

        self.__chatLogger.logRaid(
            raidSize = raidSize,
            fromWho = raidedByName,
            twitchChannel = user.getHandle()
        )

        return True


class RaidThankEvent(AbsEvent):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handleEvent(self, channel: Channel, user: User, tags: Dict[str, Any]) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isRaidLinkMessagingEnabled():
            return False
        elif not user.isRaidLinkMessagingEnabled():
            return False

        raidedByName = tags.get('msg-param-displayName')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('display-name')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('login')

        if not utils.isValidStr(raidedByName):
            self.__timber.log('RaidEvent', f'{user.getHandle()} was raided, but the tags dictionary seems to have strange values: {tags}')
            return False

        messageSuffix = f'😻 Raiders, if you could, I\'d really appreciate you clicking this link to watch the stream. It helps me on my path to partner. {user.getTwitchUrl()} Thank you! 😻'
        raidSize = utils.getIntFromDict(tags, 'msg-param-viewerCount', -1)

        message: str = None
        if raidSize >= 10:
            raidSizeStr = locale.format_string("%d", raidSize, grouping = True)
            message = f'Thank you for the raid of {raidSizeStr} {raidedByName}! {messageSuffix}'
        else:
            message = f'Thank you for the raid {raidedByName}! {messageSuffix}'

        await self.__twitchUtils.waitThenSend(
            messageable = channel,
            delaySeconds = generalSettings.getRaidLinkMessagingDelay(),
            message = message,
            twitchChannel = user.getHandle()
        )

        self.__timber.log('RaidEvent', f'{user.getHandle()} received raid of {raidSize} from {raidedByName}!')
        return True


class SubGiftThankingEvent(AbsEvent):

    def __init__(
        self,
        authRepository: AuthRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(authRepository, AuthRepository):
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__authRepository: AuthRepository = authRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handleEvent(self, channel: Channel, user: User, tags: Dict[str, Any]) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        authSnapshot = await self.__authRepository.getAllAsync()

        if not generalSettings.isSubGiftThankingEnabled():
            return False
        elif not user.isSubGiftThankingEnabled():
            return False

        giftedByName: str = tags.get('display-name')
        if not utils.isValidStr(giftedByName):
            giftedByName = tags.get('login')

        giftedToName: str = tags.get('msg-param-recipient-display-name')
        if not utils.isValidStr(giftedToName):
            giftedToName = tags.get('msg-param-recipient-user-name')

        if giftedToName.lower() != authSnapshot.requireNick().lower():
            return False
        elif not utils.isValidStr(giftedByName):
            return False
        elif giftedToName.lower() == giftedByName.lower():
            return False

        await self.__twitchUtils.waitThenSend(
            messageable = channel,
            delaySeconds = 8,
            message = f'😻 Thank you for the gifted sub @{giftedByName}! ✨',
            twitchChannel = user.getHandle()
        )

        self.__timber.log('SubGiftThankingEvent', f'{authSnapshot.requireNick()} received sub gift to {user.getHandle()} from {giftedByName}!')
        return True


class StubEvent(AbsEvent):

    def __init__(self):
        pass

    async def handleEvent(self, channel: Channel, user: User, tags: Dict[str, Any]) -> bool:
        return False
