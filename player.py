import pygame
from random import randint

moveDelay = 95
class Player:

    def __init__(self,x,y,step):
        # Set initial player position and state
        self.x = x/2
        self.y = y/6
        self.id = 0 # Shape ID
        self.invincible = False
        self.invincibleStart = 0  # Timestamp when hit
        self.invincibleDuration = 2500  # Invicibility duration in ms
        self.step = step
        self.lastMoveTime = 0

        # Random color for each spawn
        self.randColor = (randint(80, 255),randint(80, 255),randint(80, 255))

        # Define available shapes and boundaries (image path, left offset, right offset, top offset)
        self.shape = (('assets\\T.png',50,100,50), ('assets\\I.png',0,0,150), ('assets\\LL.png',50,50,100), ('assets\\LR.png',0,50,100))

        # Load image and apply random color
        self.image = pygame.image.load(self.shape[self.id][0]).convert_alpha()
        self.image.fill(self.randColor,special_flags=pygame.BLEND_RGBA_MULT)   # Blending the random color to the colors of the sprite
        self.stretchedImage = pygame.transform.scale(self.image, (240, 240))

        # Define drawing position
        self.placement = pygame.Rect(self.x - self.shape[self.id][1], self.y - self.shape[self.id][3], 50, 50)


    def controls(self,key,x,y):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastMoveTime > moveDelay: # Movement handling with WASD
            if key[pygame.K_s]:
                self.y += self.step
            elif key[pygame.K_w]:
                self.y -= self.step
            elif key[pygame.K_a]:
                self.x -= self.step
            elif key[pygame.K_d]:
                self.x += self.step
            self.lastMoveTime = currentTime

        # Cyclical x movement and setting boundary offset to match position
        self.x = (self.x - self.shape[self.id][1])%(x - self.shape[self.id][2]) + self.shape[self.id][1]
        if self.y > y - 50:
            self.y = y - 50
        elif self.y < self.shape[self.id][3]:
            self.y = self.shape[self.id][3]

        # Hitboxes used for collision detection
        self.hitbox = (pygame.Rect(self.x,self.y +50 - self.shape[self.id][3],50,self.shape[self.id][3]),pygame.Rect(self.placement.x,self.placement.y,50+self.shape[self.id][2],50))

        self.placement = pygame.Rect(self.x - self.shape[self.id][1], self.y - self.shape[self.id][3], 50, 50)

        if self.invincible: # Checks if player is hit
            now = pygame.time.get_ticks()
            if now - self.invincibleStart > self.invincibleDuration:    # Turn off invincibility if timer expired
                self.invincible = False


    def transform(self,key,event):
        # Change shape with [ and ] keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHTBRACKET:
                self.id += 1
                self.randColor = (randint(80, 255), randint(80, 255), randint(80, 255))
            elif event.key == pygame.K_LEFTBRACKET:
                self.id -= 1
                self.randColor = (randint(80, 255), randint(80, 255), randint(80, 255))
        self.id = self.id % 4 # Cyclical shape ID

        # Reload image and apply color after transformation
        self.image = pygame.image.load(self.shape[self.id][0]).convert_alpha()
        self.image.fill(self.randColor,special_flags=pygame.BLEND_RGBA_MULT)
        self.stretchedImage = pygame.transform.scale(self.image, (240, 240))
        self.placement = pygame.Rect(self.x - self.shape[self.id][1], self.y - self.shape[self.id][3], 240,240)

    def draw(self,window):
        # Blink while invincible
        if self.invincible:
            if int(pygame.time.get_ticks() / 100) % 2  == 0:    # Blinks every 200ms
                window.blit(self.stretchedImage, self.placement)
        else:
            window.blit(self.stretchedImage, self.placement)

    def playerCollision(self,row):
        if self.invincible:
            return False    # Not colliding

        # Check for collision with any part of the row
        if self.hitbox[0].collidelist(row) != -1 or self.hitbox[1].collidelist(row) != -1:
            self.invincible = True
            self.invincibleStart = pygame.time.get_ticks()
            return True

    def restart(self,x,y,step):
        # Reset player
        self.x = x / 2
        self.y = y / 6
        self.id = 0
        self.invincible = False
        self.invincibleDuration = 2500  # invicibility duration
        self.step = step
        self.randColor = (randint(80, 255), randint(80, 255), randint(80, 255))  # creates random color
        self.image = pygame.image.load(self.shape[self.id][0]).convert_alpha()
        self.image.fill(self.randColor,special_flags=pygame.BLEND_RGBA_MULT)  # blending the random color to the colors of the sprite
        self.stretchedImage = pygame.transform.scale(self.image, (240, 240))
        self.placement = pygame.Rect(self.x - self.shape[self.id][1], self.y - self.shape[self.id][3], 50, 50)

    def pauseInvicibleUpdate(self,pauseTime):
        # Account for pause time during invincibility
        self.invincibleStart += pauseTime