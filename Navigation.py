class Navigation:
    def __init__(self, ang):
        pass


class Labyrinth:
    def __init__(self, ang=0):
        # map
        self.__lab = [[[None, None, None, None, True, False]]]
        self.size = [1, 1]
        self.zero = [0, 0]
        # position
        self.pos = [0, 0]
        self.ang = ang
        # angle from 0 to 270 degrees
        self.pure_ang = self.get_ang(self.ang)

        self.points = []

    # NAVIGATION
    def get_path(self):
        # TEST
        point = self.get_point()
        print("POINT", point)
        # print(point)
        if point:
            return self.get_motions(point[:])
        else:
            return self.get_motions([0, 0])

    def get_motions(self, point):
        # print("POINT", point)
        trajectory = self.get_trajectory([point], self.pos)
        ang = self.ang
        rotations = []
        for i in range(len(trajectory) - 1):
            d_ang = self.get_dif_rot(trajectory[i], trajectory[i+1], ang)
            ang += d_ang
            rotations.append(ang)
        print(trajectory)
        print(self.ang, rotations)
        return rotations

    def get_dif_rot(self, point1, point2, ang1):
        d_point = [point2[0] - point1[0], point2[1] - point1[1]]
        if d_point == [0, 1]:
            ang2 = 0
        if d_point == [0, -1]:
            ang2 = 180
        if d_point == [1, 0]:
            ang2 = 90
        if d_point == [-1, 0]:
            ang2 = -90
        ang = self.get_ang(ang2 - ang1)
        if ang == 270:
            return -90
        return ang

    def get_trajectory(self, path, aim):
        if path[-1] == aim or len(path) > 10:
            return path[::-1]

        pths = []
        for i in range(4):
            if self.check_dir(self.get(path[-1]), 90*i):
                pt = self.get_dir(path[-1], 90*i)
                # print(pt, path)
                if pt not in path:
                    new_path = path[:]
                    new_path.append(pt)
                    # print(new_path)
                    if new_path is not None:
                        pths.append(self.get_trajectory(new_path, aim))
        # print(pths)
        if pths:
            return min(pths, key=lambda x: len(x) if x is not None else 100000)
        else:
            return None

    def get_point(self):
        while len(self.points) > 0:
            point = self.points[-1]
            cell = self.get(point)
            if cell[0] and not self.get(self.get_dir(point, 0))[5]:
                return point
            elif cell[1] and not self.get(self.get_dir(point, 90))[5]:
                return point
            elif cell[2] and not self.get(self.get_dir(point, 180))[5]:
                return point
            elif cell[3] and not self.get(self.get_dir(point, 270))[5]:
                return point
            else:
                self.points.pop(-1)
        return None

    def check_dir(self, cell, ang):
        return cell[ang//90]

    def get_dir(self, pos, ang):
        if ang == 0:
            new_pos = [pos[0], pos[1] + 1]
        elif ang == 90:
            new_pos = [pos[0] + 1, pos[1]]
        elif ang == 180:
            new_pos = [pos[0], pos[1] - 1]
        elif ang == 270:
            new_pos = [pos[0] - 1, pos[1]]
        # print(new_pos, pos)
        return new_pos

    def get_to_scan(self):
        res = []
        cell = self.get(self.pos)
        if cell[self.get_ang(self.ang - 90) // 90] is None:
            res.append(-90)
        if cell[self.get_ang(self.ang) // 90] is None:
            res.append(0)
        if cell[self.get_ang(self.ang + 90) // 90] is None:
            res.append(90)
        return res

    def get_to_move(self):
        res = []
        cell = self.get(self.pos)
        if self.check_dir(cell, self.get_ang(self.ang + 90)) and not self.get(self.get_dir(self.pos, self.get_ang(self.ang + 90)))[5]:
            res.append(90)
        if self.check_dir(cell, self.get_ang(self.ang)) and not self.get(self.get_dir(self.pos, self.get_ang(self.ang)))[5]:
            res.append(0)
        if self.check_dir(cell, self.get_ang(self.ang - 90)) and not self.get(self.get_dir(self.pos, self.get_ang(self.ang - 90)))[5]:
            res.append(-90)
        if self.check_dir(cell, self.get_ang(self.ang + 180)) and not self.get(self.get_dir(self.pos, self.get_ang(self.ang + 180)))[5]:
            res.append(180)
        if len(res) > 1:
            # print(self.pos)
            self.points.append(self.pos)
        if res:
            return res[0]
        else:
            return None

    # SCAN

    def scan(self, angle, n):
        # self.open_cells(self.pos, angle, n)
        self.open_wall(self.pos, angle, n > 0)

    def open_wall(self, pos, angle, is_open):
        ang = self.get_ang(self.pure_ang + angle)
        # look forward
        if ang == 0:
            self.get(pos)[0] = is_open
            pos = (pos[0], pos[1] + 1)
            self.get(pos)[2] = is_open
        # look back
        elif ang == 180:
            self.get(pos)[2] = is_open
            pos = (pos[0], pos[1] - 1)
            self.get(pos)[0] = is_open
        # look right
        elif ang == 90:
            self.get(pos)[1] = is_open
            pos = (pos[0] + 1, pos[1])
            self.get(pos)[3] = is_open
        # look left
        elif ang == 270:
            self.get(pos)[3] = is_open
            pos = (pos[0] - 1, pos[1])
            self.get(pos)[1] = is_open

    def open_cells(self, pos, angle, n):
        ang = self.get_ang(self.pure_ang + angle)
        # look forward
        if ang == 0:
            self.get(pos)[0] = n > 0
            if pos != self.pos:
                self.get(pos)[2] = pos != self.pos
            pos = (pos[0], pos[1] + 1)
            if n == 0:
                self.get(pos)[2] = False
        # look back
        elif ang == 180:
            self.get(pos)[2] = n > 0
            if pos != self.pos:
                self.get(pos)[0] = pos != self.pos
            pos = (pos[0], pos[1] - 1)
            if n == 0:
                self.get(pos)[0] = False
        # look right
        elif ang == 90:
            self.get(pos)[1] = n > 0
            if pos != self.pos:
                self.get(pos)[3] = pos != self.pos
            pos = (pos[0] + 1, pos[1])
            if n == 0:
                self.get(pos)[3] = False
        # look left
        elif ang == 270:
            # left
            self.get(pos)[3] = n > 0
            # right
            if pos != self.pos:
                self.get(pos)[1] = pos != self.pos
            pos = (pos[0] - 1, pos[1])
            if n == 0:
                self.get(pos)[1] = False

        if n > 0:
            # pos is increased
            self.open_cells(pos, angle, n - 1)

    # MOTION

    def rotate(self, ang):
        self.ang += ang
        self.pure_ang = self.get_ang(self.ang)

    def move(self, n=1):
        if self.pure_ang == 0:
            self.pos = [self.pos[0], self.pos[1] + n]
        elif self.pure_ang == 180:
            self.pos = [self.pos[0], self.pos[1] - n]
        elif self.pure_ang == 90:
            self.pos = [self.pos[0] + n, self.pos[1]]
        elif self.pure_ang == 270:
            self.pos = [self.pos[0] - n, self.pos[1]]
        self.get(self.pos)[5] = True

    def get_ang(self, ang):
        a = ang % 360
        """
        if self.ang < 0:
            a = 360 - a
        """
        a /= 90
        a = round(a)*90
        return a

    # DRAW

    def get_type_cell(self, pos):
        cell = self.get(pos)
        if cell[0] is True and cell[1] is True and cell[2] is True and cell[3] is True:
            return "╋"
        elif cell[0] is True and cell[1] is True and cell[2] is True and cell[3] is True:
            return "╋"
        elif cell[1] is True and cell[2] is True and cell[3] is True:
            return "┳"
        elif cell[0] is True and cell[2] is True and cell[3] is True:
            return "┫"
        elif cell[0] is True and cell[1] is True and cell[3] is True:
            return "┻"
        elif cell[0] is True and cell[1] is True and cell[3] is True:
            return "┣"

        elif cell[2] is True and cell[3] is True:
            return "┓"
        elif cell[0] is True and cell[3] is True:
            return "┛"
        elif cell[0] is True and cell[1] is True:
            return "┗"
        elif cell[1] is True and cell[2] is True:
            return "┏"
        elif cell[0] is True and cell[2] is True:
            return "┃"
        elif cell[1] is True and cell[3] is True:
            return "━"

        elif cell[0] is True:
            return "╹"
        elif cell[1] is True:
            return "╺"
        elif cell[2] is True:
            return "╻"
        elif cell[3] is True:
            return "╸"

        else:
            return "╳"

    def draw_lab(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                print(self.get_type_cell((x - self.zero[0], self.size[1] - y-1 - self.zero[1])), end="")
            print()

    def get_checked_cell(self, pos):
        if pos == self.pos:
            return "o"
        elif all(elem is not None for elem in self.get(pos)[:-1]):
            return "1"
        elif any(elem is not None for elem in self.get(pos)[:-1]):
            return "2"
        else:
            return "3"

    def draw_checked(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                print(self.get_checked_cell((x - self.zero[0], self.size[1] - y - 1 - self.zero[1])), end="")
            print()

    # SERVISE

    def _add_line_up(self):
        # print("ADD UP")
        self.__lab.append([[None, None, None, None, False, False] for _ in range(self.size[0])])
        self.size[1] += 1
        for i in range(self.size[0]):
            if self.__lab[-2][i][0] is not None:
                self.__lab[-1][i][2] = self.__lab[-2][i][0]

    def _add_line_down(self):
        # print("ADD DOWN")
        self.__lab.insert(0, [[None, None, None, None, False, False] for _ in range(self.size[0])])
        self.size[1] += 1
        self.zero[1] += 1
        for i in range(self.size[0]):
            if self.__lab[1][i][2] is not None:
                self.__lab[0][i][0] = self.__lab[1][i][2]

    def _add_line_right(self):
        # print("ADD RIGHT")
        [self.__lab[i].append([None, None, None, None, False, False]) for i in range(self.size[1])]
        self.size[0] += 1
        for i in range(self.size[1]):
            if self.__lab[i][-2][1] is not None:
                self.__lab[i][-1][3] = self.__lab[i][-2][1]

    def _add_line_left(self):
        # print("ADD LEFT")
        [self.__lab[i].insert(0, [None, None, None, None, False, False]) for i in range(self.size[1])]
        self.size[0] += 1
        self.zero[0] += 1
        for i in range(self.size[1]):
            if self.__lab[i][1][3] is not None:
                self.__lab[i][0][1] = self.__lab[i][1][3]

    def get(self, pos):
        # print(pos[0] + self.zero[0], pos[1] + self.zero[1])
        while pos[1] + self.zero[1] >= self.size[1]:
            self._add_line_up()
        while pos[0] + self.zero[0] >= self.size[0]:
            self._add_line_right()
        while pos[1] + self.zero[1] < 0:
            self._add_line_down()
        while pos[0] + self.zero[0] < 0:
            self._add_line_left()
        return self.__lab[pos[1] + self.zero[1]][pos[0] + self.zero[0]]
"""
    # DEPRECATED

    def set_forward(self, n):
        self.open_cells(self.pos, 0, n)

    def set_right(self, n):
        self.open_cells(self.pos, 90, n)

    def set_left(self, n):
        self.open_cells(self.pos, 270, n)

    def set_size(self, size):
        # DEPRECATED
        #             top, right, back, left, visited
        self.lab = [[[None, None, None, None, False] for _ in range(size[0])] for _ in range(size[1])]
        self.lab[0][0] = [None, None, False, None, True]
        for i in range(size[0]):
            self.lab[size[1] - 1][i][0] = False
            self.lab[0][i][2] = False
        for i in range(size[1]):
            self.lab[i][0][3] = False
            self.lab[i][size[0] - 1][1] = False
"""

if __name__ == '__main__':
    lab = Labyrinth()

    # 0 0
    lab.scan(180, 0)
    lab.scan(-90, 0)
    lab.scan(0, 1)
    lab.scan(90, 0)

    # 0 1
    lab.get_to_move()
    lab.move()
    lab.scan(-90, 0)
    lab.scan(0, 1)
    lab.scan(90, 0)

    # 0 2
    lab.get_to_move()
    lab.move()
    lab.scan(-90, 0)
    lab.scan(0, 1)
    lab.scan(90, 0)

    # 0 3
    lab.get_to_move()
    lab.move()
    lab.scan(-90, 0)
    lab.scan(0, 0)
    lab.scan(90, 1)

    # 1 3
    lab.get_to_move()
    lab.rotate(90)
    lab.move()
    lab.scan(-90, 0)
    lab.scan(0, 1)
    lab.scan(90, 0)

    # 2 3
    lab.get_to_move()
    lab.move()
    lab.scan(-90, 0)
    lab.scan(0, 0)
    lab.scan(90, 1)

    # 2 2
    lab.get_to_move()
    lab.rotate(90)
    lab.move()
    lab.scan(-90, 1)
    lab.scan(0, 0)
    lab.scan(90, 1)

    # 1 2
    lab.get_to_move()
    lab.rotate(90)
    lab.move()
    lab.scan(-90, 1)
    lab.scan(0, 0)
    lab.scan(90, 0)

    # 1 1
    lab.get_to_move()
    lab.rotate(-90)
    lab.move()
    lab.scan(-90, 0)
    lab.scan(0, 1)
    lab.scan(90, 0)

    # 1 0
    lab.get_to_move()
    lab.move()
    lab.scan(-90, 1)
    lab.scan(0, 0)
    lab.scan(90, 0)

    # 2 0
    lab.get_to_move()
    lab.rotate(-90)
    lab.move()
    lab.scan(-90, 1)
    lab.scan(0, 1)
    lab.scan(90, 0)

    # 3 0
    lab.get_to_move()
    lab.move()
    lab.scan(-90, 1)
    lab.scan(0, 0)
    lab.scan(90, 0)

    # 3 1
    lab.get_to_move()
    lab.rotate(-90)
    lab.move()
    lab.scan(-90, 0)
    lab.scan(0, 1)
    lab.scan(90, 0)

    # 3 2
    lab.get_to_move()
    lab.move()
    lab.scan(-90, 1)
    lab.scan(0, 1)
    lab.scan(90, 0)

    # 3 3
    lab.move()
    lab.scan(-90, 0)
    lab.scan(0, 0)
    lab.scan(90, 0)

    # TEST
    lab.draw_lab()
    print(lab.pos, lab.pure_ang)
    print(lab.get((2, 1)), lab.points)
    lab.get_path()

    """# print("DRAW LAB")
    lab.draw_lab()
    # print(lab.size)
    # print("DRAW CHECKED")
    lab.draw_checked()

    # print("SCAN")
    lab.scan(0, 1)
    print("##########")
    lab.draw_lab()
    lab.draw_checked()

    # print("SCAN")
    lab.scan(-90, 0)
    print("##########")
    lab.draw_lab()
    lab.draw_checked()

    # print("SCAN")
    lab.scan(90, 0)
    print("##########")
    lab.draw_lab()
    lab.draw_checked()"""

    """
    print("##########")
    # print(lab.get_to_scan())
    lab.set_left(0)
    # print(lab.get_to_scan())
    lab.set_forward(3)
    # print(lab.get_to_scan())
    lab.set_right(0)
    # print(lab.get_to_scan())
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.move()
    lab.set_left(0)
    lab.set_right(0)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.move()
    lab.set_left(0)
    lab.set_right(0)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.move()
    lab.set_left(0)
    lab.set_right(2)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.rotate(90)
    lab.move()
    lab.set_left(0)
    lab.set_right(0)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.move()
    lab.set_left(0)
    lab.set_right(1)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.rotate(90)
    lab.move()
    lab.set_right(1)
    lab.set_left(1)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.rotate(90)
    lab.move()
    lab.set_left(2)
    print(lab.get((1, 2)))
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.rotate(-90)
    lab.move()
    lab.set_left(0)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.move()
    lab.set_left(2)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.rotate(-90)
    lab.move()
    lab.set_left(1)
    lab.set_right(0)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.rotate(-90)
    lab.move()
    lab.set_left(0)
    lab.set_right(0)
    lab.draw_lab()
    lab.draw_checked()

    print("##########")
    lab.rotate(180)
    lab.move()
    lab.rotate(-90)
    lab.move()
    lab.set_left(3)
    lab.set_right(0)
    lab.draw_lab()
    lab.draw_checked()

    # [[[True, False, False, False, True], [True, True, False, False, False], [True, True, False, True, False], [True, False, False, True, False]], [[True, False, True, False, False], [True, False, True, False, False], [False, False, True, False, False], [True, False, True, False, False]], [[True, False, True, False, False], [False, True, True, False, False], [True, True, False, True, False], [True, False, True, True, False]], [[False, True, True, False, False], [False, True, False, True, False], [False, False, True, True, False], [False, False, True, False, False]]]
    """