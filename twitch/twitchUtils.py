import asyncio
import queue
from datetime import datetime, timedelta, timezone
from queue import SimpleQueue
from typing import List, Optional

from twitchio.abcs import Messageable

import CynanBotCommon.utils as utils
from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.sentMessageLogger.sentMessageLogger import \
    SentMessageLogger
from CynanBotCommon.timber.timber import Timber
from twitch.outboundMessage import OutboundMessage


class TwitchUtils():

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        sentMessageLogger: SentMessageLogger,
        timber: Timber,
        sleepTimeSeconds: float = 0.5,
        maxRetries: int = 3,
        queueTimeoutSeconds: int = 3,
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(sentMessageLogger, SentMessageLogger):
            raise ValueError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.25 or sleepTimeSeconds > 3:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(maxRetries):
            raise ValueError(f'maxRetries argument is malformed: \"{maxRetries}\"')
        elif maxRetries < 0 or maxRetries > utils.getIntMaxSafeSize():
            raise ValueError(f'maxRetries argument is out of bounds: {maxRetries}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__sentMessageLogger: SentMessageLogger = sentMessageLogger
        self.__timber: Timber = timber
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__maxRetries: int = maxRetries
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds
        self.__timeZone: timezone = timeZone

        self.__messageQueue: SimpleQueue[OutboundMessage] = SimpleQueue()
        backgroundTaskHelper.createTask(self.__startOutboundMessageLoop())

    def getMaxMessageSize(self) -> int:
        return 494

    async def safeSend(
        self,
        messageable: Messageable,
        message: Optional[str],
        twitchChannel: str,
        maxMessages: int = 3,
        perMessageMaxSize: int = 494
    ):
        if not isinstance(messageable, Messageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidInt(maxMessages):
            raise ValueError(f'maxMessages argument is malformed: \"{maxMessages}\"')
        elif maxMessages < 1 or maxMessages > 5:
            raise ValueError(f'maxMessages is out of bounds: {maxMessages}')
        elif not utils.isValidInt(perMessageMaxSize):
            raise ValueError(f'perMessageMaxSize argument is malformed: \"{perMessageMaxSize}\"')
        elif perMessageMaxSize < 300:
            raise ValueError(f'perMessageMaxSize is too small: {perMessageMaxSize}')
        elif perMessageMaxSize > self.getMaxMessageSize():
            raise ValueError(f'perMessageMaxSize is too big: {perMessageMaxSize} (max size is {self.getMaxMessageSize()})')

        if not utils.isValidStr(message):
            return

        if len(message) < self.getMaxMessageSize():
            await self.__safeSend(
                messageable = messageable,
                message = message,
                twitchChannel = twitchChannel
            )
            return

        messages = utils.splitLongStringIntoMessages(
            maxMessages = maxMessages,
            perMessageMaxSize = perMessageMaxSize,
            message = message
        )

        for m in messages:
            await self.__safeSend(
                messageable = messageable,
                message = m,
                twitchChannel = twitchChannel
            )

    async def __safeSend(
        self,
        messageable: Messageable,
        message: str,
        twitchChannel: str
    ):
        if not isinstance(messageable, Messageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        successfullySent: bool = False
        exceptions: Optional[List[Exception]] = None

        for index in range(self.__maxRetries):
            try:
                await messageable.send(message)
                successfullySent = True
            except Exception as e:
                self.__timber.log('TwitchUtils', f'Encountered error when trying to send outbound message (twitchChannel={twitchChannel}) (retry={index}) (len={len(message)}) \"{message}\": {e}', e)

                if exceptions is None:
                    exceptions = list()

                exceptions.append(e)

        numberOfRetries: int = 0
        if utils.hasItems(exceptions):
            numberOfRetries = len(exceptions)

        self.__sentMessageLogger.logMessage(
            successfullySent = successfullySent,
            numberOfRetries = numberOfRetries,
            exceptions = exceptions,
            msg = message,
            twitchChannel = twitchChannel
        )

        if not successfullySent:
            self.__timber.log('TwitchUtils', f'Failed to send message after {numberOfRetries} retries (twitchChannel={twitchChannel}) (len={len(message)}) \"{message}\"')

    async def __sendOutboundMessage(self, outboundMessage: OutboundMessage):
        if not isinstance(outboundMessage, OutboundMessage):
            raise ValueError(f'outboundMessage argument is malformed: \"{outboundMessage}\"')

        try:
            self.__messageQueue.put(outboundMessage, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TwitchUtils', f'Encountered queue.Full when submitting a new outbound message ({outboundMessage}) into the outbound message queue (queue size: {self.__messageQueue.qsize()}): {e}', e)

    async def __startOutboundMessageLoop(self):
        while True:
            outboundMessages: List[OutboundMessage] = list()

            try:
                while not self.__messageQueue.empty():
                    outboundMessages.append(self.__messageQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TwitchUtils', f'Encountered queue.Empty when building up Twitch messages list (queue size: {self.__messageQueue.qsize()}) (actions size: {len(outboundMessages)}): {e}', e)

            now = datetime.now(self.__timeZone)

            for outboundMessage in outboundMessages:
                if now >= outboundMessage.getDelayUntilTime():
                    await self.safeSend(
                        messageable = outboundMessage.getMessageable(),
                        message = outboundMessage.getMessage(),
                        twitchChannel = outboundMessage.getTwitchChannel()
                    )
                else:
                    await self.__sendOutboundMessage(outboundMessage)

            await asyncio.sleep(self.__sleepTimeSeconds)

    async def waitThenSend(
        self,
        messageable: Messageable,
        delaySeconds: int,
        message: str,
        twitchChannel: str
    ):
        if not isinstance(messageable, Messageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidInt(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1 or delaySeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        now = datetime.now(self.__timeZone)
        delayUntilTime = now + timedelta(seconds = delaySeconds)

        await self.__sendOutboundMessage(OutboundMessage(
            delayUntilTime = delayUntilTime,
            messageable = messageable,
            message = message,
            twitchChannel = twitchChannel
        ))
