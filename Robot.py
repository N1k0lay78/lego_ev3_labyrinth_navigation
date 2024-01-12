#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor, GyroSensor
from time import sleep, time
from ev3dev2.sound import Sound

from Navigation import Labyrinth


class Robot:
    def __init__(self, map_size=(4, 4), is_debug=False):
        self.is_debug = is_debug

        # INIT components
        # sounds
        # https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sound.html
        self.__sound = Sound()
        # sensors
        # https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sensors.html
        self.__color = ColorSensor(INPUT_1)
        self.__touch = TouchSensor(INPUT_2)
        self.__ultrasonic = UltrasonicSensor(INPUT_3)
        self.__gyro = GyroSensor(INPUT_4)
        self.ang = 0
        # motors
        # https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html
        self.__drive = MoveTank(OUTPUT_A, OUTPUT_D)
        self.__lidar_motor = MediumMotor(OUTPUT_C)
        self.__color_motor = MediumMotor(OUTPUT_B)

        # Labyrinth
        self.lab = Labyrinth()
        self.cell_size_sm = 37
        self.dist_by_scan = 5
        self.dist_forward = 17
        self.move_cell_const_sm = self.cell_size_sm - self.dist_forward
        self.reset_and_calibrate()

    def run(self):
        self.wait_for_start()

        self.search()

        self.wait_for_end()

    def run_dist(self):
        while True:
            dist = self.lidar(0)
            print(round(dist), self.get_cells(dist))
            print()

    def run_for_one_wall(self):
        while True:
            self.wait_for("GO FORWARD")
            self.move()

    def run_rotate(self):
        while True:
            self.wait_for("ROTATE AROUND")
            self.rotate(180)
            self.wait_for("ROTATE LEFT")
            self.rotate(-90)
            self.wait_for("ROTATE RIGHT")
            self.rotate(90)

    def run_move(self):
        self.wait_for("START MOVE")
        while True:
            self.move()
            self.wait_for("NEXT")

    def run_lidar(self):
        self.wait_for("LOOK BEHIND")
        print(self.get_cells(dist=self.lidar(180)))
        self.wait_for("LOOK LEFT")
        print(self.get_cells(dist=self.lidar(-90)))
        self.wait_for("LOOK FORWARD")
        print(self.get_cells(dist=self.lidar(0)))
        print()
        self.wait_for("LOOK RIGHT")
        print(self.get_cells(dist=self.lidar(90)))
        print()
        self.wait_for("LOOK COMPLETE")

    def search(self):
        sleep(2)
        self.scan(180)
        # self.lab.draw_lab()
        # self.wait_for("next")
        while True:
            for ang in [90, 0, -90]:
                # print("#############")
                self.scan(ang)
                # self.lab.draw_checked()
            print()
            # self.lab.draw_lab()
            # self.wait_for("next")
            # self.wait_for("WAIT")
            move = self.lab.get_to_move()
            if move is not None and move != 180:
                self.rotate(move)
            else:
                print("PURE ANG", self.lab.pure_ang)
                print("POS", self.lab.pos, self.lab.pure_ang)
                # print("POINTS", self.lab.points)
                rotations = self.lab.get_path()
                print(rotations)
                self.wait_for("GO TO POINT")
                for rotation in rotations:
                    self.rotate(rotation)
                    self.move()
                    self.wait_for("GO TO NEXT POINT")
            self.move()
            if self.is_debug:
                print(self.lab.pos)
            print()

    def scan(self, ang):
        dist = self.lidar(ang)
        # print("SCAN", ang, self.get_cells())
        n = self.get_cells(dist=dist)
        print("SCAN", ang, round(n), end=" ")
        self.lab.scan(ang, self.get_cells())

    def lidar(self, ang):
        res = []
        angs = {}
        d_ang = 18
        d_n = 0
        for d_i in range(-d_n, d_n + 1):
            self.set_lidar_ang(ang - d_ang*d_i, speed=20)
            sleep(0.1)
            d = self.get_dist()
            res.append(d)
            angs[d] = ang - d_ang*d_i
        self.set_lidar_ang(angs[max(res)])
        return max(res)

    def move(self, n=1):
        """
        dist = self.lidar(0)
        self.set_lidar_ang(0)
        cells = self.get_cells(dist) - n

        # cells = max(cells, 0 if self.is_debug else cells)
        self.__drive.on(20, 20)
        while self.get_cells(self.get_dist() + self.move_cell_const_sm) > cells:
            pass
        """
        print("MOVE")
        self.set_lidar_ang(0)
        st_t = time()
        self.reset_color()
        det_red, det_yellow = False, False
        while (time() - st_t < 3.65) and self.get_dist() > self.dist_forward:
            self.__drive.on(20, 20)
            self.move_color()
            if time() - st_t > 0.5:
                if self.__color.color == 5:
                    det_red = True
                if self.__color.color == 4:
                    det_yellow = True

        # self.__drive.on_for_seconds(20, 20, 3.6)
        # stop motors
        self.__drive.on(0, 0)
        self.stop_color()

        if det_red and det_yellow:
            self.speak("DETECT PPLE")
        self.lab.move(n)

    def rotate(self, ang):
        if ang != 0:
            print("ROTATE", ang, end=" ")
            self.ang += ang
            self.lab.rotate(ang)
            if ang == 180:
                self.__drive.on_for_seconds(40, -40, 0.7)
            elif ang > 0:
                self.__drive.on_for_seconds(40, -40, 0.4)
            else:
                self.__drive.on_for_seconds(-40, 40, 0.4)
            while abs(self.get_angle() - self.ang) > 0:
                if (self.ang - self.get_angle()) > 0:
                    self.__drive.on(3, -3)
                else:
                    self.__drive.on(-3, 3)
            self.__drive.on(0, 0)

    def run_color(self):
        self.wait_for("reset color")
        self.reset_color()
        self.wait_for("run color")
        while True:
            self.move_color()

    def stop_color(self):
        self.__color_motor.on(0)

    def reset_color(self):
        self.__color_motor.on_to_position(10, 0)

    def move_color(self, speed=20):
        if self.__color_motor.position > -10:
            self.__color_motor.on(-speed)
        elif self.__color_motor.position < -120:
            self.__color_motor.on(speed)

    def get_angle(self):
        return self.__gyro.angle

    def get_cells(self, dist=None):
        if dist is None:
            return self.get_dist() // self.cell_size_sm
        else:
            return dist // self.cell_size_sm

    def get_dist(self):
        return self.__ultrasonic.distance_centimeters_continuous

    def set_lidar_ang(self, ang, speed=10):
        self.__lidar_motor.on_to_position(speed, ang)

    def wait_for_end(self):
        self.wait_for("press button for end")

    def wait_for_start(self):
        self.wait_for("press button for start")

    def wait_for(self, text):
        self.speak(text)
        while not self.is_touched():
            pass

    def is_touched(self):
        return self.__touch.is_pressed

    def speak(self, text):
        self.__sound.speak(text)

    def reset_and_calibrate(self):
        if self.is_debug:
            self.speak("Calibrating")
        # reset motors
        self.__color_motor.reset()
        self.__lidar_motor.reset()

        # reset and calibrate gyro
        self.__gyro.calibrate()
        self.__gyro.reset()
