#! /usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
import gtk
from gettext import gettext as _

LINE_SIZE = 10
T = 15
COLOR_OWNER = (255, 0, 0)
PLAYER_A = 0
PLAYER_B = 0

class box:

    def __init__(self, parent, x, y):
        self.screen = parent.screen
        self.fuente = parent.fuente
        self.box_size = parent.box_size
        self.x_offset = parent.x_offset
        self.y_offset = parent.y_offset
        self.x = x
        self.y = y
        x1 = self.x * self.box_size[0] + self.x_offset
        y1 = self.y * self.box_size[1] + self.y_offset
        dx = int(self.box_size[0] / 2.0)
        dy = int(self.box_size[1] / 2.0)
        self.pos_x = x1 + dx
        self.pos_y = y1 + dy
        self.up = 0
        self.left = 0
        self.right = 0
        self.down = 0
        self.owner = None

    def check(self):
        return ((self.up + self.left + self.right + self.down) == 4)

    def setOwner(self, owner):
        global PLAYER_A
        global PLAYER_B
        if owner == 'A':
            self.owner = 'A'
            PLAYER_A = PLAYER_A + 1
        else:
            self.owner = 'B'
            PLAYER_B = PLAYER_B + 1
        self.showOwner()
        print PLAYER_A, PLAYER_B

    def showOwner(self):
        text = self.fuente.render(self.owner, 1, COLOR_OWNER)
        textrect = text.get_rect()
        textrect.center = (self.pos_x, self.pos_y)
        self.screen.blit(text, textrect)

class Game:

    def __init__(self, parent=None):
        self.parent = parent
        self.current = 'A'
        self.grid_size = (8, 6)
        self.calc_grid_cant()
        self.box_size = (50, 50)
        self.x_offset = 100
        self.y_offset = 100
        self.back_color = (84, 185, 72)
        self.line_color = (0, 0, 0)
        self.point_color = (0, 0, 0)

    def draw_line(self, r1, r2):
        pygame.draw.line(self.screen, self.line_color, r1, r2, LINE_SIZE)

    def draw_game_end(self):
        s = self.screen.get_size()
        alphasurface = pygame.Surface(s)
        alphasurface.convert()
        alphasurface.fill((100,100,100))
        alphasurface.set_alpha(200)
        self.screen.blit(alphasurface, (0, 0))
        winner = None
        if PLAYER_A > PLAYER_B:
            winner = 'A'
        elif PLAYER_B > PLAYER_A:
            winner = 'B'
        if winner == None:
            msg = _('Empate')
        else:
            msg = _('Player %s win!') % winner
        text = self.fuente2.render(msg, 1, COLOR_OWNER)
        textrect = text.get_rect()
        s = self.screen.get_size()
        textrect.center = (int(s[0] / 2), int(s[1] / 2))
        self.screen.blit(text, textrect)
        text = self.fuente.render(_('Click to start a new game'), 1, COLOR_OWNER)
        textrect = text.get_rect()
        s = self.screen.get_size()
        textrect.center = (int(s[0] / 2), int(s[1] / 2) + 60)
        self.screen.blit(text, textrect)

    def set_board_size(self, size):
        self.grid_size = size
        self.calc_grid_cant()
        self.draw_grid()

    def calc_grid_cant(self):
        self.grid_cant = (self.grid_size[0] - 1) * (self.grid_size[1] - 1)

    def set_point_color(self, color):
        self.point_color = color
        self.draw_grid()

    def set_back_color(self, color):
        self.back_color = color
        self.draw_grid()

    def set_line_color(self, color):
        self.line_color = color
        self.draw_grid()

    def set_owner_color(self, color):
        global COLOR_OWNER
        COLOR_OWNER = color
        self.draw_grid()

    def draw_grid(self):
        global PLAYER_A
        global PLAYER_B
        PLAYER_A = 0
        PLAYER_B = 0
        self.current = 'A'
        w = self.grid_size[0]
        h = self.grid_size[1]
        s_w = self.screen.get_width()
        s_h = self.screen.get_height()

        if s_w < (w * (self.box_size[0] + 1)):
            value = int(s_w / (self.box_size[0] + 1.0)) - 1
            self.parent.h_spin_set_max(value)
            return
        else:
            xx = w * (self.box_size[0] - 1)
            self.x_offset = int((s_w - xx) / 2.0) + LINE_SIZE * 2

        if s_h < (h * (self.box_size[1] + 1)):
            value = int(s_h / (self.box_size[1] + 1.0)) - 1
            self.parent.v_spin_set_max(value)
            return
        else:
            yy = h * (self.box_size[1] - 1)
            self.y_offset = int((s_h - yy) / 2.0) + LINE_SIZE * 2

        self.screen.fill(self.back_color)
        self.horizontal = []
        self.vertical = []
        self.boxes = []
        self.x_end = 0
        self.y_end = 0

        for i in range(w):
            x = i * self.box_size[0] + self.x_offset
            self.horizontal.append(x)
            v_boxes = []
            for j in range(h):
                y = j * self.box_size[1] + self.y_offset
                if i == 0:
                    self.vertical.append(y)
                if j > 0:
                    v_boxes.append(box(self, i - 1, j - 1))
                pygame.draw.circle(self.screen, self.point_color, (x, y), LINE_SIZE)
            if i > 0:
                self.boxes.append(v_boxes)
        self.x_end = (len(self.horizontal) - 1) * self.box_size[0] + self.x_offset
        self.y_end = (len(self.vertical) - 1) * self.box_size[1] + self.y_offset

    def where_x(self, x):
        for i in range(len(self.horizontal)):
            if i > 0:
                x1 = self.horizontal[i - 1]
                x2 = self.horizontal[i]
                if x >= x1 and x <= x2:
                    return (x1, x2, i)
        return (False, False, 0)

    def where_y(self, y):
        for j in range(len(self.vertical)):
            if j > 0:
                y1 = self.vertical[j - 1]
                y2 = self.vertical[j]
                if y >= y1 and y <= y2:
                    return (y1, y2, j)
        return (False, False, 0)

    def where(self, pos):
        x, y = pos
        r1 = self.where_x(x)
        r2 = self.where_y(y)
        if not(r1[0] == False):
            if not(r2[0] == False):
                if x < (r1[0] + T):
                    x_b = r1[2] - 1
                    y_b = r2[2] - 1
                    b = self.boxes[x_b][y_b]
                    if b.left:
                        return True
                    con = False
                    b.left = 1
                    if b.check():
                        b.setOwner(self.current)
                        con = True
                    if x_b > 0:
                        b2 = self.boxes[x_b - 1][y_b]
                        b2.right = 1
                        if b2.check():
                            b2.setOwner(self.current)
                            con = True
                    self.draw_line((r1[0],r2[0]), (r1[0],r2[1]))
                    return con
                elif x > (r1[1] - T):
                    x_b = r1[2] - 1
                    y_b = r2[2] - 1
                    b = self.boxes[x_b][y_b]
                    if b.right:
                        return True
                    con = False
                    b.right = 1
                    if b.check():
                        b.setOwner(self.current)
                        con = True
                    if x_b < (self.grid_size[0] - 2):
                        b2 = self.boxes[x_b + 1][y_b]
                        b2.left = 1
                        if b2.check():
                            b2.setOwner(self.current)
                            con = True
                    self.draw_line((r1[1],r2[0]), (r1[1],r2[1]))
                    return con
        else:
            if (x > (self.x_offset - T)) and (x < self.x_offset):
                if not(r2[0] == False):
                    x_b = 0
                    y_b = r2[2] - 1
                    b = self.boxes[x_b][y_b]
                    if b.left:
                        return True
                    con = False
                    b.left = 1
                    if b.check():
                        b.setOwner(self.current)
                        con = True
                    self.draw_line((self.x_offset,r2[0]), (self.x_offset,r2[1]))
                    return con
            elif (x < (self.x_end + T)) and (x > self.x_end):
                if not(r2[0] == False):
                    x_b = self.grid_size[0] - 2
                    y_b = r2[2] - 1
                    b = self.boxes[x_b][y_b]
                    if b.right:
                        return True
                    con = False
                    b.right = 1
                    if b.check():
                        b.setOwner(self.current)
                        con = True
                    self.draw_line((self.x_end,r2[0]), (self.x_end,r2[1]))
                    return con

        if not(r2[0] == False):
            if not(r1[0] == False):
                if y < (r2[0] + T):
                    x_b = r1[2] - 1
                    y_b = r2[2] - 1
                    b = self.boxes[x_b][y_b]
                    if b.up:
                        return True
                    con = False
                    b.up = 1
                    if b.check():
                        b.setOwner(self.current)
                        con = True
                    if y_b > 0:
                        b2 = self.boxes[x_b][y_b-1]
                        b2.down = 1
                        if b2.check():
                            b2.setOwner(self.current)
                            con = True
                    self.draw_line((r1[0],r2[0]), (r1[1],r2[0]))
                    return con
                elif y > (r2[1] - T):
                    x_b = r1[2] - 1
                    y_b = r2[2] - 1
                    b = self.boxes[x_b][y_b]
                    if b.down:
                        return True
                    con = False
                    b.down = 1
                    if b.check():
                        b.setOwner(self.current)
                        con = True
                    if y_b < self.grid_size[1] - 2:
                        b2 = self.boxes[x_b][y_b+1]
                        b2.up = 1
                        if b2.check():
                            b2.setOwner(self.current)
                            con = True
                    self.draw_line((r1[0],r2[1]), (r1[1],r2[1]))
                    return con
        else:
            if (y > self.y_offset - T) and (y < self.y_offset):
                if not(r1[0] == False):
                    x_b = r1[2] - 1
                    y_b = 0
                    b = self.boxes[x_b][y_b]
                    if b.up:
                        return True
                    con = False
                    b.up = 1
                    if b.check():
                        b.setOwner(self.current)
                        con = True
                    self.draw_line((r1[0],self.y_offset), (r1[1],self.y_offset))
                    return con
            elif (y < (self.y_end + T)) and (y > self.y_end):
                if not(r1[0] == False):
                    x_b = r1[2] - 1
                    y_b = self.grid_size[1] - 2
                    b = self.boxes[x_b][y_b]
                    if b.down:
                        return True
                    con = False
                    b.down = 1
                    if b.check():
                        b.setOwner(self.current)
                    self.draw_line((r1[0],self.y_end), (r1[1],self.y_end))
                    return False


    def run(self):
        pygame.init()
        self.screen = pygame.display.get_surface()
        if not self.screen:
            self.screen = pygame.display.set_mode((900, 700))
            pygame.display.set_caption(_('Dots and boxes'))
        self.screen.fill(self.back_color)
        self.fuente = pygame.font.Font(None, self.box_size[0])
        self.fuente2 = pygame.font.Font(None, self.box_size[0] * 2)
        self.draw_grid()
        run = True
        while run:
            while gtk.events_pending():
                gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    ret = self.where(pos)
                    if ret == False:
                        if self.current == 'A':
                            self.current = 'B'
                        else:
                            self.current = 'A'
                        if self.parent:
                            self.parent.set_current_player(self.current)
            pygame.display.flip()
            if self.grid_cant == (PLAYER_A + PLAYER_B):
                self.draw_game_end()
                run2 = True
                while run2:
                    while gtk.events_pending():
                        gtk.main_iteration()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run2 = False
                            self.draw_grid()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            run2 = False
                            self.draw_grid()
                    pygame.display.flip()

if __name__ == '__main__':
    g = Game()
    g.run()
