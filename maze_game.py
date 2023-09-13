import os

from pygame.locals import *
import pygame
import numpy as np
import datetime

#adds pygame to this program
import time #adds time to program
import random

import maze_solver
from maze_solver import Dijkstra, A_star

from maze_generate import generate_maze #adds the function in another file

pygame.font.init()
# creates some fonts for use in the program
my_lowres_font1 = pygame.font.SysFont('Arial', 50)
my_lowres_font2 = pygame.font.SysFont('Arial', 220)
my_font2 = pygame.font.Font('Kenney Future Narrow.ttf', 50)
my_font3 = pygame.font.Font('Kenney Future Narrow.ttf', 220) #title

class Window:
    # list of walls
    def __init__(self, user_ID_from_login):
        # is this module running? (menu)
        self._running = True
        # is the display running?
        self._display = None
        # is the image for character present?
        self._image = None
        # user components
        self._user = None
        # is the game running? (mazes)
        self.started = False
        # is debugging mode on (algorithms)
        self.debugging = False
        # has the maze been drawn?
        self.maze_has_been_drawn = False
        # algorithms coloured points
        self.temporarily_coloured_points = []
        # is tutorial open?
        self.tutorial = False
        # tutorial image
        self.tutorial_menu = None
        # low resoloution mode?
        self.lowres = False

        #new
        #loads the user ID
        self.user_ID = user_ID_from_login
        #loads default high score
        self.high_score = 86400
        #loads filename for high score
        self.filename = "users_info.npy"
        #loads the high score
        self.load_score()



    def init(self):
        (width, height) = (1200, 690) #window dimensions/resolution
        pygame.init()
        self._display = pygame.display.set_mode((width, height), pygame.HWSURFACE)
        pygame.display.set_caption('Maze Game') #window name
        self._image = pygame.image.load("smaller.png").convert() #gets the player sprite loaded in
        self.tutorial_menu = pygame.image.load("tutorial.png").convert() #loads tutorial
        # x, y, width, height
        self.clock = pygame.time.Clock()

# sets up the a nice looking button
    def button(self, _display, position, text):
        if self.lowres == False:
            font = pygame.font.Font("Kenney Future Narrow.ttf", 30)
        else:
            font = pygame.font.SysFont('Arial', 30)

        text_render = font.render(text, 1, (0, 0, 0))
        x, y, w, h = text_render.get_rect()
        x, y = position
        pygame.draw.line(self._display, (134, 202, 234), (x, y), (x + w, y), 5) #top
        pygame.draw.line(self._display, (134, 202, 234), (x, y - 2), (x, y + h), 5) #left
        pygame.draw.line(self._display, (28, 115, 156), (x, y + h), (x + w, y + h), 5) #right
        pygame.draw.line(self._display, (28, 115, 156), (x + w, y + h), [x + w, y], 5) #bottom
        pygame.draw.rect(self._display, (37, 154, 208), (x, y, w, h)) #fill
        return self._display.blit(text_render, (x, y))

    def event(self, event):
        if event.type == QUIT:
            self._running = False

    def draw_maze_and_player(self):
        for point in self.maze.all_points():
            if self.debugging:
                pygame.draw.rect(self._display, point.get_colour_code(), point.pygame_rect)
            else:
                if point.colour == "red":
                    colour = point.get_colour_code()
                else:
                    colour = (255,255,255)
                pygame.draw.rect(self._display, colour, point.pygame_rect)

            if False and not self.maze_has_been_drawn:

                self.clock.tick(100)
                pygame.display.flip()

        # draw player!
        self._display.blit(self._image, (self._user.x, self._user.y))
        self.maze_has_been_drawn = True
        if self.debugging == True:
            self.b4 = self.button(self._display, (1052, 0), "Dijkstra")
            self.b5 = self.button(self._display, (1052, 45), "A Star")
        else:
            self.b4 = self.button(self._display, (1052, 0), "Vanilla")
            self.b5 = self.button(self._display, (0, -60), "if u can see this ur a hacker")

    def render(self): #happens every few seconds
        if self.started == False:
            self._display.fill((255, 133, 194)) #colour of background
        elif self.started == True:
            self._display.fill((62, 63, 64)) #colour of background in game

        if self.started == True:
            self.draw_maze_and_player()
        else:
            self.welcome_screen()

        self.tutorial_box()
        pygame.display.flip()

    def off(self):
        pygame.quit()

    def colour_point(self, point, colour, fps=0):
        point.colour = colour
        self.temporarily_coloured_points.append(point)
        self.render()
        if fps > 0: #fps is the number of ticks per second which is equal to frames per second as render runs on the same system
            self.clock.tick(fps)

    def colour_points_between(self, junction_A, junction_B, colour, fps=0):
        con_A = [c[0] for c in junction_A.connections]
        #con_B = [(c[0].x, c[0].y)  for c in junction_B.connections]
        index  = con_A.index(junction_B)

        #print(first_neighbour)
        just_came_from = junction_A
        current = junction_A.neighbours[index]
        midpoint = self.maze.get_point((current.x + just_came_from.x) // 2, (current.y + just_came_from.y) // 2)
        self.colour_point(midpoint, colour, fps)


        while current != junction_B:
            options = current.neighbours
            next = options[0] if options[0] != just_came_from else options[1]
            midpoint = self.maze.get_point((current.x+next.x)//2, (current.y+next.y)//2)

            self.colour_point(current, colour, fps)
            self.colour_point(midpoint, colour, fps)

            just_came_from = current
            current = next


    def reset_colours(self):
        for point in self.temporarily_coloured_points:
            point.colour = point.original_colour

    def begin(self):
        self.started = True
        # use the other file to generate maze
        self.maze = generate_maze()
        self._user = User(self.maze, self, highscore=self.high_score, filename=self.filename, userID=self.user_ID)
        print(self.maze.get_point(0, 0).colour)
        print(self.maze.get_point(0, 0).original_colour)
        self.render()
        self.maze.link_junctions_and_dead_ends(self.colour_point, self.reset_colours)
        self.tutorial_box()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.started == False:
                    if self.tutorial == True:
                        if self.b7.collidepoint(pygame.mouse.get_pos()):
                            self.tutorial = False
                    else:
                        if self.b1.collidepoint(pygame.mouse.get_pos()):
                                self.begin()

                        elif self.b2.collidepoint(pygame.mouse.get_pos()):
                            self.debugging = not self.debugging

                        elif self.b3.collidepoint(pygame.mouse.get_pos()):
                            self.clear_times()

                        elif self.b6.collidepoint(pygame.mouse.get_pos()):
                            self.tutorial = not self.tutorial
                            self.tutorial_box()

                        elif self.b8.collidepoint(pygame.mouse.get_pos()):
                            self.lowres = not self.lowres

                if self.started == True: # this stops crash in the main menu if u miss click a button
                    if self.debugging == True:

                        if self.b4.collidepoint(pygame.mouse.get_pos()):
                            maze_solver.Dijkstra.start(self, self.maze, self.colour_points_between, self.colour_point)

                        elif self.b5.collidepoint(pygame.mouse.get_pos()):
                            maze_solver.A_star.start(self, self.maze, self.colour_points_between, self.colour_point)

                if event.type == pygame.QUIT:
                    self._running = False
#new
    def clear_times(self):
        file_name = 'users_info.npy'

        if not os.path.isfile(file_name):
            return

        user_ID = str(self.user_ID)

        database = np.load(file_name, allow_pickle=True).item()

        if user_ID in database:
            database[user_ID]['high_score'] = 86400

        np.save(file_name, database)

    def execute(self):
        if self.init() == False:
            self._running = False

        while (self._running):
            self.render()

            pygame.event.pump()
            if (pygame.key.get_pressed()[K_RIGHT]):
                self._user.moveRight()
            if (pygame.key.get_pressed()[K_LEFT]):
                self._user.moveLeft()
            if (pygame.key.get_pressed()[K_UP]):
                self._user.moveUp()
            if (pygame.key.get_pressed()[K_DOWN]):
                self._user.moveDown()
            if (pygame.key.get_pressed()[K_ESCAPE]):
                self._running = False

            self.handle_events()
        self.off()

    def tutorial_box(self):
        if self.tutorial == True:
            outline = pygame.draw.rect(self._display, (255, 255, 255), (197, 97, 756, 506)) #x,y,w,h
            self._display.blit(self.tutorial_menu, (200,100))
            self.b7 = self.button(self._display, (833, 102), " CLOSE")

#new
    def load_score(self):
        file_name = 'users_info.npy'

        if not os.path.isfile(file_name):
            return None

        userID = str(self.user_ID)

        database = np.load(file_name, allow_pickle=True).item()

        if userID in database:
            users_record = database[userID]
            if isinstance(users_record, int):
                score = users_record
            else:
                score = users_record.get('high_score')
            return int(score)

        return None

    #new
    def load_username(self):
        # find name of database
        file_name = 'users_info.npy'
        # if the file does not exist, return None
        if not os.path.isfile(file_name):
            return None

        user_ID = str(self.user_ID)
        # load the database
        database = np.load(file_name, allow_pickle=True).item()
        # if the user is in the database, return the username
        if user_ID in database:
            users_record = database[user_ID]
            if isinstance(users_record, dict):
                username = users_record.get('username')
                return username

        return None

    def welcome_screen(self):
        text_surface = my_font3.render("Lost", False, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(300, -20))
        self._display.blit(text_surface, text_rect)

        text_surface = my_font2.render("Use the arrow keys to move", False, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(200, 300))
        self._display.blit(text_surface, text_rect)

        score = self.load_score()
        if score is not None:
            time_in_sec = datetime.timedelta(seconds=score)
            text_surface = my_font2.render("Best time for " + str(self.load_username()) + ": " + str(time_in_sec),False, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(150, 250))
            self._display.blit(text_surface, text_rect)

        self.b1 = self.button(self._display, (410, 400), " Begin")
        self.b2 = self.button(self._display, (410, 450), " Debugging: " + str(self.debugging))
        self.b3 = self.button(self._display, (410, 500), " Clear Times")
        self.b6 = self.button(self._display, (410, 550), " Tutorial")
        self.b8 = self.button(self._display, (410, 600), " Low Res: " + str(self.lowres))


class User:
    def __init__(self, given_maze, window, highscore, filename,userID):
        # maze coordinates, (0, 0), (1, 0), (2, 0)
        # position of the user is in pixels
        self.window = window
        self.maze_start_time = None
        self.maze_end_time = None
        self.maze = given_maze
        self.x = self.maze.start_point.x * 30 + 5
        self.y = self.maze.start_point.y * 30 + 5
        self.speed = 2
        self.high_score = highscore
        self.filename = filename
        self.user_ID = userID

    def check_point_in_maze(self, point_in_pixels):
        # look at the Point
        # if the Point is not inside the maze, return False (they can't move there)
        # if the Point is inside the maze, return True!

        # int divide the Point in pixels by 30 and check if it is in the maze
        point = self.maze.get_point(point_in_pixels[0]//30, point_in_pixels[1]//30)
        if point != None:
            # valid, they are in the maze
            return True
        else:
            # invalid, not in the maze
            return False
#new
    def log_time(self, maze_start_time, maze_end_time):
        total_time = maze_end_time - maze_start_time
        userID = str(self.user_ID)
        database = np.load(self.filename, allow_pickle=True).item()
        if userID in database:
            users_record = database[userID]
            if users_record['high_score'] > total_time:
                users_record['high_score'] = total_time
                np.save(self.filename, database)

    def has_finished(self, corner): #this checks if the player is inside the end point
        end = self.maze.end_point

        if self.maze_end_time is None and (corner[0]//30, corner[1]//30) == (end.x,end.y):
            self.maze_end_time = time.time()
            self.log_time(self.maze_start_time, self.maze_end_time)
            self.window.started = False
        # if it hasn't started, check if it has started now!,stops player being able to got back to start of maze to pause time
        if self.maze_start_time is None:
            self.has_started(corner)

    def has_started(self,corner):
        #print("checking")
        start =self.maze.start_point
        if (corner[0]//30, corner[1]//30) != (start.x,start.y):
            self.maze_start_time = time.time()
            self.window.colour_point(start, "pink", 4)
            self.window.colour_point(start, "red", 4)
            self.window.colour_point(start, "pink", 4)
            self.window.colour_point(start, "red", 4) #makes it flash

    def moveUp(self):
        player_top_left = (self.x, self.y - self.speed)
        player_top_right = (self.x + 20, self.y - self.speed)

        tl_inside = self.check_point_in_maze(player_top_left)
        tr_inside = self.check_point_in_maze(player_top_right)
        if tl_inside and tr_inside:
            self.y = -self.speed + self.y
            self.has_finished(player_top_left)


    def moveDown(self):
        player_bottom_left = (self.x, self.y + self.speed + 20) #adding +20 because that is the height of the square moving
        player_bottom_right = (self.x + 20, self.y + self.speed + 20)

        bl_inside = self.check_point_in_maze(player_bottom_left)
        br_inside = self.check_point_in_maze(player_bottom_right)
        if bl_inside and br_inside:
            self.y = self.speed + self.y
            self.has_finished(player_bottom_left)

    def moveRight(self):
        player_top_right = (self.x + self.speed + 20, self.y)
        player_bottom_right = (self.x + self.speed + 20, self.y + 20)

        tr_inside = self.check_point_in_maze(player_top_right)
        br_inside = self.check_point_in_maze(player_bottom_right)
        if tr_inside and br_inside:
            self.x = self.speed + self.x
            self.has_finished(player_top_right)

    def moveLeft(self):
        player_top_left = (self.x - self.speed, self.y)
        player_bottom_left = (self.x - self.speed, self.y + 20)

        tl_inside = self.check_point_in_maze(player_top_left)
        bl_inside = self.check_point_in_maze(player_bottom_left)
        if tl_inside and bl_inside:
            self.x = -self.speed + self.x
            self.has_finished(player_top_left)