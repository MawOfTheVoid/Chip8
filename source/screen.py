import pygame


class Screen():

    def __init__(self, on_pixel_color, off_pixel_color):
        self.screen_matrix = [[0 for x in range(64)] for y in range(32)]
        self.on_pixel_color = on_pixel_color
        self.off_pixel_color = off_pixel_color
        self.rect_width = 0
        self.rect_height = 0
        self.screen_width = 800
        self.screen_height = 400
        self.is_fullscreen = False
        pygame.display.set_icon(pygame.image.load("Chip8Boy.png"))
        pygame.display.set_caption("Chip 8")
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            flags=pygame.RESIZABLE)

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            pygame.display.set_mode(
                (self.screen_width, self.screen_height),
                flags=pygame.RESIZABLE)
            self.update_rect_sizes()
            self.is_fullscreen = False
        elif self.is_fullscreen is False:
            pygame.display.set_mode(
                (0, 0), flags=pygame.FULLSCREEN)
            self.update_rect_sizes()
            self.is_fullscreen = True

    def resize(self, width, height):
        self.screen_width = width
        self.screen_height = height
        pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            flags=pygame.RESIZABLE)
        self.update_rect_sizes()

    def update_rect_sizes(self):
        self.rect_width = self.screen_width / 64
        self.rect_height = self.screen_height / 32

    def draw_matrix(self):
        pass
