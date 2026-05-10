import pygame
from random import randint, randrange


class Row:
    def __init__(self,x,y):
        # Row definitions: (image_path, row_height, left_hole_offset, right_hole_offset)
        self.image = (('assets\\Trow.png',100,50,50),('assets\\Irow.png',200,0,0),('assets\\LLrow.png',150,50,0),('assets\\LRrow.png',150,0,50))
        self.rowId = randint(0, 3) # Select random row type
        self.randColor = (randint(150, 255),randint(150, 255),randint(150, 255))   # Creates random color
        self.x = -randrange(50, 1300,50) # Initial X spawn
        self.y = y
        self.invisible = False  # Becomes True if player matches the row
        self.Cancled = False    # Becomes True if player collided with wrong shape
        self.moveTimer = 0      # Time counter for movement
        self.levelTimer = 1     # Used for difficulty increase
        self.level = 0
        self.moveDelay = 500    # Row move interval in ms

    def spawn(self,window):
        # Load and color the row image
        self.imagePrint = pygame.image.load(self.image[self.rowId][0]).convert_alpha()
        self.imagePrint.fill(self.randColor,special_flags=pygame.BLEND_RGBA_MULT)  # Blending the random color to the colors of the sprite
        self.stretchedImage = pygame.transform.scale(self.imagePrint, (2750, 200))
        self.placement = pygame.Rect(self.x, self.y, 2750, 200)

        # Build row hitboxes based on shape type
        if not self.invisible:
            self.hitbox = (pygame.Rect(0,self.y ,1300 + self.x,self.image[self.rowId][1]),pygame.Rect(1300+self.x,self.y + self.image[self.rowId][2]  ,50,self.image[self.rowId][1]-self.image[self.rowId][2]),pygame.Rect(1400+self.x,self.y + self.image[self.rowId][3]  ,50,self.image[self.rowId][1]-self.image[self.rowId][3]),pygame.Rect(1450 + self.x ,self.y ,-self.x,self.image[self.rowId][1]))
            self.checkHitbox = pygame.Rect(1350 + self.x,self.y + self.image[self.rowId][1] - 50,50,50)
        else:
            self.hitbox = [pygame.Rect(0, 0, 0,0)]

        currentTime = pygame.time.get_ticks()

        # Draw the row on screen
        if self.y > -200:
            if not self.invisible:
                window.blit(self.stretchedImage,self.placement)

        else:
            # Resets row position and properties when its off screen
            self.randColor = (randint(80, 255), randint(80, 255), randint(80, 255))
            self.rowId = randint(0, 3)
            self.x = -randrange(50, 1300,50)
            self.y = 1600
            self.invisible = False
            self.Cancled = False

        # Move row upwards on timer
        if currentTime - self.moveTimer > self.moveDelay:            # Timer for row going up
            self.y -= 50
            self.moveTimer = currentTime
            self.levelTimer += self.moveDelay / 1000

            # Increase level and speed every 30 seconds till level 6
            if int(self.levelTimer) % 31 == 0 and self.level < 6:
                self.levelTimer = 1
                self.level +=1
                self.moveDelay -= 50

        # Display level UI
        font = pygame.font.SysFont("Lucida Console", 34, bold=True)
        text = font.render(f"level:{self.level}", True, (0, 0, 0))
        textOutline = font.render(f"level:{self.level}", True, (255, 255, 255))
        window.blits([(textOutline, (1202, 50)), (textOutline, (1198, 50)), (textOutline, (1200, 48)), (textOutline, (1200, 52))])
        window.blit(text, (1200, 50))

    def cancleRow(self, bool):
        # Checks if player hits row
        if bool:
            self.randColor = (80,80,80)
            self.Cancled = True
            return True
        return False

    def checkCollision(self, p_Hitbox,p_ID):
        # Checks if player is inside hitbox and has the right shape
        if self.checkHitbox.colliderect(p_Hitbox) and self.rowId == p_ID and not self.Cancled and not self.invisible:
            self.invisible = True
            return True
        return False

    def restart(self,x,y):
        # Reset row settings on restart
        self.rowId = randint(0, 3)
        self.randColor = (randint(150, 255), randint(150, 255), randint(150, 255))  # creates random color
        self.x = -randrange(50, 1300, 50)
        self.y = y
        self.invisible = False
        self.Cancled = False
        self.levelTimer = 1
        self.level = 0
        self.moveDelay = 500