from wpilib.simulation import SimDeviceSim

from pyfrc.physics import drivetrains


class PhysicsEngine:
    def __init__(self, physics_controller):
        # self.physics_controller = physics_controller
        # self.drivetrain = drivetrains.TwoMotorDrivetrain(
        #    deadzone=drivetrains.linear_deadzone(0.2)
        # )

        self.sim_fp_motor = SimDeviceSim("SPARK MAX [1]")

    def update_sim(self, now, tm_diff):
        print(self.sim_fp_motor.getDouble("Velocity"))
        # l_motor = self.test.getSpeed()
        # r_motor = self.r_motor.getSpeed()

        # speeds = self.drivetrain.calculate(l_motor, r_motor)
        # self.physics_controller.drive(speeds, tm_diff)

        # optional: compute encoder
        # l_encoder = self.drivetrain.wheelSpeeds.left * tm_diff
