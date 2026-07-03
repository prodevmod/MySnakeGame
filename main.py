#imports
import pygame, sys, random, os
from pygame.math import Vector2

# Helper function to get the correct path for assets when compiled to an .exe
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#Theme function for snake
def get_tinted_image(original_image, tint_color):
    # 1. Copy the original image so we don't overwrite the base file
    tinted_surface = original_image.copy()
    
    # 2. Create a PixelArray to look at the individual pixels
    pixels = pygame.PixelArray(tinted_surface)
    
    # 3. Replace pure white (255, 255, 255) with your new theme color
    pixels.replace((255, 255, 255), tint_color)
    
    # 4. CRITICAL: Delete the pixel array to "unlock" the surface
    # so Pygame is allowed to draw it to the screen again.
    del pixels
    
    return tinted_surface

#Classes
class FRUIT:
    def __init__(self):
        #x/y pos
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)
        self.is_poison = False

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
        if self.is_poison == True:
            if apple_pois is not None:
                screen.blit(apple_pois,fruit_rect)
            else:
                pygame.draw.rect(screen,(255,0,0),fruit_rect)
        elif self.is_poison == False:
            if apple is not None:
                screen.blit(apple,fruit_rect)
            else:
                pygame.draw.rect(screen,(255,0,0),fruit_rect)

    def randomize(self):
        luck_factor = random.randint(1,10)
        
        if luck_factor == 3:
            self.is_poison = True
        else:
            self.is_poison = False
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y) 

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(0,0)
        self.new_block = False
        self.minus_block = False

        self.head_up = pygame.image.load(resource_path('Graphics/head_up.png')).convert_alpha()
        self.head_down = pygame.image.load(resource_path('Graphics/head_down.png')).convert_alpha()
        self.head_right = pygame.image.load(resource_path('Graphics/head_right.png')).convert_alpha()
        self.head_left = pygame.image.load(resource_path('Graphics/head_left.png')).convert_alpha()
            
        self.tail_up = pygame.image.load(resource_path('Graphics/tail_up.png')).convert_alpha()
        self.tail_down = pygame.image.load(resource_path('Graphics/tail_down.png')).convert_alpha()
        self.tail_right = pygame.image.load(resource_path('Graphics/tail_right.png')).convert_alpha()
        self.tail_left = pygame.image.load(resource_path('Graphics/tail_left.png')).convert_alpha()

        self.body_vertical = pygame.image.load(resource_path('Graphics/body_vertical.png')).convert_alpha()
        self.body_horizontal = pygame.image.load(resource_path('Graphics/body_horizontal.png')).convert_alpha()

        self.body_tr = pygame.image.load(resource_path('Graphics/body_tr.png')).convert_alpha()
        self.body_tl = pygame.image.load(resource_path('Graphics/body_tl.png')).convert_alpha()
        self.body_br = pygame.image.load(resource_path('Graphics/body_br.png')).convert_alpha()
        self.body_bl = pygame.image.load(resource_path('Graphics/body_bl.png')).convert_alpha()
        self.crunch_sound = pygame.mixer.Sound(resource_path('Sound/crunch.ogg'))
        self.over_sound = pygame.mixer.Sound(resource_path('Sound/over.ogg'))
        self.poison_sound = pygame.mixer.Sound(resource_path('Sound/poison.ogg'))

    def draw_snake(self,snake_head_color,snake_color):
        self.update_head_graphics(snake_head_color)
        self.update_tail_graphics(snake_color)
                    
        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical_copy,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal_copy,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl_copy,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl_copy,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr_copy,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br_copy,block_rect)

    def move_snake(self):
        if self.direction != Vector2(0, 0):
            if self.new_block == True:
                body_copy = self.body[:]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False
            elif self.minus_block == True and len(self.body) > 3:
                body_copy = self.body[:-2]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.minus_block = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]

    def update_head_graphics(self,snake_head_color):
        head_relation = self.body[1] - self.body[0]
        self.head_up_copy = get_tinted_image(self.head_up, snake_head_color)
        self.head_down_copy = get_tinted_image(self.head_down, snake_head_color)
        self.head_right_copy = get_tinted_image(self.head_right, snake_head_color)
        self.head_left_copy = get_tinted_image(self.head_left, snake_head_color)
        if head_relation == Vector2(1,0): self.head = self.head_left_copy
        elif head_relation == Vector2(-1,0): self.head = self.head_right_copy
        elif head_relation == Vector2(0,1): self.head = self.head_up_copy
        elif head_relation == Vector2(0,-1): self.head = self.head_down_copy

    def update_tail_graphics(self,snake_color):
        tail_relation = self.body[-2] - self.body[-1]
        self.tail_up_copy = get_tinted_image(self.tail_up, snake_color)
        self.tail_down_copy = get_tinted_image(self.tail_down, snake_color)
        self.tail_right_copy = get_tinted_image(self.tail_right, snake_color)
        self.tail_left_copy = get_tinted_image(self.tail_left, snake_color)
        self.body_vertical_copy = get_tinted_image(self.body_vertical, snake_color)
        self.body_horizontal_copy = get_tinted_image(self.body_horizontal, snake_color)

        self.body_tr_copy = get_tinted_image(self.body_tr, snake_color)
        self.body_tl_copy = get_tinted_image(self.body_tl, snake_color)
        self.body_br_copy = get_tinted_image(self.body_br, snake_color)
        self.body_bl_copy = get_tinted_image(self.body_bl, snake_color)

        if tail_relation == Vector2(1,0): self.tail = self.tail_left_copy
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right_copy
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up_copy
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down_copy
    
    def add_block(self):
        self.new_block  = True

    def remove_block(self):
        self.minus_block  = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_over_sound(self):
        self.over_sound.play()

    def play_poison_sound(self):
        self.poison_sound.play()

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.wall = BLOCK()
        self.fhit = False
        self.score = str(len(self.snake.body) - 3)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.score = str(len(self.snake.body) - 3)

    def draw_elements(self,grass_color,snake_head_color,snake_color):
        self.draw_grass(grass_color)
        self.wall.draw_blocks()
        if self.fruit.pos not in self.wall.blocks:
            self.fruit.draw_fruit()
        else:
            self.fruit.randomize()
        self.snake.draw_snake(snake_head_color,snake_color)
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0] and self.fruit.is_poison == False:
            self.snake.add_block()
            self.wall.blocks.insert(0,self.fruit.pos)
            self.fhit = True
            self.fruit.randomize()
            self.snake.play_crunch_sound()
            # Reset the 15 second timer
            pygame.time.set_timer(CHANGE_EVENT, 15000)
            
        elif self.fruit.pos == self.snake.body[0] and self.fruit.is_poison == True and self.fhit == False:
            self.snake.remove_block()
            self.wall.blocks.insert(0,self.fruit.pos)
            self.fhit = True
            self.fruit.randomize()
            self.snake.play_poison_sound()
            # Reset the 15 second timer
            pygame.time.set_timer(CHANGE_EVENT, 15000)

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

        for block in self.wall.blocks:
            if block == self.snake.body[0]:
                if self.fhit == False:
                    self.game_over()
                else:
                    self.fhit = False

    def draw_score(self):
        margin = 20
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(255, 213, 79))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left - margin/2,apple_rect.top - margin/2 ,apple_rect.width + score_rect.width + margin,apple_rect.height + margin)

        pygame.draw.rect(screen,(bg_theme),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)

    def game_over(self):
        global game_state
        game_state = "GAME_OVER"
        self.snake.play_over_sound()
        # Stop the timer when the game is over
        pygame.time.set_timer(CHANGE_EVENT, 0)

    def reset(self):
        self.snake.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.snake.direction = Vector2(0,0)
        self.wall.blocks = []
        self.fhit = False
        self.fruit.randomize()
    
    def draw_grass(self,grass_color):
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color, grass_rect)            

class WELCOME:
    def __init__(self):
        self.welcome_txt = "hi"

    def update(self):
        self.start_text()

    def start_text(self):
        margin = 20
        start_string = "SnakeGame"
        theme_string = "T to change theme / SPACE to Start"
        start_surface = start_font.render(start_string, True, (255, 0, 0))
        theme_surface = instr_font.render(theme_string, True, (255, 255, 255))
        
        start_x = int((cell_size * cell_number) / 2)
        start_y = int((cell_size * cell_number) / 2 - 100)
        start_rect = start_surface.get_rect(center=(start_x, start_y))

        theme_x = int((cell_size * cell_number) / 2)
        theme_y = int((cell_size * cell_number) / 2 )
        theme_rect_orig = theme_surface.get_rect(center=(theme_x, theme_y))
        
        bg_rect = pygame.Rect(
            start_rect.left - margin / 2,
            start_rect.top - margin / 2,
            start_rect.width + margin,
            start_rect.height + margin
        )
        theme_rect = pygame.Rect(
            theme_rect_orig.left - margin / 2,
            theme_rect_orig.top - margin / 2,
            theme_rect_orig.width + margin,
            theme_rect_orig.height + margin
        )

        pygame.draw.rect(screen, (bg_theme), bg_rect)
        pygame.draw.rect(screen, (bg_theme), theme_rect)
        screen.blit(start_surface, start_rect)
        screen.blit(theme_surface, theme_rect_orig)

class GAME_OVER_SCREEN:
    def __init__(self):
        self.over_txt = "hi"

    def update(self,final_score):
        self.over_text(final_score)

    def over_text(self,final_score):
        margin = 20
        over_string = "GAME OVER"
        over_surface = over_font.render(over_string, True, (255, 0, 0))
        over_score = f"Your Score: {final_score} "
        over_score_surface = over_font.render(over_score, True, (255, 213, 79))
        theme_string = "T to change theme / SPACE to Restart / ESC to LEAVE"
        theme_surface = instr_font.render(theme_string, True, (255, 255, 255))

        over_x = int((cell_size * cell_number) / 2)
        over_y = int((cell_size * cell_number) / 2 - 100)
        over_rect = over_surface.get_rect(center=(over_x, over_y))

        over_sc_x = int((cell_size * cell_number) / 2)
        over_sc_y = int((cell_size * cell_number) / 2 + 100)
        over_sc_rect = over_score_surface.get_rect(center=(over_sc_x, over_sc_y))

        theme_x = int((cell_size * cell_number) / 2)
        theme_y = int((cell_size * cell_number) / 2 )
        theme_rect_orig = theme_surface.get_rect(center=(theme_x, theme_y))
        
        bg_rect = pygame.Rect(
            over_rect.left - margin / 2,
            over_rect.top - margin / 2,
            over_rect.width + margin,
            over_rect.height + margin)
        bg_rect_two = pygame.Rect(
            over_sc_rect.left - margin / 2,
            over_sc_rect.top - margin / 2,
            over_sc_rect.width + margin,
            over_sc_rect.height + margin
        )
        theme_rect = pygame.Rect(
            theme_rect_orig.left - margin / 2,
            theme_rect_orig.top - margin / 2,
            theme_rect_orig.width + margin,
            theme_rect_orig.height + margin
        )

        pygame.draw.rect(screen, (bg_theme), bg_rect)
        screen.blit(over_surface, over_rect)
        pygame.draw.rect(screen, (bg_theme), bg_rect_two)
        screen.blit(over_score_surface , over_sc_rect)
        pygame.draw.rect(screen, (bg_theme), theme_rect)
        screen.blit(theme_surface, theme_rect_orig)

class BLOCK:
    def __init__(self):
        self.blocks = []

    def draw_blocks(self):
        for block in self.blocks:
            x_pos = int(block.x*cell_size)
            y_pos = int(block.y*cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            if wall is not None:
                screen.blit(wall,block_rect)
            else:
                pygame.draw.rect(screen,(0,255,255),block_rect)

# Starts global initializations
pygame.init()

# Layout setup
cell_size = 40
cell_number = 20
game_width = cell_size * cell_number
game_height = cell_size * cell_number

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_width = window.get_width()
window_height = window.get_height()

screen = pygame.Surface((game_width, game_height)) 

offset_x = (window_width - game_width) // 2
offset_y = (window_height - game_height) // 2

clock = pygame.time.Clock()

# NOTE: Ensure your graphics/sound files exist in these folders, or handle the exceptions!
try:
    apple = pygame.image.load(resource_path('Graphics/apple.png')).convert_alpha()
    apple_pois = pygame.image.load(resource_path('Graphics/apple_pois.png')).convert_alpha()
    wall = pygame.image.load(resource_path('Graphics/wall.png'))
    game_font = pygame.font.Font(resource_path('Graphics/et.otf'),40) 
    instr_font = pygame.font.Font(resource_path('Graphics/et.otf'),20) 
    start_font = pygame.font.Font(resource_path('Graphics/bw.otf'),90) 
    over_font = pygame.font.Font(resource_path('Graphics/bw.otf'),90) 
except:
    # Fallback to defaults if files are missing just to keep the script running for testing
    apple = None
    apple_pois = None
    wall = None
    game_font = pygame.font.Font(None, 40)
    instr_font = pygame.font.Font(None, 20)
    start_font = pygame.font.Font(None, 90)
    over_font = pygame.font.Font(None, 90)

game_state = "START"
final_score = 0
CHANGE_EVENT =  pygame.USEREVENT + 1

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()
welcome = WELCOME()
game_over_screen = GAME_OVER_SCREEN()

# Theme setups
bg_themes = [(34, 139, 34), (194, 162, 108), (20, 30, 50)]
grass_themes = [(50, 205, 50), (232, 216, 184), (35, 55, 85)]
snake_head_themes = [(255, 0, 127), (38, 58, 41), (100, 98, 48)]
snake_themes = [(100, 0, 120), (65, 90, 69), (15, 56, 15)]

current_theme_index = 0
bg_theme = bg_themes[current_theme_index]
grass_theme = grass_themes[current_theme_index]
snake_theme = snake_themes[current_theme_index]
snake_head_theme = snake_head_themes[current_theme_index]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                
        if event.type == SCREEN_UPDATE and game_state == "PLAYING":
            main_game.update()

        # Handle the timer event running out
        if event.type == CHANGE_EVENT and game_state == "PLAYING":
            main_game.fruit.randomize()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)

            if event.key == pygame.K_t and (game_state == "START" or game_state == "GAME_OVER"):
                current_theme_index = (current_theme_index + 1) % len(bg_themes)
                bg_theme = bg_themes[current_theme_index]
                grass_theme = grass_themes[current_theme_index]
                snake_head_theme = snake_head_themes[current_theme_index]
                snake_theme = snake_themes[current_theme_index]
                            
            if event.key == pygame.K_ESCAPE and game_state == "GAME_OVER":
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_SPACE:
                if game_state == "START":
                    game_state = "PLAYING"
                    # Start the 15-second timer when the game starts
                    pygame.time.set_timer(CHANGE_EVENT, 5000)
                elif game_state == "GAME_OVER":
                    main_game.reset()       
                    game_state = "PLAYING"
                    # Restart the 15-second timer when restarting the game
                    pygame.time.set_timer(CHANGE_EVENT, 5000)  

# --- Drawing Logic ---

    window.fill((0, 0, 0))

    screen.fill(bg_theme)
        
    if game_state == "PLAYING":
        main_game.draw_elements(grass_theme,snake_head_theme,snake_theme)
        final_score = len(main_game.snake.body) - 3
    elif game_state == "START":
        main_game.draw_grass(grass_theme)
        welcome.update()
    elif game_state == "GAME_OVER":
        main_game.draw_grass(grass_theme)
        game_over_screen.update(final_score)

    window.blit(screen, (offset_x, offset_y))
    
    pygame.display.update()
    clock.tick(60)