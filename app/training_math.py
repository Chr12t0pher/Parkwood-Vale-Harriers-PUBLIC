"""
training_math.py calculates the calories burnt by the runner. Will be integrated into functions.py soon.
"""


def calculate_running(speed, time):
    if speed < 5.5:
        return 472 * time
    elif speed < 6.5:
        return 590 * time
    elif speed < 7.5:
        return 679 * time
    elif speed < 8.5:
        return 797 * time
    elif speed < 9.5:
        return 885 * time
    else:
        return 944 * time


def calculate_cycling(speed, time):
    if speed < 10:
        return 236 * time
    elif 10 <= speed < 12:
        return 354 * time
    elif 12 <= speed < 14:
        return 472 * time
    elif 14 <= speed < 16:
        return 590 * time
    elif 16 <= speed < 20:
        return 708 * time
    elif speed > 20:
        return 944 * time


def calculate_swimming(stroke, time):
    if stroke == "freestyle_slow":
        return 413 * time
    elif stroke == "freestyle_fast":
        return 590 * time
    elif stroke == "backstroke":
        return 413 * time
    elif stroke == "breaststroke":
        return 590 * time
    elif stroke == "butterfly":
        return 649 * time
