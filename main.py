import pygame, sys
from pygame.locals import *

from player import Player
from row import Row

playerStep = 50  # Player move every 50 pixels
x = 1400
y = 900

pink = (251,198,207)
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = x, y
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('TetriFlip')
clock = pygame.time.Clock()

# Initialize game objects
player = Player(x, y, playerStep)
row1 = Row(x, y)
row2 = Row(x, y+600)
row3 = Row(x, y+1200)

score = 0
lives = 3

# Fonts for UI elements
font = pygame.font.SysFont("Lucida Console", 34, bold=True)
pauseFont = pygame.font.SysFont("Lucida Console", 120, bold=True)

# Load images and scale to screen
background = pygame.transform.scale(pygame.image.load('assets\\background.jpg'),(1400,900))
endScreen = pygame.transform.scale(pygame.image.load('assets\\ENDSC.jpg'),(1400,900))
StartScreen = pygame.transform.scale(pygame.image.load('assets\\startSC.jpg'),(1400,900))
rainbow = pygame.transform.scale(pygame.image.load('assets\\rainbow_fade.jpg'),(2800,900))
quitButton = pygame.transform.scale(pygame.image.load('assets\\quitb.jpg'),(200,100))
restartButton = pygame.transform.scale(pygame.image.load('assets\\restartb.jpg'),(200,100))

start = False
musicPlaying = True
playQuitSound = True
playRestartSound = True
pressESC = False
xFade = 0

# Load sounds
pygame.mixer.music.load('assets\\sound\\background music.wav')
hitSound = pygame.mixer.Sound('assets\\sound\\hit.wav')
deathSound = pygame.mixer.Sound('assets\\sound\\death.wav')
completeRowSound = pygame.mixer.Sound('assets\\sound\\wall.wav')
quitSound = pygame.mixer.Sound('assets\\sound\\quit.mp3')
restartSound = pygame.mixer.Sound('assets\\sound\\restart.wav')

# Initialize sound channels
hitSoundChannel = hitSound.play()
hitSound.stop()

# Start screen loop
while not start:
    window.blit(rainbow,(xFade,0))
    xFade -= 7
    if xFade == -1400:
        xFade = 0
    window.blit(StartScreen,(0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pygame.mixer.music.play(-1, 0.0)
            start = True
    pygame.display.update()

# Main game loop
while True:
    if lives >=0:
        clock.tick(60)  # 60 FPS
        window.blit(background,(0,0))
        key = pygame.key.get_pressed()
        player.controls(key,x,y)    # Movement
        player.draw(window)         # Draw player

        # Spawn rows
        row1.spawn(window)
        row2.spawn(window)
        row3.spawn(window)

        # Player scores if correct shape overlaps the check hitbox
        if row1.checkCollision(player.hitbox[0],player.id) or row2.checkCollision(player.hitbox[0],player.id) or row3.checkCollision(player.hitbox[0],player.id):
            score += 100
            completeRowSound.play()

        # Player loses life if colliding with row
        if row1.cancleRow(player.playerCollision(row1.hitbox)) or row2.cancleRow(player.playerCollision(row2.hitbox)) or row3.cancleRow(player.playerCollision(row3.hitbox)):
            lives -= 1
            if lives >=0:
                hitSoundChannel = hitSound.play()
            else:
                deathSound.play()
                pygame.mixer.music.stop()

        # Render UI text with outline
        text = font.render(f"lives:{lives}  score:{score}", True, (0, 0, 0))
        textOutline = font.render(f"lives:{lives}  score:{score}", True, (255, 255, 255))
        window.blits([(textOutline, (52, 50)),(textOutline, (48, 50)),(textOutline, (50, 48)),(textOutline, (50, 52))])
        window.blit(text, (50, 50))

        pygame.display.update()

        for event in pygame.event.get():
            player.transform(key,event)     # Pass the event type to the function in order to avoid checking the event type twice
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m: # Press m to toggle mute
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                musicPlaying = not musicPlaying

                # Pause menu
                if event.key == pygame.K_ESCAPE:
                    pressESC = False
                    pauseText = pauseFont.render("PAUSED",True,(0,0,0))
                    pauseTextOutline = pauseFont.render("PAUSED", True, (255, 255, 255))
                    overlay = pygame.Surface((1400, 900), pygame.SRCALPHA) # Creates overlay surface for the pause menu
                    overlay.fill((0, 0, 0, 100))    # Transparent dark overlay
                    window.blit(overlay, (0, 0))
                    window.blits([(pauseTextOutline, (497, 150)), (pauseTextOutline, (493, 150)), (pauseTextOutline, (495, 148)),(pauseTextOutline, (495, 152))])
                    window.blit(pauseText, (495, 150))
                    pygame.mixer.music.pause()
                    hitSoundChannel.pause()
                    pygame.display.update()
                    pauseStartTime = pygame.time.get_ticks()
                    while not pressESC:
                        for pauseEvent in pygame.event.get():
                            if pauseEvent.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif pauseEvent.type == pygame.KEYDOWN:
                                if pauseEvent.key == pygame.K_ESCAPE:
                                    pygame.mixer.music.unpause()
                                    player.pauseInvicibleUpdate(pygame.time.get_ticks()-pauseStartTime)
                                    hitSoundChannel.unpause()
                                    pressESC = True

    # End screen
    else:
        window.blit(endScreen, (0, 0))
        window.blit(quitButton,(300,650))
        window.blit(restartButton,(900,650))
        quitHitbox = pygame.Rect(300,650,200,100)
        restartHitbox = pygame.Rect(900,650,200,100)

        # Render "Final Score" text
        text = font.render("Final Score", True, (0, 0, 0))
        textOutline = font.render("Final Score", True, (255, 255, 255))

        # Render score number
        scoreText = font.render(f"{score}", True, (0, 0, 0))
        scoreTextOutline = font.render(f"{score}", True, (255, 255, 255))
        scoreRect = scoreText.get_rect(center=(700,725))    # Getting the center of the score

        # Printing score with outline
        window.blits([(scoreTextOutline, (scoreRect[0]+2, scoreRect[1])),(scoreTextOutline, (scoreRect[0]-2, scoreRect[1])),(scoreTextOutline, (scoreRect[0], scoreRect[1]+2)),(scoreTextOutline, (scoreRect[0], scoreRect[1]-2))])
        window.blit(scoreText, scoreRect)
        window.blits([(textOutline, (597, 660)),(textOutline, (593, 660)),(textOutline, (595, 658)),(textOutline, (595, 662))])
        window.blit(text, (595, 660))

        # Handle hover + click effects
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if quitHitbox.collidepoint(event.pos):
                    quitButton.fill((255,0,0,150), special_flags=pygame.BLEND_RGBA_MULT)
                    if playQuitSound:
                        playQuitSound = False
                        quitSound.play()
                else:
                    quitButton = pygame.transform.scale(pygame.image.load('assets\\quitb.jpg'), (200, 100))
                    quitSound.stop()
                    playQuitSound = True

                if restartHitbox.collidepoint(event.pos):
                    restartButton.fill((0, 255, 0, 150), special_flags=pygame.BLEND_RGBA_MULT)
                    if playRestartSound:
                        playRestartSound = False
                        restartSound.play(loops=-1)
                else:
                    restartButton = pygame.transform.scale(pygame.image.load('assets\\restartb.jpg'), (200, 100))
                    restartSound.stop()
                    playRestartSound = True

            # Check mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quitHitbox.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if restartHitbox.collidepoint(event.pos): # Restart game
                    lives = 3
                    score = 0
                    restartSound.stop()
                    playRestartSound = True
                    player.restart(x,y,playerStep)
                    row1.restart(x,y)
                    row2.restart(x,y+600)
                    row3.restart(x,y+1200)
                    pygame.mixer.music.play(-1, 0.0)

        pygame.display.update()
