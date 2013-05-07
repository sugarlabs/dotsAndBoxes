#! /usr/bin/env python
# -*- coding: utf-8 -*-


import pygame


#pygame.draw.rect(self.captura_to_show, (0,0,255), (p[0]*self.c1, p[1]*self.c2, 5, 5), 5)

GRID_SIZE = (8, 6)
BOX_SIZE = (60, 60)
X_OFFSET = 200
Y_OFFSET = 200
T = 15
COLOR1 = (255, 0, 0)
COLOR2 = (0, 0, 255)

class Game:

    def __init__(self, parent=None):
        pygame.init()

        self.horizontal = []
        self.vertical = []
        self.x_end = 0
        self.y_end = 0
        self.screen = pygame.display.set_mode((900, 700))
        self.screen.fill((84, 185, 72))
        self.draw_grid()

    def draw_grid(self):
        #pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
        #pygame.draw.circle(s, (255, 255, 255), (100, 100), 5, 5)
        #pygame.draw.line(Surface, color, start_pos, end_pos, width=1): return Rect
        #pygame.draw.line(s, (255, 255, 255), (100, 280), (100, 240), 5)

        w = GRID_SIZE[0]
        h = GRID_SIZE[1]

        for i in range(w):
            x = i * BOX_SIZE[0] + X_OFFSET
            self.horizontal.append(x)
            for j in range(h):
                y = j * BOX_SIZE[1] + Y_OFFSET
                if i == 0:
                    self.vertical.append(y)

                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 5, 5)

        self.x_end = (len(self.horizontal) - 1) * BOX_SIZE[0] + X_OFFSET
        self.y_end = (len(self.vertical) - 1) * BOX_SIZE[1] + Y_OFFSET

        print self.horizontal
        print self.vertical

    def where_x(self, x):
        for i in range(len(self.horizontal)):
            if i > 0:
                x1 = self.horizontal[i - 1]
                x2 = self.horizontal[i]
                if x >= x1 and x <= x2:
                    return x1, x2
        return False

    def where_y(self, y):
        for j in range(len(self.vertical)):
            if j > 0:
                y1 = self.vertical[j - 1]
                y2 = self.vertical[j]
                if y >= y1 and y <= y2:
                    return y1, y2
        return False

    def where(self, pos):
        x, y = pos
        r1 = self.where_x(x)
        r2 = self.where_y(y)

        if not(r1 == False):
            if not(r2 == False):
                if x < (r1[0] + T):
                    #print 'cerca de', r1[0]
                    pygame.draw.line(self.screen, COLOR1, (r1[0],r2[0]), (r1[0],r2[1]), 5)
                    return
                elif x > (r1[1] - T):
                    #print 'cerca de', r1[1]
                    pygame.draw.line(self.screen, COLOR1, (r1[1],r2[0]), (r1[1],r2[1]), 5)
                    return
        else:
            if (x > (X_OFFSET - T)) and (x < X_OFFSET):
                if not(r2 == False):
                    pygame.draw.line(self.screen, COLOR1, (X_OFFSET,r2[0]), (X_OFFSET,r2[1]), 5)
                    return
            elif (x < (self.x_end + T)) and (x > self.x_end):
                if not(r2 == False):
                    pygame.draw.line(self.screen, COLOR1, (self.x_end,r2[0]), (self.x_end,r2[1]), 5)
                    return

        if not(r2 == False):
            if not(r1 == False):
                if y < (r2[0] + T):
                    #print 'aloja', r2[0]
                    pygame.draw.line(self.screen, COLOR2, (r1[0],r2[0]), (r1[1],r2[0]), 5)
                    return
                elif y > (r2[1] - T):
                    #print 'aloja', r2[1]
                    pygame.draw.line(self.screen, COLOR2, (r1[0],r2[1]), (r1[1],r2[1]), 5)
                    return
        else:
            if (y > Y_OFFSET - T) and (y < Y_OFFSET):
                if not(r1 == False):
                    pygame.draw.line(self.screen, COLOR2, (r1[0],Y_OFFSET), (r1[1],Y_OFFSET), 5)
                    return
            elif (y < (self.y_end + T)) and (y > self.y_end):
                if not(r1 == False):
                    pygame.draw.line(self.screen, COLOR2, (r1[0],self.y_end), (r1[1],self.y_end), 5)
                    return


    def run(self):

        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    print pos
                    self.where(pos)

            pygame.display.flip()

if __name__ == '__main__':
    g = Game()
    g.run()
