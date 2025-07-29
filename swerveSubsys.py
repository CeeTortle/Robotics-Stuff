import commands2,phoenix6,wpimath
import wpimath.geometry
import wpimath.kinematics
class swerveSubsys():
    def __init__(self,driveID,turnID,turnSensorID=None):
        super().__init__()
        self.driveMotor=phoenix6.hardware.TalonFX(driveID)
        self.turnMotor=phoenix6.hardware.TalonFX(turnID)
        self.turnVariable=self.turnMotor.get_position()
        #DRIVE CONFIG
        driveConfig=phoenix6.configs.TalonFXConfiguration()
        driveConfig.slot0.k_p = 0.1
        driveConfig.slot0.k_i = 0
        driveConfig.slot0.k_d= 0
        turnConfig=phoenix6.configs.TalonFXConfiguration()
        turnConfig.slot1.k_p = 0.5
        turnConfig.slot1.k_i = 0
        turnConfig.slot1.k_d= 0
        turnConfig.closed_loop_general.continuous_wrap = True
        self.driveMotor.configurator.apply(driveConfig)
        self.turnMotor.configurator.apply(turnConfig)
        self.postion=phoenix6.controls.PositionDutyCycle(0,slot=1)
        self.dutyCycle=phoenix6.controls.DutyCycleOut(0)
        
        
        
        if turnSensorID!=None:
            self.hasSensor=True
            self.turnSensor=phoenix6.hardware.CANcoder(turnSensorID)
            self.turnVariable=self.turnSensor.get_position()
    def setState(self,desRot,desSpeed):
        print(desRot)
        self.turnMotor.set_control(self.postion.with_position(desRot))
        self.driveMotor.set_control(self.dutyCycle.with_output(desSpeed))
    def getState(self):
        print(self.turnMotor.get_position())
class driveTrainSubsys(commands2.Subsystem):
    def __init__(self):
        super().__init__()
        for i in range(4):
            num=(i+1)*2
            string=str("self.swerve"+str(i)+"=swerveSubsys("+str(num-1)+","+str(num)+")")
            print(string)
            exec(string)
        self.swerveKinematics=wpimath.kinematics.SwerveDrive4Kinematics(wpimath.geometry.Translation2d(x=0.26,y=0.32),wpimath.geometry.Translation2d(x=0.26,y=-0.32),wpimath.geometry.Translation2d(x=-0.26,y=0.32),wpimath.geometry.Translation2d(x=-0.26,y=-0.32))
    def setState(self,fb,lr,rot):
        swerveNumbers=self.swerveKinematics.toSwerveModuleStates(wpimath.kinematics.ChassisSpeeds(fb,lr,rot))
        for i in range(4):
            exec(str("self.swerve"+str(i)+".setState(float(swerveNumbers["+str(i)+"].angle.degrees()/360),float(swerveNumbers["+str(i)+"].speed_fps/3.29))"))
    def getState(self):
        self.swerve0.getState()
class joystickSubsys(commands2.Subsystem):
    def __init__(self,joystick=commands2.button.CommandXboxController):
        self.myJoy=joystick
        super().__init__()
    def getLY(self):
        return self.myJoy.getLeftY()
    def getLX(self):
        return self.myJoy.getLeftX()
class hotasSubsys(commands2.Subsystem):
    def __init__(self,joystick=commands2.button.CommandJoystick):
        self.myJoy=joystick
        super().__init__()
    def getY(self):
        return self.myJoy.getRawAxis(axis=0)
    def getZ(self):
        return self.myJoy.getRawAxis(axis=5)
    def getX(self):
        return self.myJoy.getRawAxis(axis=1)
class driveTrainCommand(commands2.Command):
    def __init__(self,driveSubsys:driveTrainSubsys,joySubsys:hotasSubsys):
        super().__init__()
        self.addRequirements(driveSubsys,joySubsys)
        self.driveTrain,self.joystick=driveSubsys,joySubsys
    def execute(self):
        self.driveTrain.setState(self.joystick.getY(),self.joystick.getX(),self.joystick.getZ())
        #self.driveTrain.getState()