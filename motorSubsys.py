import commands2
import wpilib
import phoenix6
class motorSubsys(commands2.Subsystem):
    def __init__(self):
        self.motor1=phoenix6.hardware.TalonFX(2)
        #--CONFIG--
        motor1Config=phoenix6.configs.TalonFXConfiguration()
        motor1Config.slot0.k_p=0.1
        motor1Config.slot0.k_i=0.0
        motor1Config.slot0.k_d=0.0
        #--END CONFIG--
        self.motor1.configurator.apply(motor1Config)
        super().__init__()
    def setSpeed(self,speed):
        self.motor1.set(speed)
    def setPosition(self,position):
        self.motor1.set_position(position)


class joySubsys(commands2.Subsystem):
    def __init__(self,joystick=commands2.button.CommandXboxController):
        self.myJoy=joystick
        super().__init__()
    def getJoystick(self):
        return self.myJoy.getLeftY()

'''class motorCommand(commands2.Command):
    def __init__(self,mySubsys=motorSubsys()):
        super().__init__()
        self.addRequirements(mySubsys)
        self.motor=mySubsys
    def execute(self):
        self.motor.setSpeed(0.05)'''
class motorDefCommand(commands2.Command):
    def __init__(self,mySubsys: motorSubsys,joystickSubsys: joySubsys):
        print("DEFAULT COMMAND")
        super().__init__()
        self.addRequirements(mySubsys,joystickSubsys)
        self.motor=mySubsys
        self.joy=joystickSubsys
    def execute(self):
        print("Something1",self.joy.getJoystick())
        self.motor.setSpeed(self.joy.getJoystick())
class testDefCommand(commands2.Command):
    def __init__(self,myJoy: joySubsys):
        super().__init__()
        self.joy=myJoy
        self.addRequirements(myJoy)
    def execute(self):
        print("TESTING",self.joy.getJoystick())
