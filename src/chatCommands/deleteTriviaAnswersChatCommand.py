from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from ..trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from ..trivia.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class DeleteTriviaAnswersChatCommand(AbsChatCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        answerDelimiter: str = ', '
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise TypeError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise TypeError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(answerDelimiter, str):
            raise TypeError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__answerDelimiter: str = answerDelimiter

    async def handleChatCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('DeleteTriviaAnswersCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but not enough arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to delete additional trivia answers as not enough arguments were given. Example: !deletetriviaanswers {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        emote: str | None = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('DeleteTriviaAnswersCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to delete additional trivia answers as an invalid emote argument was given. Example: !deletetriviaanswers {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if reference is None:
            self.__timber.log('DeleteTriviaAnswersCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")')
            return

        result = await self.__additionalTriviaAnswersRepository.deleteAdditionalTriviaAnswers(
            triviaId = reference.triviaId,
            triviaQuestionType = reference.triviaType,
            triviaSource = reference.triviaSource,
        )

        if result is None:
            await self.__twitchUtils.safeSend(ctx, f'{reference.emote} There are no additional trivia answers for {reference.triviaSource.toStr()}:{reference.triviaId}')
        else:
            additionalAnswers = self.__answerDelimiter.join(result.answerStrings)
            await self.__twitchUtils.safeSend(ctx, f'{reference.emote} Deleted additional trivia answers for {result.triviaSource.toStr()}:{result.triviaId} — {additionalAnswers}')

        self.__timber.log('DeleteTriviaAnswersCommand', f'Handled !deletetriviaanswers command with {result} for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')