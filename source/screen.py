import pygame


class Screen():

    def __init__(self, on_pixel_color, off_pixel_color):
        self.monitor_width = pygame.display.Info().current_w
        self.monitor_height = pygame.display.Info().current_h
        self.screen_matrix = [[0 for x in range(64)] for y in range(32)]
        # self.screen_matrix[31][63] = 1
        self.on_pixel_color = on_pixel_color
        self.off_pixel_color = off_pixel_color
        self.rect_width = 0
        self.rect_height = 0
        self.screen_width = 800
        self.screen_height = 400
        self.is_fullscreen = False
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.update_rect_sizes(self.screen_width, self.screen_height)
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
            self.is_fullscreen = False
            self.update_rect_sizes(self.screen_width, self.screen_height)
        elif self.is_fullscreen is False:
            pygame.display.set_mode(
                (self.monitor_width, self.monitor_height), flags=pygame.FULLSCREEN)
            self.is_fullscreen = True
            self.update_rect_sizes(self.monitor_width, self.monitor_height)

    def resize(self, width, height):
        self.screen_width = width
        self.screen_height = height
        pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            flags=pygame.RESIZABLE)
        self.update_rect_sizes(self.screen_width, self.screen_height)

    def update_rect_sizes(self, width, height):
        self.rect_width = width / 64
        self.rect_height = height / 32

    def draw_matrix(self):
        self.screen.fill(self.off_pixel_color)
        for row_number, row in enumerate(self.screen_matrix):
            rect_top = self.rect_height * row_number
            for pixel_number, pixel in enumerate(row):
                if pixel:
                    pygame.draw.rect(
                        self.screen, self.on_pixel_color,
                        pygame.Rect(
                            pixel_number * self.rect_width,
                            rect_top, self.rect_width,
                            self.rect_height)
                    )
        self.clock.tick(240)
        pygame.display.flip()
