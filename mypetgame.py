import pygame
import os
import random

pygame.init()


WIDTH, HEIGHT = 900, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pet Game")

x = 50
y = 305
vel = 10
vel_y = 10
move_left = False
move_right = False
stepIndex = 0

jump = False
i = 0

#load doghouse
house = pygame.image.load('DogH.png')

#load bg
bg_img = pygame.image.load('fallbackground.jpg')
bg = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))

# Load dog images
stand_img = pygame.image.load(os.path.join('Dog stand.png'))
stand = pygame.transform.scale(stand_img, (100,90))

right_img = [pygame.image.load(os.path.join('Dog run1.png')),
         pygame.image.load(os.path.join('Dog run2.png')),
         pygame.image.load(os.path.join('Dog run3.png')),
         pygame.image.load(os.path.join('Dog run 4.png'))
         ]

# Scale each image individually
right = [pygame.transform.scale(img, (100,90)) for img in right_img]

left_img = [pygame.image.load(os.path.join('Dog run1L.png')),
        pygame.image.load(os.path.join('Dog run2L.png')),
        pygame.image.load(os.path.join('Dog run3L.png')),
        pygame.image.load(os.path.join('Dog run 4L.png'))
        ]
# Scale each image individually
left = [pygame.transform.scale(img, (100, 90)) for img in left_img]

#Load lava images
lava_img = [pygame.image.load(os.path.join('lava1.png')),
            pygame.image.load(os.path.join('lava2.png')),
            pygame.image.load(os.path.join('lava3.png')),
            ]
#Scale
lava = [pygame.transform.scale(img, (80,70)) for img in lava_img]

class Dog:
    def __init__(self, x, y):
        # walk
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 10
        #direction dog is facing
        self.direc_right = False
        self.direc_left = False
        self.stepIndex = 0
        self.jump = False
        #Health
        self.hitbox = (self.x, self.y, 80, 80)
        self.health = 10
        self.lives = 3
        self.alive = True


#movement
    def move_dog(self, userInput):
        # move right when press D
        if userInput[pygame.K_d] and self.x <= WIDTH - 95: #-95 is offsett so that char does not go off screen
            self.x += self.velx
            self.direc_right = True
            self.direc_left = False

        elif userInput[pygame.K_a] and self.x >= 0: #move left when press A
            self.x -= self.velx
            self.direc_right = False
            self.direc_left = True
        else:
            self.direc_right = False
            self.direc_left = False
            self.stepIndex = 0  #when pressed it starts from the first image

        if self.jump is False and userInput[pygame.K_SPACE]:
                self.jump = True
        if self.jump is True:
            self.y -= self.vely*3
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10

#draw dog on window
    def draw(self,win):
        self.hitbox = (self.x + 15, self.y + 20, 75, 60) # coordinates + w and h of hitbox
        # pygame.draw.rect(win, (0,0,0),self.hitbox,1) #rectangle for hitbox
        if self.stepIndex >= 16:
            self.stepIndex = 0 #resets/ go backs to the first pic
        if self.direc_left:
            win.blit(left[self.stepIndex//4], (self.x,self.y)) #for smoother fps
            self.stepIndex += 1

        elif self.direc_right:
            win.blit(right[self.stepIndex//4], (self.x,self.y))
            self.stepIndex += 1

        else:
            win.blit(stand,(self.x,self.y))


    # def hit(self):
    #     for mob in mobs:
    #         if player.hitbox[0] < mob.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < mob.y + 32 < \
    #                 player.hitbox[1] + player.hitbox[3]:
    #             print("  player hit lava ")


class Mobs:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.lava = False
        self.stepIndex = 0
        # Health
        self.hitbox = (self.x, self.y, 80, 80)
        # self.health = 30

    def step(self):
        if self.stepIndex >= 27:
            self.stepIndex = 0
    def draw_lava(self,win):
        self.step()
        win.blit(lava[self.stepIndex//9],(self.x,self.y))
        self.stepIndex += 1
        self.hitbox = (self.x -5, self.y + 15, 90, 45)  # coordinates + w and h of hitbox
        # pygame.draw.rect(win, (0, 0, 0), self.hitbox, 1) #hitbox both in init and draw method to update hitbox as dog is moving

    def mob_move(self):
        self.hit()
        self.x -= speed #speed of the mob

    def hit(self):
        #check when the player hit box reaches the same cordinates as the mob hitbox
        if player.hitbox[0] < mob.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < mob.y + 32 < player.hitbox[1] + player.hitbox[3]:
            print(" lava hit player ")
            if player.health > 0:
                player.health -= 1
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 10
                elif player.health == 0 and player.lives == 0:
                    player.alive = False



    def off_screen(self):
        return  not(self.x >= -70 and self.x <= WIDTH)





#draw images on window
def draw_game():
    win.fill((0, 0, 0))
    win.blit(bg,(0,0)) #draw background

    #draw player
    player.draw(win)

    #draw mobs
    for mob in mobs:
        mob.draw_lava(win)

    #player health
    if player.alive == False:
        win.fill((0,0,0)) #screen goes dark when player dies
        font = pygame.font.Font('FreeSansBold-Rdmo.otf',32)
        text = font.render('You Died! Press R to restart', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (WIDTH//2, HEIGHT//2)
        win.blit(text, textRect)
        if userInput[pygame.K_r]: #pressing R restarts games
            player.alive = True
            player.lives = 3
            player.health = 10
    #player live counter
    font = pygame.font.Font('FreeSansBold-Rdmo.otf',32)
    text = font.render('Hearts:' + str(player.lives), True, (0,0,0))
    win.blit(text, (750, 20))

    pygame.time.delay(30)
    pygame.display.update()


#Instance of Dog class
player = Dog(50,305)

#Instance of mob class
mobs = []
speed = 3

#Main Loop
run = True
while run:

    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Input
    userInput = pygame.key.get_pressed()

    #movement
    player.move_dog(userInput)

    # Spawn lava randomly only at the far right of the screen
    if random.randint(0, 200) < 2:  # Adjust the probability as needed
        lava_x = random.randint(WIDTH - 300, WIDTH - 150)  # Adjust size of lava image
        lava_y = random.randint(0, 305)  # Adjust size of lava image
        new_lava = Mobs(lava_x, lava_y, speed)
        mobs.append(new_lava)

    #Mobs
    if len(mobs) == 0:
        mob = Mobs(700,330, speed)
        mobs.append(mob)
        if speed <= 10:
            speed += 1
    for mob in mobs:
        mob.mob_move()
        if mob.off_screen():
            mobs.remove(mob)


    #draw game in window
    draw_game()

    # #Background loop
    # win.blit(bg, (i,0))
    # win.blit(bg, (WIDTH + i, 0))
    #
    # if i <= -WIDTH:
    #     i = 0
    # i -= 1
    # pygame.time.delay(30)
    # pygame.display.update()



    #Movement
    # userInput = pygame.key.get_pressed()
    #
    # if userInput[pygame.K_a]:
    #     x -= vel
    #     move_left = True
    #     move_right = False
    #
    # elif userInput[pygame.K_d]:
    #     x += vel
    #     move_left = False
    #     move_right = True
    #
    # else:
    #     move_right = False
    #     move_left = False
    #     stepIndex = 0



    # if jump is False and userInput[pygame.K_SPACE]:
    #     jump = True
    #     if jump is True:
    #         #y -= vel_y*4
    #         vel_y -= 1
    #         if vel_y < -10:
    #             jump = False
    #             vel_y = 10
    #
    # #background loop
    # win.blit(bg, (i, 0))
    # win.blit(bg, (WIDTH+i,0))
    #
    # if i == -WIDTH:
    #     win.blit(bg,(WIDTH+i,0))
    #     i = 0
    #
    # i -= 1

  #draw dog
    # global stepIndex
    # if stepIndex >= 16:
    #     stepIndex = 0
    # if move_left:
    #     win.blit(left[stepIndex//4],(x,y))
    #     stepIndex += 1
    # elif move_right:
    #     win.blit(right[stepIndex//4],(x,y))
    #     stepIndex += 1
    # else:
    #     win.blit(stand,(x,y))

    #fix