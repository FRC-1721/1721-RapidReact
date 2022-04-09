import math


def reboundValue(target, datum) -> float:
    """
    https://www.chiefdelphi.com/t/wrap-around-with-rev-spark-maxes/403608/17
    Made with help from JohnGilb on Chief Delphi
    """

    lowerDatum = datum - 180  # 180 behind
    upperDatum = datum + 180  # 180 ahead

    if target < lowerDatum:
        target = upperDatum + ((target - lowerDatum) % (upperDatum - lowerDatum))
    elif target > upperDatum:
        target = lowerDatum + ((target - upperDatum) % (upperDatum - lowerDatum))

    return target


print(reboundValue(350, 15))

# for i in range(20, 60):
#     cur = 220
#     print(
#         f"New setpoint {(i * 10)}, current {cur}, rebound value {reboundValue((i * 10), cur)}"
#     )
