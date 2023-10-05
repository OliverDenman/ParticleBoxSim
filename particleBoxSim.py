import pygame, sys, random, math

class main:
    def __init__(self):

#------------ PYGAME SETUP ------------------------------

        pygame.init()
        pygame.display.set_caption("Particle Box Collision")
        self.windowSize = (1280,720) #Screen resolution
        self.gameWindow = pygame.display.set_mode((self.windowSize)) #set display to draw too
        self.clockObject = pygame.time.Clock() #set the clock for tick rate

#------------ GENERAL VARIABLES -------------------------

        self.particles = []
        self.particleCount = 0
        self.velocityMod = 2
        self.relSpeed = 1.0
        self.paused = False

        self.maxParticles = 256
        self.framerate = 120
        self.dispColour = (32,34,46) #Screen colour
        self.textColour = (250,250,250)

        self.UIBorderWidth = 300
        self.UIAlpha = 75
        self.UISurface = pygame.Surface((self.UIBorderWidth,self.windowSize[1]))
        self.fontMessage = pygame.font.SysFont("comicsansms", 25)
        self.fontStart = pygame.font.Font(None, 50)
        self.fontPaused = pygame.font.Font(None, 50)
        self.fontControls = pygame.font.SysFont("comicsansms", 20)
        self.fadeAlpha = 250
        self.fadeAmount = 5

        self.firstPressed = False
        self.renderFade = True

        self.colliderXBoundPos = self.windowSize[0]
        self.colliderXBoundNeg = 0
        self.colliderYBoundPos = self.windowSize[1]
        self.colliderYBoundNeg = 0

#------------ CREATE PARTICLES ---------------------------

    def createParticle(self):
        self.location = [ii for ii in pygame.mouse.get_pos()]
        self.direction = random.randint(0,360)
        self.XYDir = 2*[1]
        self.velocity = self.velocityMod
        self.radius = 10
        self.particles.append([self.location, self.direction, self.XYDir, self.radius, self.velocity])

#------------ DESTROY PARTICLES ---------------------------

    def destroyParticle(self, pos):
        del self.particles[pos-1]

#------------ CALC NEXT POSITION OF PARTICLE -------------

    def nextPos(self,particle):
        if self.paused == False:
            velocityCalc = particle[4] * self.relSpeed
            nextPosX = particle[0][0] + math.cos(particle[1]) * particle[2][0] * velocityCalc
            nextPosY = particle[0][1] + math.sin(particle[1]) * particle[2][1] * velocityCalc
            particle[2][0] *= -1 if (nextPosX > (self.colliderXBoundPos-particle[3]) or nextPosX < (self.colliderXBoundNeg+particle[3])) else 1
            particle[2][1] *= -1 if (nextPosY > (self.colliderYBoundPos-particle[3]) or nextPosY < (self.colliderYBoundNeg+particle[3])) else 1
            particle[0][0] += math.cos(particle[1]) * particle[2][0] * velocityCalc
            particle[0][1] += math.sin(particle[1]) * particle[2][1] * velocityCalc

#------------ USER INTERFACE -----------------------------

    def drawUI(self):
        particleCountMessage = self.fontMessage.render(f"Particles: {str(self.particleCount).zfill(3)}/{str(self.maxParticles).zfill(3)}", True, (250,250,250))
        self.gameWindow.blit(particleCountMessage, [15,15])

        veloctyMessage = self.fontMessage.render(f"Velocity: {str(self.velocityMod).zfill(3)}", True, self.textColour)
        self.gameWindow.blit(veloctyMessage, [15,65])

        fpsMessage = self.fontControls.render(f"FPS: {str(self.clockObject.get_fps())[0:5]}", True, self.textColour)
        self.gameWindow.blit(fpsMessage, [15,self.windowSize[1]-40])

        relSpeedMessage = self.fontMessage.render(f"Relative Speed: x{self.relSpeed}", True, self.textColour)
        self.gameWindow.blit(relSpeedMessage, [15,115])

        ControlsMessage = self.fontControls.render(f"Particles: UP/DOWN", True, self.textColour)
        self.gameWindow.blit(ControlsMessage, [15,self.windowSize[1]-165])

        ControlsMessage = self.fontControls.render(f"Velocity: LEFT/RIGHT", True, self.textColour)
        self.gameWindow.blit(ControlsMessage, [13,self.windowSize[1]-135])

        ControlsMessage = self.fontControls.render(f"Relative Speed: G/H", True, self.textColour)
        self.gameWindow.blit(ControlsMessage, [15,self.windowSize[1]-105])

        ControlsMessage = self.fontControls.render(f"Pause/Play: P", True, self.textColour)
        self.gameWindow.blit(ControlsMessage, [15,self.windowSize[1]-75])

        clickToStartMessage = self.fontStart.render(f"Hold  [Mouse Button One]  To Place Particles", True, self.textColour)

        pausedMessage = self.fontPaused.render("PAUSED", True, self.textColour)
        if self.paused == True:
            self.gameWindow.blit(pausedMessage, [self.windowSize[0]-170, self.windowSize[1]-50])

        if self.renderFade == True:
            self.gameWindow.blit(clickToStartMessage, [((self.windowSize[0]-self.UIBorderWidth)/2)-100, self.windowSize[1]/2])
        elif self.fadeAlpha < 1:
            self.renderFade = False
        if self.fadeAlpha > 1:
            if self.firstPressed == True:
                clickToStartMessage.set_alpha(self.fadeAlpha)
                self.fadeAlpha -= self.fadeAmount
                self.gameWindow.blit(clickToStartMessage, [((self.windowSize[0]-self.UIBorderWidth)/2)-100, self.windowSize[1]/2])

        self.UISurface.set_alpha(self.UIAlpha)
        self.gameWindow.blit(self.UISurface,(0,0))


#------------ MAIN RUN FUNCTION --------------------------

    def run(self):
        while True:

        #------------ EXIT THE GAME WHEN QUIT PRESSED ------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #get input
                    pygame.quit() #exit the pygame instance
                    exit() #use sys calls to exit

        #------------ INPUT -------------------------------------

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.paused = False
                        self.relSpeed = 1.0
                        self.firstPressed = False
                        self.renderFade = True
                        self.fadeAlpha = 250
                        self.particles = []
                        self.particleCount = len(self.particles)
                        self.maxParticles = 256
                        self.velocityMod = 2
                    if event.key == pygame.K_LEFT:
                        self.velocityMod -= 1 if self.velocityMod > 1 else 0
                    if event.key == pygame.K_RIGHT:
                        self.velocityMod += 1 if self.velocityMod < 5 else 0
                    if event.key == pygame.K_g:
                        self.relSpeed -= 0.5 if self.relSpeed > 0.5 else 0
                    if event.key == pygame.K_h:
                        self.relSpeed += 0.5 if self.relSpeed < 5 else 0
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     self.createParticle()

            key = pygame.key.get_pressed()

            if key[pygame.K_UP]:
                self.maxParticles += 1 if self.maxParticles < 10000 else 0
            if key[pygame.K_DOWN]:
                if self.maxParticles > 0:
                    if self.maxParticles == self.particleCount:
                        self.destroyParticle(self.maxParticles)
                        self.particleCount -= 1
                    self.maxParticles -= 1

        #------------ MAIN GAME LOOP -----------------------------

            if pygame.mouse.get_pressed()[0]:
                if self.particleCount < self.maxParticles and [ii for ii in pygame.mouse.get_pos()][0] > self.UIBorderWidth:
                    self.firstPressed = True
                    self.renderFade = False
                    self.createParticle()
                    self.particleCount += 1

            for particle in reversed(self.particles):
                self.nextPos(particle)
                pygame.draw.circle(self.gameWindow, (77,78,91), ((particle[0][0],particle[0][1])), particle[3])

            self.drawUI()

        #------------ UPDATE THE DISPLAY SURFACE FOR 120 FPS ------
            pygame.display.update() #update the display with the new buffer
            self.gameWindow.fill(self.dispColour) #change the colour of the display
            self.clockObject.tick(self.framerate) #Run at 60 fps

#------------ ROOT INSTANCE CHECK -----------------------

if __name__ == "__main__":
    main().run()
