#!/usr/bin/env python3
from Robot import Robot
print(".\n.\n.\n.\n.\n.\n")
robot = Robot(is_debug=True)
robot.run()
"""
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.led import Leds
from time import sleep, time
from ev3dev2.sound import Sound

# INIT components
# sounds
# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sound.html
spkr = Sound()
# sensors
# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html
# cs = ColorSensor(INPUT_3)
# ts = TouchSensor(INPUT_1)
gs = GyroSensor(INPUT_3)
us = UltrasonicSensor(INPUT_1)
# motors
# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
# mm = MediumMotor(OUTPUT_D)

# spkr.speak('Wellcome to SMTU hakaton!')
spkr.speak('calibrating!')
# mm.reset()
gs.reset()
gs.calibrate()
ang=0
spkr.speak('start work')
count_wall = 0
speed = 10
while True:
    t0 = time()
    while (23 < us.distance_centimeters_continuous and count_wall != 5) or (60 < us.distance_centimeters_continuous and count_wall == 5):
        tank_drive.on(min((time()-t0)*30+5, 20), min((time()-t0)*30+5, 20))
    tank_drive.on(0, 0)
    count_wall += 1
    if count_wall in [1, 2, 3]:
        tank_drive.on_for_seconds(40, -40, 0.5)
        ang += 90
    else:
        tank_drive.on_for_seconds(-40, 40, 0.5)
        ang -= 90
    print(gs.angle, ang)
    while abs(gs.angle - ang) > 3:
        if (ang - gs.angle) > 0:
            tank_drive.on(5, -5)
        else:
            tank_drive.on(-5, 5)
    tank_drive.on(0, 0)
    # gs.reset()
    if count_wall in [1, 2, 5, 7, 11]:
        spkr.speak("found")
    # if count_wall == 5:
    #     spkr.speak("use feature")"""