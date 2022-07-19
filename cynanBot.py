from asyncio import AbstractEventLoop
from typing import Dict, Optional

from twitchio import Channel, Message
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import CommandNotFound
from twitchio.ext.pubsub import PubSubChannelPointsMessage

import CynanBotCommon.utils as utils
import twitch.twitchUtils as twitchUtils
from commands import (AbsCommand, AnalogueCommand, AnswerCommand,
                      ClearCachesCommand, CommandsCommand,
                      CutenessChampionsCommand, CutenessCommand,
                      CutenessHistoryCommand, CynanSourceCommand,
                      DiscordCommand, GiveCutenessCommand, JishoCommand,
                      LoremIpsumCommand, MyCutenessCommand,
                      MyCutenessHistoryCommand, PbsCommand, PkMonCommand,
                      PkMoveCommand, RaceCommand, StubCommand,
                      SuperAnswerCommand, SuperTriviaCommand, SwQuoteCommand,
                      TamalesCommand, TimeCommand, TranslateCommand,
                      TriviaScoreCommand, TwitterCommand, WeatherCommand,
                      WordCommand)
from cutenessUtils import CutenessUtils
from CynanBotCommon.analogue.analogueStoreRepository import \
    AnalogueStoreRepository
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
from CynanBotCommon.chatLogger.chatLogger import ChatLogger
from CynanBotCommon.cuteness.cutenessRepository import CutenessRepository
from CynanBotCommon.cuteness.doubleCutenessHelper import DoubleCutenessHelper
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.language.jishoHelper import JishoHelper
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.lruCache import LruCache
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.trivia.absTriviaEvent import AbsTriviaEvent
from CynanBotCommon.trivia.correctAnswerTriviaEvent import \
    CorrectAnswerTriviaEvent
from CynanBotCommon.trivia.correctSuperAnswerTriviaEvent import \
    CorrectSuperAnswerTriviaEvent
from CynanBotCommon.trivia.failedToFetchQuestionSuperTriviaEvent import \
    FailedToFetchQuestionSuperTriviaEvent
from CynanBotCommon.trivia.failedToFetchQuestionTriviaEvent import \
    FailedToFetchQuestionTriviaEvent
from CynanBotCommon.trivia.incorrectAnswerTriviaEvent import \
    IncorrectAnswerTriviaEvent
from CynanBotCommon.trivia.newSuperTriviaGameEvent import \
    NewSuperTriviaGameEvent
from CynanBotCommon.trivia.newTriviaGameEvent import NewTriviaGameEvent
from CynanBotCommon.trivia.outOfTimeSuperTriviaEvent import \
    OutOfTimeSuperTriviaEvent
from CynanBotCommon.trivia.outOfTimeTriviaEvent import OutOfTimeTriviaEvent
from CynanBotCommon.trivia.triviaEventType import TriviaEventType
from CynanBotCommon.trivia.triviaGameMachine import TriviaGameMachine
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository
from CynanBotCommon.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.userIdsRepository import UserIdsRepository
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from events import AbsEvent, RaidThankEvent, SubGiftThankingEvent
from messages import (AbsMessage, CatJamMessage, ChatBandMessage,
                      ChatLogMessage, CynanMessage, DeerForceMessage,
                      EyesMessage, ImytSlurpMessage, JamCatMessage,
                      RatJamMessage, StubMessage)
from persistence.authRepository import AuthRepository
from persistence.generalSettingsRepository import GeneralSettingsRepository
from pointRedemptions import (AbsPointRedemption, CutenessRedemption,
                              PkmnBattleRedemption, PkmnCatchRedemption,
                              PkmnEvolveRedemption, PkmnShinyRedemption,
                              PotdPointRedemption, StubPointRedemption,
                              TriviaGameRedemption)
from triviaUtils import TriviaUtils
from twitch.eventSubUtils import EventSubUtils
from twitch.pubSubUtils import PubSubUtils
from users.usersRepository import UsersRepository


class CynanBot(commands.Bot):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        analogueStoreRepository: Optional[AnalogueStoreRepository],
        authRepository: AuthRepository,
        chatBandManager: Optional[ChatBandManager],
        chatLogger: Optional[ChatLogger],
        cutenessRepository: Optional[CutenessRepository],
        cutenessUtils: Optional[CutenessUtils],
        doubleCutenessHelper: Optional[DoubleCutenessHelper],
        funtoonRepository: Optional[FuntoonRepository],
        generalSettingsRepository: GeneralSettingsRepository,
        jishoHelper: Optional[JishoHelper],
        languagesRepository: LanguagesRepository,
        locationsRepository: Optional[LocationsRepository],
        nonceRepository: NonceRepository,
        pokepediaRepository: Optional[PokepediaRepository],
        starWarsQuotesRepository: Optional[StarWarsQuotesRepository],
        tamaleGuyRepository: Optional[TamaleGuyRepository],
        timber: Timber,
        translationHelper: Optional[TranslationHelper],
        triviaGameMachine: Optional[TriviaGameMachine],
        triviaScoreRepository: Optional[TriviaScoreRepository],
        triviaSettingsRepository: Optional[TriviaSettingsRepository],
        triviaUtils: Optional[TriviaUtils],
        twitchTokensRepository: TwitchTokensRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        weatherRepository: Optional[WeatherRepository],
        wordOfTheDayRepository: Optional[WordOfTheDayRepository]
    ):
        super().__init__(
            client_secret = authRepository.getAll().requireTwitchClientSecret(),
            initial_channels = [ user.getHandle().lower() for user in usersRepository.getUsers() ],
            loop = eventLoop,
            nick = authRepository.getAll().requireNick(),
            prefix = '!',
            retain_cache = True,
            token = authRepository.getAll().requireTwitchIrcAuthToken()
        )

        if eventLoop is None:
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif authRepository is None:
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif languagesRepository is None:
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif nonceRepository is None:
            raise ValueError(f'nonceRepository argument is malformed: \"{nonceRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif twitchTokensRepository is None:
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__authRepository: AuthRepository = authRepository
        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository

        self.__channelPointsLruCache: LruCache = LruCache(64)

        #######################################
        ## Initialization of command objects ##
        #######################################

        self.__commandsCommand: AbsCommand = CommandsCommand(generalSettingsRepository, timber, usersRepository)
        self.__cynanSourceCommand: AbsCommand = CynanSourceCommand(timber, usersRepository)
        self.__discordCommand: AbsCommand = DiscordCommand(timber, usersRepository)
        self.__loremIpsumCommand: AbsCommand = LoremIpsumCommand(timber, usersRepository)
        self.__pbsCommand: AbsCommand = PbsCommand(timber, usersRepository)
        self.__raceCommand: AbsCommand = RaceCommand(timber, usersRepository)
        self.__timeCommand: AbsCommand = TimeCommand(timber, usersRepository)
        self.__twitterCommand: AbsCommand = TwitterCommand(timber, usersRepository)

        if analogueStoreRepository is None:
            self.__analogueCommand: AbsCommand = StubCommand()
        else:
            self.__analogueCommand: AbsCommand = AnalogueCommand(analogueStoreRepository, generalSettingsRepository, timber, usersRepository)

        if cutenessRepository is None or doubleCutenessHelper is None or triviaGameMachine is None or triviaScoreRepository is None or triviaUtils is None:
            self.__answerCommand: AbsCommand = StubCommand()
            self.__superAnswerCommand: AbsCommand = StubCommand()
            self.__superTriviaCommand: AbsCommand = StubCommand()
        else:
            self.__answerCommand: AbsCommand = AnswerCommand(generalSettingsRepository, timber, triviaGameMachine, usersRepository)
            self.__superAnswerCommand: AbsCommand = SuperAnswerCommand(generalSettingsRepository, timber, triviaGameMachine, usersRepository)
            self.__superTriviaCommand: AbsCommand = SuperTriviaCommand(generalSettingsRepository, timber, triviaGameMachine, usersRepository)

        self.__clearCachesCommand: AbsCommand = ClearCachesCommand(authRepository, chatBandManager, funtoonRepository, generalSettingsRepository, timber, triviaSettingsRepository, usersRepository)

        if cutenessRepository is None or cutenessUtils is None:
            self.__cutenessCommand: AbsCommand = StubCommand()
            self.__cutenessChampionsCommand: AbsCommand = StubCommand()
            self.__cutenessHistoryCommand: AbsCommand = StubCommand()
            self.__giveCutenessCommand: AbsCommand = StubCommand()
            self.__myCutenessCommand: AbsCommand = StubCommand()
            self.__myCutenessHistoryCommand: AbsCommand = StubCommand()
        else:
            self.__cutenessCommand: AbsCommand = CutenessCommand(cutenessRepository, cutenessUtils, timber, userIdsRepository, usersRepository)
            self.__cutenessChampionsCommand: AbsCommand = CutenessChampionsCommand(cutenessRepository, cutenessUtils, timber, userIdsRepository, usersRepository)
            self.__cutenessHistoryCommand: AbsCommand = CutenessHistoryCommand(cutenessRepository, cutenessUtils, timber, userIdsRepository, usersRepository)
            self.__giveCutenessCommand: AbsCommand = GiveCutenessCommand(cutenessRepository, timber, userIdsRepository, usersRepository)
            self.__myCutenessCommand: AbsCommand = MyCutenessCommand(cutenessRepository, cutenessUtils, timber, usersRepository)
            self.__myCutenessHistoryCommand: AbsCommand = MyCutenessHistoryCommand(cutenessRepository, cutenessUtils, timber, userIdsRepository, usersRepository)

        if jishoHelper is None:
            self.__jishoCommand: AbsCommand = StubCommand()
        else:
            self.__jishoCommand: AbsCommand = JishoCommand(generalSettingsRepository, jishoHelper, timber, usersRepository)

        if pokepediaRepository is None:
            self.__pkMonCommand: AbsCommand = StubCommand()
            self.__pkMoveCommand: AbsCommand = StubCommand()
        else:
            self.__pkMonCommand: AbsCommand = PkMonCommand(generalSettingsRepository, pokepediaRepository, timber, usersRepository)
            self.__pkMoveCommand: AbsCommand = PkMoveCommand(generalSettingsRepository, pokepediaRepository, timber, usersRepository)

        if starWarsQuotesRepository is None:
            self.__swQuoteCommand: AbsCommand = StubCommand()
        else:
            self.__swQuoteCommand: AbsCommand = SwQuoteCommand(starWarsQuotesRepository, timber, usersRepository)

        if tamaleGuyRepository is None:
            self.__tamalesCommand: AbsCommand = StubCommand()
        else:
            self.__tamalesCommand: AbsCommand = TamalesCommand(generalSettingsRepository, tamaleGuyRepository, timber, usersRepository)

        if translationHelper is None:
            self.__translateCommand: AbsCommand = StubCommand()
        else:
            self.__translateCommand: AbsCommand = TranslateCommand(generalSettingsRepository, languagesRepository, timber, translationHelper, usersRepository)

        if cutenessRepository is None or triviaScoreRepository is None:
            self.__triviaScoreCommand: AbsCommand = StubCommand()
        else:
            self.__triviaScoreCommand: AbsCommand = TriviaScoreCommand(generalSettingsRepository, timber, triviaScoreRepository, triviaUtils, userIdsRepository, usersRepository)

        if locationsRepository is None or weatherRepository is None:
            self.__weatherCommand: AbsCommand = StubCommand()
        else:
            self.__weatherCommand: AbsCommand = WeatherCommand(generalSettingsRepository, locationsRepository, timber, usersRepository, weatherRepository)

        if wordOfTheDayRepository is None:
            self.__wordCommand: AbsCommand = StubCommand()
        else:
            self.__wordCommand: AbsCommand = WordCommand(generalSettingsRepository, languagesRepository, timber, usersRepository, wordOfTheDayRepository)

        #############################################
        ## Initialization of event handler objects ##
        #############################################

        self.__raidThankEvent: AbsEvent = RaidThankEvent(eventLoop, generalSettingsRepository, timber)
        self.__subGiftThankingEvent: AbsEvent = SubGiftThankingEvent(eventLoop, authRepository, generalSettingsRepository, timber)

        ###############################################
        ## Initialization of message handler objects ##
        ###############################################

        self.__catJamMessage: AbsMessage = CatJamMessage(generalSettingsRepository, timber)
        self.__cynanMessage: AbsMessage = CynanMessage(generalSettingsRepository, timber)
        self.__deerForceMessage: AbsMessage = DeerForceMessage(generalSettingsRepository, timber)
        self.__eyesMessage: AbsMessage = EyesMessage(generalSettingsRepository, timber)
        self.__imytSlurpMessage: AbsMessage = ImytSlurpMessage(generalSettingsRepository, timber)
        self.__jamCatMessage: AbsMessage = JamCatMessage(generalSettingsRepository, timber)
        self.__ratJamMessage: AbsMessage = RatJamMessage(generalSettingsRepository, timber)

        if chatBandManager is None:
            self.__chatBandMessage: AbsMessage = StubMessage()
        else:
            self.__chatBandMessage: AbsMessage = ChatBandMessage(chatBandManager, generalSettingsRepository, timber)

        if chatLogger is None:
            self.__chatLogMessage: AbsMessage = StubMessage()
        else:
            self.__chatLogMessage: AbsMessage = ChatLogMessage(chatLogger)

        ########################################################
        ## Initialization of point redemption handler objects ##
        ########################################################

        self.__potdPointRedemption: AbsPointRedemption = PotdPointRedemption(timber)

        if cutenessRepository is None or doubleCutenessHelper is None:
            self.__cutenessPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__cutenessPointRedemption: AbsPointRedemption = CutenessRedemption(cutenessRepository, doubleCutenessHelper, timber)

        if funtoonRepository is None:
            self.__pkmnBattlePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnBattlePointRedemption: AbsPointRedemption = PkmnBattleRedemption(funtoonRepository, generalSettingsRepository, timber)

        if funtoonRepository is None:
            self.__pkmnCatchPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnCatchPointRedemption: AbsPointRedemption = PkmnCatchRedemption(funtoonRepository, generalSettingsRepository, timber)

        if funtoonRepository is None:
            self.__pkmnEvolvePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnEvolvePointRedemption: AbsPointRedemption = PkmnEvolveRedemption(funtoonRepository, generalSettingsRepository, timber)

        if funtoonRepository is None:
            self.__pkmnShinyPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnShinyPointRedemption: AbsPointRedemption = PkmnShinyRedemption(funtoonRepository, generalSettingsRepository, timber)

        if cutenessRepository is None or triviaGameMachine is None or triviaScoreRepository is None or triviaUtils is None:
            self.__triviaGamePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__triviaGamePointRedemption: AbsPointRedemption = TriviaGameRedemption(generalSettingsRepository, timber, triviaGameMachine)

        generalSettings = self.__generalSettingsRepository.getAll()

        ########################################
        ## Initialization of EventSub objects ##
        ########################################

        self.__eventSubUtils: EventSubUtils = None
        if generalSettings.isEventSubEnabled():
            # TODO
            pass

        ######################################
        ## Initialization of PubSub objects ##
        ######################################

        self.__pubSubUtils: PubSubUtils = None
        if generalSettings.isPubSubEnabled():
            self.__pubSubUtils = PubSubUtils(
                eventLoop = eventLoop,
                authRepository = authRepository,
                client = self,
                generalSettingsRepository = generalSettingsRepository,
                timber = timber,
                twitchTokensRepository = twitchTokensRepository,
                userIdsRepository = userIdsRepository,
                usersRepository = usersRepository
            )

        self.__timber.log('CynanBot', f'Finished initialization of {self.__authRepository.getAll().requireNick()}')

    async def event_command_error(self, context: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        else:
            raise error

    async def event_message(self, message: Message):
        if message.echo:
            return

        if utils.isValidStr(message.content):
            generalSettings = await self.__generalSettingsRepository.getAllAsync()

            if generalSettings.isPersistAllUsersEnabled():
                await self.__userIdsRepository.setUser(
                    userId = str(message.author.id),
                    userName = message.author.name
                )

            twitchUser = await self.__usersRepository.getUserAsync(message.channel.name)

            await self.__chatLogMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            )

            if await self.__chatBandMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__cynanMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__deerForceMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__catJamMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__imytSlurpMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__jamCatMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__ratJamMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__eyesMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

        await self.handle_commands(message)

    async def event_pubsub_channel_points(self, event: PubSubChannelPointsMessage):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        twitchUserIdStr = str(event.channel_id)
        twitchUserNameStr = await self.__userIdsRepository.fetchUserName(twitchUserIdStr)
        twitchUser = await self.__usersRepository.getUserAsync(twitchUserNameStr)
        rewardId = str(event.reward.id)
        userIdThatRedeemed = str(event.user.id)
        userNameThatRedeemed: str = event.user.name
        redemptionMessage: str = event.input
        lruCacheId = f'{twitchUserNameStr}:{event.id}'.lower()

        if generalSettings.isDebugLoggingEnabled() or generalSettings.isRewardIdPrintingEnabled() or twitchUser.isRewardIdPrintingEnabled():
            self.__timber.log('CynanBot', f'Reward ID for {twitchUser.getHandle()}:{twitchUserIdStr} (redeemed by {userNameThatRedeemed}:{userIdThatRedeemed}): \"{rewardId}\"')

        if self.__channelPointsLruCache.contains(lruCacheId):
            self.__timber.log('CynanBot', f'Encountered duplicate reward ID for {twitchUser.getHandle()}:{twitchUserIdStr} (redeemed by {userNameThatRedeemed}:{userIdThatRedeemed}): \"{event.id}\"')
            return

        self.__channelPointsLruCache.put(lruCacheId)
        twitchChannel = await self.__getChannel(twitchUser.getHandle())

        if generalSettings.isPersistAllUsersEnabled():
            await self.__userIdsRepository.setUser(
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

        if twitchUser.isCutenessEnabled() and twitchUser.hasCutenessBoosterPacks():
            if await self.__cutenessPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                rewardId = rewardId,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            ):
                return

        if twitchUser.isPicOfTheDayEnabled() and rewardId == twitchUser.getPicOfTheDayRewardId():
            if await self.__potdPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                rewardId = rewardId,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            ):
                return

        if twitchUser.isPkmnEnabled():
            if rewardId == twitchUser.getPkmnBattleRewardId():
                if await self.__pkmnBattlePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    return

            if twitchUser.hasPkmnCatchBoosterPacks():
                if await self.__pkmnCatchPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    return

            if rewardId == twitchUser.getPkmnEvolveRewardId():
                if await self.__pkmnEvolvePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    return

            if rewardId == twitchUser.getPkmnShinyRewardId():
                if await self.__pkmnShinyPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    return

        if twitchUser.isTriviaGameEnabled() and rewardId == twitchUser.getTriviaGameRewardId():
            if await self.__triviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                rewardId = rewardId,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            ):
                return

    async def event_pubsub_error(self, tags: Dict):
        self.__timber.log('CynanBot', f'Received PubSub error: {tags}')

    async def event_pubsub_nonce(self, tags: Dict):
        self.__timber.log('CynanBot', f'Received PubSub nonce: {tags}')

    async def event_pubsub_pong(self):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if generalSettings.isPubSubPongLoggingEnabled():
            self.__timber.log('CynanBot', f'Received PubSub pong')

    async def event_raw_usernotice(self, channel: Channel, tags: Dict):
        if not utils.hasItems(tags):
            return

        msgId = tags.get('msg-id')

        if not utils.isValidStr(msgId):
            return

        twitchUser = await self.__usersRepository.getUserAsync(channel.name)
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if msgId == 'raid':
            await self.__raidThankEvent.handleEvent(
                twitchChannel = channel,
                twitchUser = twitchUser,
                tags = tags
            )
        elif msgId == 'subgift' or msgId == 'anonsubgift':
            await self.__subGiftThankingEvent.handleEvent(
                twitchChannel = channel,
                twitchUser = twitchUser,
                tags = tags
            )
        elif generalSettings.isDebugLoggingEnabled():
            self.__timber.log('CynanBot', f'event_raw_usernotice(): {tags}')

    async def event_ready(self):
        authSnapshot = await self.__authRepository.getAllAsync()
        self.__timber.log('CynanBot', f'{authSnapshot.requireNick()} is ready!')

        if self.__triviaGameMachine is not None:
            self.__triviaGameMachine.setEventListener(self.onNewTriviaEvent)

        if self.__eventSubUtils is not None:
            self.__eventSubUtils.startEventSub()

        if self.__pubSubUtils is not None:
            self.__pubSubUtils.startPubSub()

    async def __getChannel(self, twitchChannel: str) -> Channel:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        await self.wait_for_ready()
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if generalSettings.isDebugLoggingEnabled():
            connectedChannels = self.connected_channels
            self.__timber.log('CynanBot', f'Connected channels ({len(connectedChannels)}): {connectedChannels}')

        try:
            channel: Channel = self.get_channel(twitchChannel)

            if channel is None:
                self.__timber.log('CynanBot', f'Unable to get twitchChannel: \"{twitchChannel}\"')
                raise RuntimeError(f'Unable to get twitchChannel: \"{twitchChannel}\"')
            else:
                return channel
        except KeyError as e:
            self.__timber.log('CynanBot', f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {repr(e)}')
            raise RuntimeError(f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {repr(e)}')

    async def onNewTriviaEvent(self, event: AbsTriviaEvent):
        self.__timber.log('CynanBot', f'Received new trivia event: \"{event.getTriviaEventType()}\"')

        if event.getTriviaEventType() is TriviaEventType.CORRECT_ANSWER:
            await self.__handleCorrectAnswerTriviaEvent(event)
        elif event.getTriviaEventType() is TriviaEventType.GAME_FAILED_TO_FETCH_QUESTION:
            await self.__handleFailedToFetchQuestionTriviaEvent(event)
        elif event.getTriviaEventType() is TriviaEventType.GAME_OUT_OF_TIME:
            await self.__handleGameOutOfTimeTriviaEvent(event)
        elif event.getTriviaEventType() is TriviaEventType.INCORRECT_ANSWER:
            await self.__handleIncorrectAnswerTriviaEvent(event)
        elif event.getTriviaEventType() is TriviaEventType.NEW_GAME:
            await self.__handleNewTriviaGameEvent(event)
        elif event.getTriviaEventType() is TriviaEventType.NEW_SUPER_GAME:
            await self.__handleNewSuperTriviaGameEvent(event)
        elif event.getTriviaEventType() is TriviaEventType.SUPER_GAME_FAILED_TO_FETCH_QUESTION:
            await self.__handleFailedToFetchQuestionSuperTriviaEvent(event)
        elif event.getTriviaEventType() is TriviaEventType.SUPER_GAME_CORRECT_ANSWER:
            await self.__handleSuperGameCorrectAnswerTriviaEvent(event)
        elif event.getTriviaEventType() is TriviaEventType.SUPER_GAME_OUT_OF_TIME:
            await self.__handleSuperGameOutOfTimeTriviaEvent(event)

    async def __handleCorrectAnswerTriviaEvent(self, event: CorrectAnswerTriviaEvent):
        cutenessResult = await self.__cutenessRepository.fetchCutenessIncrementedBy(
            incrementAmount = event.getPointsForWinning(),
            twitchChannel = event.getTwitchChannel(),
            userId = event.getUserId(),
            userName = event.getUserName()
        )

        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getCorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            newCuteness = cutenessResult,
            userNameThatRedeemed = event.getUserName()
        ))

    async def __handleFailedToFetchQuestionTriviaEvent(self, event: FailedToFetchQuestionTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch trivia question')

    async def __handleFailedToFetchQuestionSuperTriviaEvent(self, event: FailedToFetchQuestionSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch super trivia question')

    async def __handleGameOutOfTimeTriviaEvent(self, event: OutOfTimeTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getOutOfTimeAnswerReveal(
            question = event.getTriviaQuestion(),
            userNameThatRedeemed = event.getUserName()
        ))

    async def __handleIncorrectAnswerTriviaEvent(self, event: IncorrectAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getIncorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            userNameThatRedeemed = event.getUserName()
        ))

    async def __handleNewTriviaGameEvent(self, event: NewTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getTriviaGameQuestionPrompt(
            triviaQuestion = event.getTriviaQuestion(),
            delaySeconds = event.getSecondsToLive(),
            points = event.getPointsForWinning(),
            userNameThatRedeemed = event.getUserName()
        ))

    async def __handleNewSuperTriviaGameEvent(self, event: NewSuperTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getSuperTriviaQuestionPrompt(
            triviaQuestion = event.getTriviaQuestion(),
            delaySeconds = event.getSecondsToLive(),
            points = event.getPointsForWinning(),
            multiplier = event.getPointsMultiplier()
        ))

    async def __handleSuperGameCorrectAnswerTriviaEvent(self, event: CorrectSuperAnswerTriviaEvent):
        cutenessResult = await self.__cutenessRepository.fetchCutenessIncrementedBy(
            incrementAmount = event.getPointsForWinning(),
            twitchChannel = event.getTwitchChannel(),
            userId = event.getUserId(),
            userName = event.getUserName()
        )

        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getSuperTriviaCorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            newCuteness = cutenessResult,
            multiplier = event.getPointsMultiplier(),
            points = event.getPointsForWinning(),
            userName = event.getUserName()
        ))

    async def __handleSuperGameOutOfTimeTriviaEvent(self, event: OutOfTimeSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getSuperTriviaOutOfTimeAnswerReveal(
            question = event.getTriviaQuestion(),
            multiplier = event.getPointsMultiplier()
        ))

    @commands.command(name = 'a')
    async def command_a(self, ctx: Context):
        await self.__answerCommand.handleCommand(ctx)

    @commands.command(name = 'analogue')
    async def command_analogue(self, ctx: Context):
        await self.__analogueCommand.handleCommand(ctx)

    @commands.command(name = 'answer')
    async def command_answer(self, ctx: Context):
        await self.__answerCommand.handleCommand(ctx)

    @commands.command(name = 'clearcaches')
    async def command_clearchatband(self, ctx: Context):
        await self.__clearCachesCommand.handleCommand(ctx)

    @commands.command(name = 'commands')
    async def command_commands(self, ctx: Context):
        await self.__commandsCommand.handleCommand(ctx)

    @commands.command(name = 'cuteness')
    async def command_cuteness(self, ctx: Context):
        await self.__cutenessCommand.handleCommand(ctx)

    @commands.command(name = 'cutenesschampions')
    async def command_cutenesschampions(self, ctx: Context):
        await self.__cutenessChampionsCommand.handleCommand(ctx)

    @commands.command(name = 'cutenesshistory')
    async def command_cutenesshistory(self, ctx: Context):
        await self.__cutenessHistoryCommand.handleCommand(ctx)

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx: Context):
        await self.__cynanSourceCommand.handleCommand(ctx)

    @commands.command(name = 'discord')
    async def command_discord(self, ctx: Context):
        await self.__discordCommand.handleCommand(ctx)

    @commands.command(name = 'givecuteness')
    async def command_givecuteness(self, ctx: Context):
        await self.__giveCutenessCommand.handleCommand(ctx)

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx: Context):
        await self.__jishoCommand.handleCommand(ctx)

    @commands.command(name = 'lorem')
    async def command_lorem(self, ctx: Context):
        await self.__loremIpsumCommand.handleCommand(ctx)

    @commands.command(name = 'mycuteness')
    async def command_mycuteness(self, ctx: Context):
        await self.__myCutenessCommand.handleCommand(ctx)

    @commands.command(name = 'mycutenesshistory')
    async def command_mycutenesshistory(self, ctx: Context):
        await self.__myCutenessHistoryCommand.handleCommand(ctx)

    @commands.command(name = 'pbs')
    async def command_pbs(self, ctx: Context):
        await self.__pbsCommand.handleCommand(ctx)

    @commands.command(name = 'pkmon')
    async def command_pkmon(self, ctx: Context):
        await self.__pkMonCommand.handleCommand(ctx)

    @commands.command(name = 'pkmove')
    async def command_pkmove(self, ctx: Context):
        await self.__pkMoveCommand.handleCommand(ctx)

    @commands.command(name = 'race')
    async def command_race(self, ctx: Context):
        await self.__raceCommand.handleCommand(ctx)

    @commands.command(name = 'sa')
    async def command_sa(self, ctx: Context):
        await self.__superAnswerCommand.handleCommand(ctx)

    @commands.command(name = 'sanswer')
    async def command_sanswer(self, ctx: Context):
        await self.__superAnswerCommand.handleCommand(ctx)

    @commands.command(name = 'superanswer')
    async def command_superanswer(self, ctx: Context):
        await self.__superAnswerCommand.handleCommand(ctx)

    @commands.command(name = 'supertrivia')
    async def command_supertrivia(self, ctx: Context):
        await self.__superTriviaCommand.handleCommand(ctx)

    @commands.command(name = 'swquote')
    async def command_swquote(self, ctx: Context):
        await self.__swQuoteCommand.handleCommand(ctx)

    @commands.command(name = 'tamales')
    async def command_tamales(self, ctx: Context):
        await self.__tamalesCommand.handleCommand(ctx)

    @commands.command(name = 'time')
    async def command_time(self, ctx: Context):
        await self.__timeCommand.handleCommand(ctx)

    @commands.command(name = 'translate')
    async def command_translate(self, ctx: Context):
        await self.__translateCommand.handleCommand(ctx)

    @commands.command(name = 'triviascore')
    async def command_triviascore(self, ctx: Context):
        await self.__triviaScoreCommand.handleCommand(ctx)

    @commands.command(name = 'twitter')
    async def command_twitter(self, ctx: Context):
        await self.__twitterCommand.handleCommand(ctx)

    @commands.command(name = 'weather')
    async def command_weather(self, ctx: Context):
        await self.__weatherCommand.handleCommand(ctx)

    @commands.command(name = 'word')
    async def command_word(self, ctx: Context):
        await self.__wordCommand.handleCommand(ctx)
