from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.tts.ttsEvent import TtsEvent
from CynanBotCommon.tts.ttsManagerInterface import TtsManagerInterface
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userInterface import UserInterface
from twitch.absTwitchRaidHandler import AbsTwitchRaidHandler


class TwitchRaidHandler(AbsTwitchRaidHandler):

    def __init__(
        self,
        timber: TimberInterface,
        ttsManager: Optional[TtsManagerInterface]
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')

        self.__timber: TimberInterface = timber
        self.__ttsManager: Optional[TtsManagerInterface] = ttsManager

    async def onNewRaid(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.getPayload().getEvent()

        if event is None:
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that has no event: \"{dataBundle}\"')
            return

        fromUserId = event.getFromBroadcasterUserId()
        fromUserLogin = event.getBroadcasterUserLogin()
        fromUserName = event.getBroadcasterUserName()
        toUserId = event.getToBroadcasterUserId()
        toUserLogin = event.getBroadcasterUserLogin()
        toUserName = event.getToBroadcasterUserName()
        viewers = event.getViewers()

        if not utils.isValidStr(fromUserId) or not utils.isValidStr(fromUserLogin) or not utils.isValidStr(fromUserName) or not utils.isValidStr(toUserId) or not utils.isValidStr(toUserLogin) or not utils.isValidStr(toUserName) or not utils.isValidInt(viewers):
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that is missing crucial data: ({fromUserId=}) ({fromUserLogin=}) ({fromUserName=}) ({toUserId=}) ({toUserLogin=}) ({toUserName=}) ({viewers=})')
            return

        self.__timber.log('TwitchRaidHandler', f'\"{toUserLogin}\" received raid of {viewers} from \"{fromUserLogin}\"')

        if self.__ttsManager is not None:
            await self.__ttsManager.submitTtsEvent(TtsEvent(
                message = f'Hello everyone from {fromUserName}\'s stream, welcome in. Thanks for the raid of {viewers}!',
                twitchChannel = user.getHandle(),
                userId = fromUserId,
                userName = fromUserLogin
            ))

        pass
