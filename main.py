import pygame, os, random, time
pygame.init()

SCREEN_WIDTH = 576
SCREEN_HEIGHT = 768
FPS = 120

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("FlappyBird")

main_font = pygame.font.Font( "assets/04B_19.ttf", 40)

bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "background-day.png")).convert_alpha())
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")).convert_alpha())
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "pipe-green.png")).convert_alpha())
bird_imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "yellowbird-down.png")).convert_alpha()), pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "yellowbird-mid.png")).convert_alpha()), pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "yellowbird-up.png")).convert_alpha())]

menu_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "menu.png")).convert_alpha())
menu_img_rect = menu_img.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
go_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "gameover.png")).convert_alpha())

hit_snd = pygame.mixer.Sound(os.path.join("sound","sfx_hit.wav"))
point_snd = pygame.mixer.Sound(os.path.join("sound","sfx_point.wav"))

clock = pygame.time.Clock()

class Bird(): 
    VEL = 4
    DELAY = 5

    def __init__(self, x, y): 
        self.x = x 
        self.y = y 

        self.gravity = 0.25
        self.movement = 0
        self.img_count = 0
        self.imgs = bird_imgs
        self.img =  self.imgs[0]

    def draw(self, screen):
        self.img_count += 1

        if self.img_count <= self.DELAY: 
            self.img = self.imgs[0] 
        elif self.img_count <= self.DELAY * 2: 
            self.img = self.imgs[1]
        elif self.img_count <= self.DELAY * 4:
            self.img = self.imgs[2]
        elif self.img_count <= self.DELAY * 6:
            self.img = self.imgs[1]
        elif self.img_count <= self.DELAY * 8: 
            self.img = self.imgs[0]
            self.img_count = 0

        if self.movement >= 5.0:
            self.img = self.imgs[1]  
        blitRotateCenter(self.img, (self.x, self.y), self.movement * -5)

    def move(self):
        self.movement += self.gravity
        self.y += self.movement

    def jump(self): 
        if self.y > 0: 
            self.movement = 0 
            self.movement -= self.VEL

class Pipe(): 
    GAP = 200
    VEL = 2

    def __init__(self, x):
        self.x = x 
        self.height = 0 
        
        self.top = 0 
        self.bottom = 0 

        self.gap = 100

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.randrange(70, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.top)) 
        screen.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def move(self): 
        self.x -= self.VEL

    def collision(self, bird, screen): 
        bird_rect = pygame.Rect(bird.x, bird.y, 68, 48)
        top_rect = pygame.Rect(self.x, self.top, 104, 640)
        bottom_rect = pygame.Rect(self.x, self.bottom, 104, 640)

        b_colide = bird_rect.colliderect(bottom_rect)
        t_colide = bird_rect.colliderect(top_rect)
        
        if b_colide or t_colide:
            return True 
 
        return False

class Base():
    VEL = 2

    def __init__(self): 
        self.x =  0
        self.y = 650 

    def draw(self, screen): 
        screen.blit(base_img, (self.x, self.y))
        screen.blit(base_img, (self.x + SCREEN_WIDTH, self.y))


    def move(self): 
        self.x -= self.VEL
        if self.x <= - SCREEN_WIDTH: 
            self.x = 0

def blitRotateCenter(image, position, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center = image.get_rect(topleft = position).center)

    screen.blit(rot_image, rot_rect.topleft)

def gameOverScreen(screen):
    go_text = main_font.render("Press any key to restart", 1, (255, 255, 255))
    go_text_rect = go_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 25))

    screen.blit(go_img,(SCREEN_WIDTH / 2 - 192, SCREEN_HEIGHT / 2 - 200))
    screen.blit(go_text, go_text_rect)
    
    pygame.display.flip()
    run = True 
    while run: 
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
                break

            if event.type == pygame.KEYUP: 
                main(screen)
                run = False

def main(screen): 
    run = True
    floor = Base()

    bird = Bird(SCREEN_WIDTH / 2 - 48, 500)
    pipes = [Pipe(700)]

    game = False 
    lost = False

    score = 0

    def redrawGameWin(screen): 
        screen.blit(bg_img, (0, 0)) 
        for pipe in pipes: 
            pipe.draw(screen)

        score_text = main_font.render(str(score), 1, (255, 255, 255))
        score_text_rect = score_text.get_rect(center = (288, 75))
        floor.draw(screen)
        bird.draw(screen)
        if game: 
            screen.blit(score_text, score_text_rect)
        else:
            screen.blit(menu_img, menu_img_rect)

        pygame.display.update()

    while run: 
        clock.tick(FPS)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not lost: 
            bird.jump()
            if not game:
                game = True

        if game:
            bird.move()

        if not lost:
            floor.move()

            if game:
                add_pipe = False
                temp = []
                for pipe in pipes: 
                    pipe.move()

                    if pipe.collision(bird, screen):
                        lost = True
                        hit_snd.play()

                    if pipe.x < 0: 
                        temp.append(pipe) 

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True

                if add_pipe: 
                    score += 1
                    point_snd.play()
                    pipes.append(Pipe(600))

        # if floor collision than break the whole loop
        if bird.y + 48 >= 650:
            break

        redrawGameWin(screen)

    gameOverScreen(screen)

main(screen)