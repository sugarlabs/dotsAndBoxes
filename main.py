#! /usr/bin/env python
# -*- coding: utf-8 -*-


import pygame


#pygame.draw.rect(self.captura_to_show, (0,0,255), (p[0]*self.c1, p[1]*self.c2, 5, 5), 5)

GRID_SIZE = (6, 5)
BOX_SIZE = (50, 50)
X_OFFSET = 200
Y_OFFSET = 200

class Game:

    def __init__(self, parent=None):
        pygame.init()

        self.horizontal = []
        self.vertical = []

        self.screen = pygame.display.set_mode((1200, 700))
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

        print self.horizontal
        print self.vertical

    def where_x(self, pos):
        x, y = pos
        for i in range(len(self.horizontal)):
            if i > 0:
                x1 = self.horizontal[i - 1]
                x2 = self.horizontal[i]
                if x > x1 and x < x2:
                    return x1, x2
        return False

    def run(self):

        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    print pos, self.where_x(pos)

            pygame.display.flip()

if __name__ == '__main__':
    g = Game()
    g.run()
