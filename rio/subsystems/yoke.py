# FRC 1721
# 2022

# This code is kind of a yoke - Khan

import math

from commands2 import SubsystemBase

from ctre import TalonFX, ControlMode
from networktables import NetworkTables
from rev import CANSparkMax, CANSparkMaxLowLevel
from wpilib import RobotBase
import wpilib
from wpimath import geometry

from constants.constants import getConstants


class Yoke(SubsystemBase):
    """
    This class represents the whole yoke
    subsystem on the robot.
    """

    def __init__(self) -> None:
        super().__init__()

        self.data_index = 0
        self.data_timer = wpilib.Timer()
        self.next_data_send_time = 0
        self.DATA_SEND_FREQUENCY = 0.05
        self.data_timer.start()
        self.fake_data = [
            [ 0.2533996632758717, -0.35389611653539643 ],
            [ 1.414427764564822, 0.4532788672855945 ],
            [ 2.8520270902733444, -0.41329166658587235 ],
            [ 3.746129447213704, 0.22670305670487778 ],
            [ 4.204252742817587, 0.05700326005055989 ],
            [ 5.168114968502579, -0.19496620654409336 ],
            [ 6.266934171920824, -0.2959937758374107 ],
            [ 7.63454339751726, -0.25613216676177686 ],
            [ 8.561594018646465, 0.46773854181686425 ],
            [ 9.964721269234046, -0.014820994112597408 ],
            [ 10.77702430456722, -0.21419597232751042 ],
            [ 11.212606158886956, 0.07755683949986913 ],
            [ 12.571600701608348, 0.15113480726434214 ],
            [ 13.516059481060054, -0.4873492561424009 ],
            [ 14.293595528245058, 0.4600594927657562 ],
            [ 15.873553679001017, -0.1317821200267395 ],
            [ 16.5689113215901, -0.28137183556135237 ],
            [ 17.559804101043813, -0.38189403408025724 ],
            [ 18.419667718052526, -0.3537108525044299 ],
            [ 19.198339639628376, -0.488414992923242 ],
            [ 20.457585605365367, 0.43225855821796966 ],
            [ 21.943230082739095, 0.028229188592270305 ],
            [ 22.858697137617423, -0.2802298792314497 ],
            [ 23.33391186171871, -0.22043083111922024 ],
            [ 24.109246139002384, -0.2096253530116432 ],
            [ 25.47459783072809, 0.03835507993695231 ],
            [ 26.31898267614858, 0.4084136714024742 ],
            [ 27.87548760754496, 0.3814858092140514 ],
            [ 28.356845182797407, 0.31144505240394604 ],
            [ 29.12822409914936, -0.20460371441919678 ],
            [ 30.199157972198144, -0.12054564297816706 ],
            [ 31.736809722730484, 0.07112447150799994 ],
            [ 32.69555194519693, 0.04856344141479085 ],
            [ 33.36867801845193, 0.3312664063460069 ],
            [ 34.06563158071584, -0.23650163065013752 ],
            [ 35.16125792029471, -0.20446763859100758 ],
            [ 36.99660594656883, -0.03168776472280044 ],
            [ 37.09896595105113, -0.07732581975359687 ],
            [ 38.001497442375104, 0.4138012555060142 ],
            [ 39.53521089281847, -0.2671142390697472 ],
            [ 40.75499218136703, -0.38616241142650587 ],
            [ 41.33251172745858, -0.3181915997086968 ],
            [ 42.30679657548812, -0.39656394977238385 ],
            [ 43.7143823961107, 0.07272472885468884 ],
            [ 44.984367355472784, -0.4717395983801711 ],
            [ 45.912561784205, 0.05543391432940825 ],
            [ 46.668109512255384, -0.0638702760335017 ],
            [ 47.714485817719634, -0.46360900247555503 ],
            [ 48.40677795913262, -0.37985783829230746 ],
            [ 49.2080074864734, -0.08811125039978385 ],
            [ 50.775087189922964, 0.23956323521591227 ],
            [ 51.53960871003061, 0.4215785100155207 ],
            [ 52.637545795633464, -0.40687544687986055 ],
            [ 53.058983175071134, -0.20633347896511345 ],
            [ 54.52168676337418, 0.28064799749712854 ],
            [ 55.59449492133944, -0.23496483443675031 ],
            [ 56.752479565932646, -0.3332686825497233 ],
            [ 57.87278070551585, -0.14672306939558633 ],
            [ 58.194822514781585, -0.2660184724777872 ],
            [ 59.66271110047592, 0.31883254827347973 ],
            [ 60.275606542226285, 0.2737287660174399 ],
            [ 61.60240484525688, 0.123054476288325 ],
            [ 62.0620652052864, -0.2261111041777777 ],
            [ 63.71643245154369, -0.12400536928021655 ],
            [ 64.95043339040197, -0.23931648503120018 ],
            [ 65.12750584694706, -0.3543120290489623 ],
            [ 66.52278357754915, 0.20111978979944745 ],
            [ 67.27592568846507, -0.07941405547085623 ],
            [ 68.28255288552806, -0.3607442377384438 ],
            [ 69.07288402009651, 0.2178831728122892 ],
            [ 70.97294454113036, -0.3751756767131962 ],
            [ 71.5733900611219, -0.4212824585349626 ],
            [ 72.74196734797206, 0.3722597912919341 ],
            [ 73.66986403323605, 0.023616188314581565 ],
            [ 74.83835172462865, -0.14684640849386832 ],
            [ 75.4334269622398, -0.06571932337776909 ],
            [ 76.62504549410902, 0.2808944027768401 ],
            [ 77.61260306612888, 0.12497958763148498 ],
            [ 78.95470904898487, -0.05637179592885655 ],
            [ 79.51627397623926, -0.2619575516815378 ],
            [ 80.50399902177124, -0.22019267345717153 ],
            [ 81.5780049959997, 0.29363514457252937 ],
            [ 82.59049353747326, -0.18354009976141872 ],
            [ 83.01421782632444, -0.2679440482599058 ],
            [ 84.07831241785533, -0.31843733735377655 ],
            [ 85.546834909146, -0.4522788926540584 ],
            [ 86.99145513498377, 0.2788336530915032 ],
            [ 87.5691748461773, -0.45451481759649837 ],
            [ 88.66926851182683, -0.09004214032862667 ],
            [ 89.52117458302384, 0.37532568608801786 ],
            [ 90.49928797534004, 0.003161564024508623 ],
            [ 91.39309175114558, 0.23990372988326358 ],
            [ 92.29111904804692, -0.20585969247588998 ],
            [ 93.57550496729945, 0.035191573716821356 ],
            [ 94.36276308082181, 0.46125752953469545 ],
            [ 95.72931862645423, 0.12398002441722711 ],
            [ 96.47610322987103, 0.2939709635049641 ],
            [ 97.2703463992029, 0.19494143108599982 ],
            [ 98.10719548894046, 0.05728472966601306 ],
            [ 99.17961451044609, 0.13371026582085643 ]
        ];

        # Configure Constants
        constants = getConstants("robot_hardware")
        self.yoke_const = constants["yoke"]
        self.pid_const = self.yoke_const["pid"]

        # Configure networktables
        self.configureNetworkTables()

        # Configure all motors
        self.starShooter = CANSparkMax(
            self.yoke_const["star_shooter_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.portShooter = CANSparkMax(
            self.yoke_const["port_shooter_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.primaryYokeMotor = CANSparkMax(
            self.yoke_const["primary_motor_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        # MOVE ME
        self.primaryYokeMotor.setInverted(True)

        self.auxillaryYokeMotor = CANSparkMax(
            self.yoke_const["auxillary_motor_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.kickerMotor = CANSparkMax(
            self.yoke_const["kicker_id"],
            CANSparkMaxLowLevel.MotorType.kBrushless,
        )

        self.kickerMotor.setInverted(True)

        # Get PID controller objects
        self.primaryPID = self.primaryYokeMotor.getPIDController()
        self.primaryPIDReference = 0 # can't retrieve this from PID, so store manually
        self.auxillaryPID = self.auxillaryYokeMotor.getPIDController()
        self.starPID = self.starShooter.getPIDController()
        self.portPID = self.portShooter.getPIDController()

        # Get encoders and sensors
        self.primaryYokeMotorEncoder = self.primaryYokeMotor.getEncoder()
        self.auxillaryYokeMotorEncoder = self.auxillaryYokeMotor.getEncoder()
        self.kickerMotorEncoder = self.kickerMotor.getEncoder()

        # Configure Primary PID
        self.primaryPID.setP(self.pid_const["primary"]["kp"])
        self.primaryPID.setI(self.pid_const["primary"]["ki"])
        self.primaryPID.setD(self.pid_const["primary"]["kd"])
        self.primaryPID.setFF(self.pid_const["primary"]["ff"])
        self.primaryPID.setIMaxAccum(self.pid_const["primary"]["maxi"])
        self.primaryPID.setOutputRange(
            self.pid_const["primary"]["min_power"],
            self.pid_const["primary"]["max_power"],
        )

        # TODO: Auxillary yoke pid here

        # Ratios
        self.primaryYokeMotorEncoder.setPositionConversionFactor(
            self.pid_const["ratio"]
        )
        self.auxillaryYokeMotorEncoder.setPositionConversionFactor(
            self.pid_const["ratio"]
        )

        # A handy background timer
        self.backgroundTimer = wpilib.Timer()
        self.backgroundTimer.start()

    def configureNetworkTables(self):
        # Get an instance of networktables
        self.nt = NetworkTables.getDefault()

        # Get the smart dashboard table
        self.sd = self.nt.getTable("SmartDashboard")

        # Setup subtables
        self.thermal_table = self.sd.getSubTable("Thermals")
        self.pid_NT = self.sd.getSubTable("PID")

        # Setup all of the networktable entries
        self.primary_yoke_temp = self.thermal_table.getEntry("primary_yoke_temp")
        self.auxillary_yoke_temp = self.thermal_table.getEntry("auxillary_yoke_temp")
        self.kicker_temp = self.thermal_table.getEntry("kicker_temp")

        self.graph_data = self.pid_NT.getEntry("graph_data");
        self.graph_data.setDoubleArray([0, 0]);

        self.pid_to_visualize = self.pid_NT.getEntry("subsystem")
        self.pid_to_visualize.setString("off")

        self.primary_yoke_NT = self.pid_NT.getSubTable("primary_yoke")
        self.shooter_NT = self.pid_NT.getSubTable("shooter")

        # NOTE: you can add additional tables to this array to auto set them up
        for [table, motorName] in [[self.primary_yoke_NT, "primary"], [self.shooter_NT, "shooter"]]:
            self.publishPIDForSubsystem(table, motorName)

    def setSpeed(self, speed):
        """
        Method to drive, setting
        a value from 0 to 1 by hand, no speed
        control required.
        """

        self.portShooter.set(speed)
        self.starShooter.set(-speed)

    def setVelocity(self, velocity):
        """
        Method to set the shooter speed velocity
        via pid.
        """

        # TODO: These need to be inverted, DONT do this here, do this in init
        self.starPID.setReference(velocity, CANSparkMaxLowLevel.ControlType.kVelocity)
        self.portPID.setReference(velocity, CANSparkMaxLowLevel.ControlType.kVelocity)

    def getPrimaryAngle(self):
        return self.primaryYokeMotorEncoder.getPosition()

    def getAuxillaryAngle(self):

        return self.auxillaryYokeMotorEncoder.getPosition()

    def setPrimaryYokeAngle(self, angle: geometry.Rotation2d):
        """
        Method to update the target angle
        for the primary shooter.
        """

        # Convert rotation2d to radians
        target_radians = angle.radians()
        # Convert radians to motor rotations
        target_rotations = (target_radians / (2 * math.pi)) / self.pid_const["ratio"]

        # print(
        #     f"rotation target:{target_rotations}, current: {self.getPrimaryAngle()} temp:{self.primaryYokeMotor.getMotorTemperature()}"
        # )

        # TODO: MOVE ME
        if not self.primaryYokeMotor.getMotorTemperature() > 45:
            if not target_rotations > 0.05:
                # Set a new PID target
                self.primaryPIDReference = target_rotations
                self.primaryPID.setReference(
                    target_rotations, CANSparkMaxLowLevel.ControlType.kPosition
                )
        else:
            self.primaryYokeMotor.set(0)

    def kick(self, kickspeed):
        """
        Activates the kicker, pushing the ball
        into the wheels.
        """

        self.kickerMotor.set(kickspeed)

    def periodic(self):
        """
        Called periodically when possible,
        ie: when other commands are not running.
        Odom/constant updates go here
        """

        if self.kickerMotor.getMotorTemperature() > 80:
            self.kickerMotor.set(0)
            print("Its running a little hot")

        if self.backgroundTimer.hasElapsed(1):  # Every 1s
            self.primary_yoke_temp.setDouble(
                self.primaryYokeMotor.getMotorTemperature()
            )
            self.auxillary_yoke_temp.setDouble(
                self.auxillaryYokeMotor.getMotorTemperature()
            )
            self.kicker_temp.setDouble(self.kickerMotor.getMotorTemperature())

        # TODO: Add a condition here based on the comp environment variable
        self.checkForPIDUpdates()

    def checkForPIDUpdates(self):
        # Only update the PID visualizer if the subsystem option is set.
        # This avoids running PID updates during comp.
        subsystem = self.pid_to_visualize.getString("off")

        if subsystem == "off":
            return
        elif subsystem == "primary_yoke":
            self.updatePIDForSubsystem(self.primaryPID, self.primary_yoke_NT)
            self.publishGraphingData(self.primaryPID)
        # elif subsystem == "shooter":
        #     self.updatePIDForSubsystem(self.portPID, self.shooter_NT)
        #     TODO: Update to publish shooter PID data.
        #     self.publishGraphingData(self.portPID)
    def publishPIDForSubsystem(self, table, motorName):
        kpEntry = table.getEntry("kp")
        kiEntry = table.getEntry("ki")
        kdEntry = table.getEntry("kd")
        ffEntry = table.getEntry("ff")
        # no _ after "max" here to make it easier to parse out the key on the frontend
        maxIEntry = table.getEntry("maxi")
        maxEntry = table.getEntry("max")
        minEntry = table.getEntry("min")

        kpEntry.setDouble(self.pid_const[motorName]["kp"])
        kiEntry.setDouble(self.pid_const[motorName]["ki"])
        kdEntry.setDouble(self.pid_const[motorName]["kd"])
        ffEntry.setDouble(self.pid_const[motorName]["ff"])
        maxIEntry.setDouble(self.pid_const[motorName]["maxi"])
        maxEntry.setDouble(self.pid_const[motorName]["max_power"])
        minEntry.setDouble(self.pid_const[motorName]["min_power"])

    def publishGraphingData(self, pid):
        # CODE FOR TESTING
        if (self.data_timer.hasElapsed(self.next_data_send_time)):
            self.graph_data.setDoubleArray(self.fake_data[self.data_index])
            self.data_index = (self.data_index + 1) % len(self.fake_data);
            self.next_data_send_time = self.data_timer.get() + self.DATA_SEND_FREQUENCY
        # CODE FOR THE REAL THING
        # if (self.data_timer.hasElapsed(self.next_data_send_time)):
        #     error = self.primaryPIDReference - self.getPrimaryAngle()
        #     time = self.data_timer.get()
        #     self.graph_data.setDoubleArray([time, error])
        #     self.next_data_send_time = time + self.DATA_SEND_FREQUENCY

    def updatePIDForSubsystem(self, pid, subtable):
        """
        Get each network table value and compare to the value the PID is
        currently set to. If it differs, update the PID value.

        Built to be reused with any PID just by passing in that PID and the
        subtable that stores its PID values in Networktables.
        """
        currentP = pid.getP()
        currentI = pid.getI()
        currentD = pid.getD()
        currentFF = pid.getFF()
        currentMaxI = pid.getIMaxAccum()
        currentMax = pid.getOutputMax();
        currentMin = pid.getOutputMin();

        networkTableP = subtable.getEntry("kp").getDouble(currentP)
        networkTableI = subtable.getEntry("ki").getDouble(currentI)
        networkTableD = subtable.getEntry("kd").getDouble(currentD)
        networkTableFF = subtable.getEntry("ff").getDouble(currentFF)
        networkTableMaxI = subtable.getEntry("maxi").getDouble(currentMaxI)
        networkTableMax = subtable.getEntry("max").getDouble(currentMax)
        networkTableMin = subtable.getEntry("min").getDouble(currentMin)

        if currentP != networkTableP:
            pid.setP(networkTableP);
        if currentI != networkTableI:
            pid.setI(networkTableI);
        if currentD != networkTableD:
            pid.setD(networkTableD);
        if currentFF != networkTableFF:
            pid.setFF(networkTableFF);
        if currentMaxI != networkTableMaxI:
            pid.setIMaxAccum(networkTableMaxI);
        if (currentMax != networkTableMax) or (currentMin != networkTableMin):
            pid.setOutputRange(networkTableMin, networkTableMax)
