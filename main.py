


import pygame

self.screen = pygame.display.set_mode((1200, 900))


pygame.draw.rect(self.captura_to_show, (0,0,255), (p[0]*self.c1, p[1]*self.c2, 5, 5), 5)

self.display.fill((84, 185, 72))

pygame.display.flip()


class Main:

    def __init__(self, parent):


            run = True            
            while run:
                while gtk.events_pending():
                    gtk.main_iteration()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
