import multiprocessing

from collections import OrderedDict
import pygame
import theremin2
from theremin2 import Note


width = 480
height = 320
fps = 30

white = (255, 255, 255)
black = (0, 0, 0)


menu_config = OrderedDict([
    ('Calibrate', 'calibrate'),
    ('Select sound', OrderedDict([
        ('Sine', 'select_sine'),
        ('Square', 'select_square')
    ]))
])


class State:
    def __init__(self):
        self.items = list()

    def add(self, key, value):
        self.items.append((key, value))


class View:
    def __init__(self, view_config, parent=None):
        self.config = State()
        self.build_config(view_config)
        self.parent = parent

    def build_config(self, view_config):
        for k, v in view_config.items():
            if isinstance(v, OrderedDict):
                self.config.add(k, View(v, parent=self))
            else:
                self.config.add(k, v)


def main(in_q, out_q):
    """
    Main GUI handler.

    in_q and out_q are thread-safe queues to communicate between logic and GUI.
    """
    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    view = View(menu_config)

    font = pygame.font.Font(None, 40)
    running = True
    buttons = []  # list of (button_obj, action) tuples
    while running:
        # clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                out_q.put('quit')
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in buttons:
                    if button.collidepoint(event.pos):
                        if isinstance(action, View):
                            view = action
                        else:
                            # out_q.put(action)
                            print(action)
                        break
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    out_q.put(-1)
                if event.key == pygame.K_RIGHT:
                    out_q.put(1)

        while not in_q.empty():
            msg = in_q.get()
            # Handle
            print(msg)

        screen.fill(black)

        button_height = 40
        buttons = []
        for text, action in view.config.items:
            text_obj = font.render(text, True, white)
            button_obj = text_obj.get_rect(center=(int(width / 2), button_height))
            screen.blit(text_obj, button_obj)
            buttons.append((button_obj, action))
            button_height += 40
        if view.parent:
            text_obj = font.render('Back', True, white)
            button_obj = text_obj.get_rect(center=(int(width / 2), button_height))
            screen.blit(text_obj, button_obj)
            buttons.append((button_obj, view.parent))

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    from multiprocessing import Queue
    in_q = Queue()
    out_q = Queue()

    audio_process = multiprocessing.Process(target=theremin2.main, args=(out_q, in_q))
    audio_process.start()
    main(in_q, out_q)