from CynanBot.cheerActions.wizards.absSteps import AbsSteps
from CynanBot.cheerActions.wizards.soundAlertStep import SoundAlertStep
from CynanBot.cheerActions.wizards.stepResult import StepResult


class SoundAlertSteps(AbsSteps):

    def __init__(self):
        self.__step = SoundAlertStep.BITS

    def getStep(self) -> SoundAlertStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case SoundAlertStep.BITS:
                self.__step = SoundAlertStep.TAG
                return StepResult.NEXT

            case SoundAlertStep.TAG:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next SoundAlertStep: \"{currentStep}\"')
