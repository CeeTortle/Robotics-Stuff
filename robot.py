
import wpilib
import commands2
from robotContainer import robotContainer
class myRobot(commands2.TimedCommandRobot):
    def robotInit(self):
        self.rContainer=robotContainer()
    def teleopInit(self):
        pass
