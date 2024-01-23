from typing import Optional, Self

from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.vlcHelper.vlcHelperInterface import VlcHelperInterface
from CynanBot.dependencyHolder import DependencyHolder
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.triviaUtilsInterface import TriviaUtilsInterface
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class DependencyHolderBuilder():

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        backgroundTaskHelper: BackgroundTaskHelper,
        chatLogger: ChatLoggerInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__cutenessUtils: Optional[CutenessUtilsInterface] = None
        self.__triviaUtils: Optional[TriviaUtilsInterface] = None
        self.__twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface] = None
        self.__vlcHelper: Optional[VlcHelperInterface] = None
        self.__websocketConnectionServer: Optional[WebsocketConnectionServerInterface] = None

    def build(self) -> DependencyHolder:
        return DependencyHolder(
            administratorProvider = self.__administratorProvider,
            backgroundTaskHelper = self.__backgroundTaskHelper,
            chatLogger = self.__chatLogger,
            cutenessUtils = self.__cutenessUtils,
            generalSettingsRepository = self.__generalSettingsRepository,
            sentMessageLogger = self.__sentMessageLogger,
            timber = self.__timber,
            triviaUtils = self.__triviaUtils,
            twitchPredictionWebsocketUtils = self.__twitchPredictionWebsocketUtils,
            twitchUtils = self.__twitchUtils,
            vlcHelper = self.__vlcHelper,
            websocketConnectionServer = self.__websocketConnectionServer
        )

    def setCutenessUtils(self, instance: CutenessUtilsInterface) -> Self:
        if not isinstance(instance, CutenessUtilsInterface):
            raise ValueError(f'instance argument is malformed: \"{instance}\"')

        self.__cutenessUtils = instance
        return self

    def setTriviaUtils(self, instance: TriviaUtilsInterface) -> Self:
        if not isinstance(instance, TriviaUtilsInterface):
            raise ValueError(f'instance argument is malformed: \"{instance}\"')

        self.__triviaUtils = instance
        return self

    def setTwitchPredictionWebsocketUtils(self, instance: TwitchPredictionWebsocketUtilsInterface) -> Self:
        if not isinstance(instance, TwitchPredictionWebsocketUtilsInterface):
            raise ValueError(f'instance argument is malformed: \"{instance}\"')

        self.__twitchPredictionWebsocketUtils = instance
        return self

    def setVlcHelper(self, instance: VlcHelperInterface) -> Self:
        if not isinstance(instance, VlcHelperInterface):
            raise TypeError(f'instance argument is malformed: \"{instance}\"')

        self.__vlcHelper = instance
        return self

    def setWebsocketConnectionServer(self, instance: WebsocketConnectionServerInterface) -> Self:
        if not isinstance(instance, WebsocketConnectionServerInterface):
            raise ValueError(f'instance argument is malformed: \"{instance}\"')

        self.__websocketConnectionServer = instance
        return self
