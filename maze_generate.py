import random
import pygame

class maze:
    """
    The maze class holds the following
    1. points, a dictionary containing point classes which can be used to check if a point has already been visited
        * the format of the dictionary is a key like "6,8" and a value of the point class corresponding to that point
        * {"6,8": <object>, "10,20": <object> ...}
    2. start_point: this is where the player will start
    3. end_point: this is where the player will need to get to
    """
    def __init__(self):
        self.points = {} #every square everrrr
        self.start_point = None
        self.end_point = None

    def add_point(self, ppp):
        # add an item to the dictionary
        key = f"{ppp.x},{ppp.y}"
        self.points[key] = ppp

    def get_point(self, x, y):
        key = f"{x},{y}"
        # found Point will be None if the Point is not in the maze
        found_point = self.points.get(key)
        return found_point

    def all_points(self):
        # this returns all point classes (all dictionary values)
        return self.points.values()

    def link_junctions_and_dead_ends(self, colour_point, reset_colours):
        link_junctions_and_dead_ends(self, colour_point)
        reset_colours()


COLOUR_MAP = {
    "white": (255, 255, 255),
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "pink": (240, 0, 255),
    "cyan": ( 0 , 255 , 255),
    "navy": (0, 0, 128),
}

class Point: #any path square
    """
    Point class has
    1. x (not in pixels)
    2. y
    3. colour
    4. neighbours: again this is a dictionary, very similar to maze.points above,
        * these hold other point <object>s
        * white squares are ignored (no neighbours)
        * a green square has 1-4 neighbours
        * it is marked blue if it has 1 neighbour or 3 - 4
    5. connections:
        * the keys are the point <object>s this time and the values are the distances to that object
        * a point only has connections if it is a dead end (1 neighbour) or a junction (3 - 4 neighbours)
        * a point only has connections to other dead ends/junctions
    6. pygame_rect:
        * for drawing purposes
    """
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.original_colour = colour
        self.neighbours = [] # right next to the square
        self.connections = [] #nearest junctions, deadends
        self.pygame_rect = pygame.rect.Rect(self.x*30, self.y*30, 30,30)

    def add_neighbour(self, ppp):
        # remember only for green squares
        self.neighbours.append(ppp)
    # gets the points that are the next junctions/deadends from selcected point
    def get_neighbours(self):
        return self.neighbours
    # gets colour info
    def get_colour_code(self):
        return COLOUR_MAP[self.colour]

    def add_connection(self, junction, distance):
        # remember only for junctions and dead ends
        self.connections.append([junction, distance])


def get_unvisited_neighbour(MAZE, current):
    """
    Suppose you are at (10, 10)
    well you have 4 possible neighbours
        * (8, 10)
        * (10, 8)
        * (12, 10)
        * (10, 12)
    "unvisited" means that that square is not already part of the maze
    this function will just select a random one of the unvisited ones

    if there are no potential neighbours (all visited already) then return "no choice"
    """
    # part of the maze creation algorithm
    x = current.x
    y = current.y
    potential_neighbours = []

    # use maze.get_point to determine if the point has already been visited!
    if x - 2 >= 0 and MAZE.get_point(x - 2, y) == None:
        left = Point(x - 2, y, "green")
        potential_neighbours.append(left)

    if x + 2 <= 34 and MAZE.get_point(x + 2, y) == None:
        right = Point(x + 2, y, "green")
        potential_neighbours.append(right)

    if y - 2 >= 0 and MAZE.get_point(x, y - 2) == None:
        down = Point(x, y - 2, "green")
        potential_neighbours.append(down)

    if y + 2 <= 22 and MAZE.get_point(x, y + 2) == None:
        up = Point(x, y + 2, "green")
        potential_neighbours.append(up)

    if potential_neighbours == []:
        return "no choice"
    else:
        return random.choice(potential_neighbours)


def add_new_point_and_midpoint(MAZE, stack, current, next_one):
    """
    new point: green!
    midpoint: white!
    """
    # this function calculates the midpoint between
    # 1. the previous Point (1, 2)
    # 2. new Point (1, 3)
    # midpoint = (1, 2.5)
    midx = (current.x + next_one.x)//2
    midy = (current.y + next_one.y)//2
    midpoint= Point(midx, midy, "white")

    # remember that current has already been added
    MAZE.add_point(midpoint)
    MAZE.add_point(next_one)
    stack.append(next_one)

    # they are neighbours of each other
    current.add_neighbour(next_one) # came from here
    next_one.add_neighbour(current) # arrived here

def generate_maze(): # LINK TO OTHER PROGRAMS
    """
    using an algorithm i found on wikipedia, generate a maze.
    """
    # (0, 0), (1, 0), include a midpoint (0.5, 0)
    # (0, 0), (10, 0)newPoint = Point(0, 0, "green")
    origin = Point(0, 0, "green")

    # create an instance of the maze class.
    # its not hard you just add the Point each time bro and where it came from
    MAZE = maze()
    MAZE.add_point(origin)

    # when it gets to a dead end, the item at the top of the stack has no neighbours
    # only adding green sections to this,
    stack= [origin]
    current = origin

    while len(stack) >= 1:

        # next one is either
        # 1. a random selection from the neighbours
        # 2. "no choice"
        next_one = get_unvisited_neighbour(MAZE, current)
        if next_one == "no choice":
            # dead end!!!
            stack.pop()
            # backtracking
            if stack != []:
                current = stack[-1]
        else:
            # there is a neighbour, move to that coordinate
            add_new_point_and_midpoint(MAZE, stack, current, next_one)
            current = next_one


    #visited[-1] = (visited[-1][0], visited[-1][1], "green")
    determine_start_end(MAZE)
    return MAZE

def determine_start_end(MAZE):
    possible_points = [p for p in MAZE.all_points() if p.colour == "green"]
    distance = 0
    while distance < 20:
        r1 = random.choice(possible_points)
        r2 = random.choice(possible_points)

        distance = ((r1.x - r2.x) ** 2 + (r1.y - r2.y) ** 2) ** 0.5

    # sets the start and end point
    MAZE.start_point = r1
    MAZE.end_point = r2

    # make the start point and end point
    MAZE.start_point.colour = "red"
    MAZE.end_point.colour = "red"

def get_connections(point_JorD, MAZE, colour_point):
    """
    point_JorD will be a junction or dead end (or the start or end point)
    this will follow all of the PATHWAYS
    """
    if point_JorD.colour != "red":
        ...
        #colour_point(point_JorD, "blue", 2)

    #print("################")
    for neighbouring_point in point_JorD.get_neighbours():
        if neighbouring_point.colour not in ("blue", "red"):
            ...
            #colour_point(neighbouring_point, "cyan")
        ################################### BEGIN PATHWAY
        just_came_from_point = point_JorD
        current_point = neighbouring_point
        distance = 2

        # while loop continues until you hit another junction or dead end or start point or end point
        while len(current_point.neighbours) == 2 and current_point not in (MAZE.start_point, MAZE.end_point):
            ################################ FOLLOW PATH AND MEASURE DISTANCE
            #print(current_point.neighbours)
            directions = current_point.get_neighbours()

            # there are two places it could go, one of them is where it just came from
            option1 = directions[0]
            option2 = directions[1]

            # this is to stop us going back on ourselves
            # only move to a point if it is not the one it just came from
            if option1 == just_came_from_point:
                # lets say that it just came from option 1
                # save the place it just came from
                just_came_from_point = current_point
                # and then i will want to make option 2 the current point
                current_point = option2
            else:
                just_came_from_point = current_point
                current_point = option1

            # increase the distance by 2
            distance += 2
            if current_point.colour not in ("blue", "red"):
                ...
                #colour_point(current_point, "cyan", 100)

        #print("DISTANCE", distance)
        point_JorD.add_connection(current_point, distance)
        # connections will be in the same order as neighbours.


def link_junctions_and_dead_ends(MAZE, colour_point):
    """
    for each junction or dead end in the maze, measure the distance to the other
        junctions and dead ends which it is linked to, and then set the <object>'s connections
    """
    for point in MAZE.all_points():
        if len(point.neighbours) == 1:  # DEAD END
            get_connections(point, MAZE, colour_point)
        elif len(point.neighbours) >= 3:  # JUNCTION
            get_connections(point, MAZE, colour_point)
        elif point == MAZE.start_point or point == MAZE.end_point:  # START OR THE END
            get_connections(point, MAZE, colour_point)