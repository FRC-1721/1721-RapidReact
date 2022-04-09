/**
 * 
 * @param targetAngleInDegrees target angle from WPI's swerve kinematics optimize method
 */
public void setSparkAngle(double targetAngleInDegrees) {
    // Get the current angle of the motor by reading the current rotation count and multiplying it by 
    // an experimentally derived ratio
    double currentSparkAngle = spark.getEncoder().getPosition() * degreesPerMotorRotation;
    // Slide the target angle until it is close to the current angle
    double sparkRelativeTargetAngle = reboundValue(targetAngleInDegrees, currentSparkAngle);
    // Ask the spark to turn to the new angle. Also, convert from degrees into native motor units (rotations). 
    spark.getPIDController().setReference(sparkRelativeTargetAngle / degreesPerMotorRotation, ControlType.kPosition);
}

private double reboundValue(double value, double anchor) {
    double lowerBound = anchor - 180;
    double upperBound = anchor + 180;
    
    if (value < lowerBound) {
        value = upperBound
                + ((value - lowerBound) % (upperBound - lowerBound));
    } else if (value > upperBound) {
        value = lowerBound
                + ((value - upperBound) % (upperBound - lowerBound));
    }

    return value;
}