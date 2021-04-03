"""
Pygame Hardware Hangman
"""
import pygame
import random
import math

pygame.init()

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
BLUE = (0, 120, 215)
GREEN = (0, 255, 0)

#fonts
titleFont = pygame.font.SysFont('comicsans', 85, True, False)
font = pygame.font.SysFont('comicsans', 45, True, False)
buttonFont = pygame.font.SysFont('comicsans', 25, True, False)

#Rectangle Value
rectY = 360

#Hangman Buttons
radius = 25
buttons = []
button_num = 0 
A = 65 
for i in range(13):
    x = 270 + i*60
    y = 350
    buttons.append([x, y, chr(A + i)])
for i in range(13):
    x = 270 + i*60
    y = 420
    buttons.append([x, y, chr(A + i + 13)])
print(buttons)
#game variable
ram = 4
flowers = 0 

#timer variable for failscreen
startTime = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000

#Questions and Words
questions_list = ["A circuit board that contains all principle components of the computer", 
"The brain of the computer, it's performance is measured in   Ghz", 
"A specialized processor used to accelerate the rendering of  graphics",
"A form of computer memory that stores temporary data",
"A hardware component that is used to supply power to the     computer",
"Short for malicious software, this word describes harmful    computer programs",
"This Operating System was created in 1985 by Microsoft",
"Released in 1984 by Apple, this computer was the first       successful PC that featured the GUI",
"This Operating System first released in 1991 runs on all     Android phones",
"The Operating System which macOS is based on was released in 1971"
]
words_list = ["MOTHERBOARD", "CPU", "GPU", "RAM", "PSU", "MALWARE", "WINDOWS", "MACINTOSH", "LINUX", "UNIX"]
question_number = 0
word_number = 0 
guessedLetters = []
winningCount = len(words_list)

#draw ram variables
ramX = 175
ramY = 630
#text
textOne = titleFont.render("Computer RAM Man", True, WHITE)
textTwo = font.render("Easy", True, WHITE)
textThree = font.render("Hard", True, WHITE)
textFour = font.render("Instructions", True, WHITE)
#global variable
clock = pygame.time.Clock()

#setting up the screen size
screenSize = (1280, 720)
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Hardware Hangman")

#Timer Variable

#background images
background = pygame.image.load("background1.png").convert()
backgroundTwo = pygame.image.load("Windows.jpg").convert()
backgroundThree = pygame.image.load("hardware.jpg").convert()
backgroundThree = pygame.transform.scale(backgroundThree, (1280, 720))
backgroundFour = pygame.image.load("background4.jpg").convert()
backgroundFour = pygame.transform.scale(backgroundFour, (1280,720))
# Game images
starImage = pygame.image.load("star.png").convert()
starImage = pygame.transform.scale(starImage, (80, 60))
starImage.set_colorkey(BLACK)

pcImage = pygame.image.load("PC.png").convert()
pcImage = pygame.transform.scale(pcImage, (300,300))
flowerImage = pygame.image.load("flower.png").convert()
flowerImage.set_colorkey((32,31,30))
menuImage = pygame.image.load("menu.jpg").convert()
menuImage = pygame.transform.scale(menuImage, (200,200))
gpuImage = pygame.image.load("GPU.png").convert()
gpuImage.set_colorkey((32,31,30))
gpuImage = pygame.transform.scale(gpuImage, (250, 370))
cpuImage = pygame.image.load("CPU.png").convert()
cpuImage.set_colorkey((32,31,30))
cpu = pygame.transform.scale(cpuImage, (200, 200))
homeImage = pygame.image.load("home.jpg").convert()
homeImage = pygame.transform.scale(homeImage, (110, 90))
homeImage.set_colorkey((254,254,254))
instructionsImage = pygame.image.load("instructions.jpg").convert()
instructionsImage = pygame.transform.scale(instructionsImage, (864, 486))
instructionsImage.set_colorkey((33,33,33))
chipMunkImage = pygame.image.load("chipmunk.png").convert()
chipMunkImage.set_colorkey((32,31,30))
spiderImage = pygame.image.load("spider.png").convert()
spiderImage.set_colorkey((32,31,30))
humanImage = pygame.image.load("human.png").convert()
humanImage.set_colorkey((32,31,30))
treeImage = pygame.image.load('tree.png').convert()
treeImage.set_colorkey((32,31,30))
class GameScene:
    def __init__(self):
        self.scene = "loading"

    # Menu Scene
    def loading(self):
        global ram
        global word_number
        global question_number
        global flowers
        global gussedLetters
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # detects if user presses easy or hard and places them in their desired difficulty
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                press_easy = mouse_x > 427 and mouse_x < 854 and mouse_y > 360 and mouse_y < 410
                press_hard = mouse_x > 427 and mouse_x < 854 and mouse_y > 450 and mouse_y < 500
                press_instructions = mouse_x > 427 and mouse_x < 854 and mouse_y > 540 and mouse_y < 590
                # If user presses instruction button then loads the instructions scene
                if press_instructions:
                    self.scene = "instructions"
                # If user presses hard button then gives the user 4 sticks of ram
                if press_easy:
                    self.scene = "maingame"
                    ram = 4
                    word_number = 0
                    question_number = 0
                    flowers = 0
                    guessedLetters = []
                    winningCount = len(words_list)
                # If user presses hard button then gives the user 2 sticks of ram
                if press_hard:
                    self.scene = "maingame"
                    ram = 2
                    word_number = 0
                    question_number = 0
                    flowers = 0
                    guessedLetters = []
                    winningCount = len(words_list)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.scene = "failscreen"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.scene = "victoryscreen"


        #draw background
        screen.blit(backgroundFour, (0, 0))
        
        #draw title, buttons, and button text
        screen.blit(textOne, (300, 125))

        for i in range(3):
            pygame.draw.rect(screen, GREY, (427, 360 + 90 * i, 427, 50))
            
        
        screen.blit(textTwo, (600, 373))
        screen.blit(textThree, (600, 463))
        screen.blit(textFour, (530, 553))
        
        pygame.display.flip()
    
    #instructions scene
    def instructions(self):
        
        # Draw instructions and game developer images
        screen.fill(BLACK)
        
        screen.blit(humanImage, (100, 325))
        screen.blit(chipMunkImage, (600, 325))
        screen.blit(instructionsImage, (200, -100))
        screen.blit(homeImage, (-5, 625))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > 5 and mouse_x < 95 and mouse_y > 624 and mouse_y < 710:
                    self.scene = "loading"
        
        pygame.display.flip()
    
    # Main Game Scene
    def maingame(self):

        #Use global variable
        global question_number
        global word_number
        global ram
        global flowers
        global guessedLetters
        global words_list
        global winningCount
        
        screen.fill(BLACK)
        

        # draw home button
        screen.blit(homeImage, (-5,625))

        #Draws the Questions
        if len(questions_list[question_number]) <= 60:
            question = font.render(questions_list[question_number], True, WHITE)
            screen.blit(question, (100, 110))
        if len(questions_list[question_number]) > 60 and len(questions_list[question_number]) < 81:
            quesLineOne = font.render(questions_list[question_number][:61], True, WHITE)
            quesLineTwo = font.render(questions_list[question_number][61:], True, WHITE)
            screen.blit(quesLineOne, (100, 110))
            screen.blit(quesLineTwo, (550, 140))
        if len(questions_list[question_number]) > 80:
            quesLineOne = font.render(questions_list[question_number][:61], True, WHITE)
            quesLineTwo = font.render(questions_list[question_number][61:], True, WHITE)
            screen.blit(quesLineOne, (100, 110))
            screen.blit(quesLineTwo, (300, 140))

        
        #Prints the word that user is trying to guess
        guessed_word = ""
        for letter in words_list[word_number]:
            if letter in guessedLetters:
                guessed_word += letter
            else:
                guessed_word += "_ "
            
        
        text = font.render(guessed_word ,True , WHITE)
        lengthWord = 3
       
        if len(words_list[word_number]) >= lengthWord:
            backWord = len(words_list[word_number]) - lengthWord
            screen.blit(text, (590 - backWord * 12, 250))


        #draw gpu and cpu ;)
        screen.blit(gpuImage, (0, 200))
        screen.blit(cpuImage, (1020, 260))
        

        #Draws the buttons
        for button in buttons:
            x, y, letter = button
            pygame.draw.circle(screen, WHITE, (x, y), radius, 5)
            buttonletter = buttonFont.render(letter, True, WHITE)
            screen.blit(buttonletter, [x-6,y-8])
        

        #Draws Questions left
        
        for x in range(10):
            pygame.draw.rect(screen, GREY, (185 + x*90, 0, 90, 75), 2)
            textQuestionNum = font.render(str(x+1), True, WHITE)
            screen.blit(textQuestionNum, (220 + x * 90, 10))
            pygame.draw.rect(screen, GREY, (185 + x*90, 65, 90, 10))
        
        # Draws progress bar on top of screen
        if word_number >= 1:
            for x in range(word_number):
                pygame.draw.rect(screen, BLACK, (185 + x*90, 0, 90, 65))
                pygame.draw.rect(screen, GREY, (185 + x*90, 0, 90, 75), 2)
                screen.blit(starImage, (190 + x*90, 0, 90, 75))
                pygame.draw.rect(screen, GREEN, (185 + x*90, 65, 90, 10))
        
        pygame.draw.rect(screen, BLUE, (185 + word_number*90, 65, 90, 10))

        #Moves on to next word if the word is guessed correctly
        if guessed_word == words_list[word_number]:
            question_number += 1
            word_number += 1
            winningCount -= 1
            guessedLetters = []
        
        #draw ram
        for i in range(ram):
            ramImage = pygame.image.load("ram.jpg").convert()
            ramImage = pygame.transform.scale(ramImage, (270, 100))
            ramImage.set_colorkey(WHITE)
            screen.blit(ramImage, (ramX + i * 225, ramY))

        #draw flowers
        for i in range(flowers):
            screen.blit(flowerImage, (800 - i * 225, 450))
            
            
        #If the user loses all his ram, changes to fail screen 
        if ram == 0:
            self.scene = "failscreen"
        
        #If the user guesses all the words correctly, changes to victory screen
        if winningCount == 0:
            self.scene = "victoryscreen"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > 5 and mouse_x < 95 and mouse_y > 624 and mouse_y < 710:
                    self.scene = "loading"
        
                # Uses the distance formula to determine if their cursor is on the button and if pressed adds letter to guessed
                for button in buttons:
                    x, y, letter = button
                    distanceFromButton = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                    if distanceFromButton < radius:
                        guessedLetters.append(letter)
                        if letter not in words_list[word_number]:
                            ram -= 1
                            flowers += 1
            

            # Developer Access
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_o:
                    word_number -= 1
                    question_number -= 1
                if event.key == pygame.K_p:
                    word_number += 1
                    question_number += 1
                 

            # Developer Access
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.scene = "failscreen"
        
        pygame.display.flip()

    # failscreen scene
    def failscreen(self):
        #use these global varibles 
        global startTime
        global word_number
        global question_number
        global flowers
        global guessedLetters
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #detects button press and starts a stopwatch
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > 126 and mouse_x < 376 and mouse_y > 377 and mouse_y < 437:
                    startTime = pygame.time.get_ticks()
                    

        
        # background image
        failImage = pygame.image.load("failscreen.jpg").convert()
        screen.blit(failImage, (0, 0))
        
        # Restart Button
        pygame.draw.rect(screen, BLUE, (125, 376, 250, 60))
        text = font.render("Press to Restart", True, WHITE)
        screen.blit (text, (140, 410))

        #Timer 
        percentage = 0
        counter = 10

        secondsPassed = (pygame.time.get_ticks() - startTime) / 1000
        percentage += secondsPassed * 10 // 1
        counter -= secondsPassed

        # prints the percentage of the restart process
        textPercentage = font.render((str(percentage) + "% complete"), True, WHITE)
        if percentage > 0 and percentage < 101: 
            pygame.draw.rect(screen, BLUE, (125, 376, 300, 60))
            screen.blit(textPercentage, (140, 410))
        
        # once 10 seconds has passed after pressing "restart", returns to loading screen
        if counter < 0 and counter > -1:
            self.scene = "loading"

        
        pygame.display.flip()

    #victory screen
    def victoryscreen(self):
        global word_number
        global question_number
        global winningCount
        global flowers

        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Go back to titlescreen
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                pressAgain = mouse_x > 74 and mouse_x < 426 and mouse_y > 599 and mouse_y < 651
                pressExit = mouse_x > 849 and mouse_x < 1201 and mouse_y > 599 and mouse_y < 651
                if pressAgain:
                    self.scene = "loading"
                   

                if pressExit:
                    pygame.quit()

        #draw tree
        screen.blit(treeImage, (160, 100))
        
        #draw text "You won 10 times"
        victoryText = titleFont.render("You WON!", True, WHITE)
        for i in range(5):
            screen.blit(victoryText, (80, 120 + i * 100))
        for i in range(5):
            screen.blit(victoryText, (875, 120 + i * 100))
        
        # draw buttons and button text
        pygame.draw.rect(screen, GREY, (75, 600, 350, 50))
        pygame.draw.rect(screen, GREY, (850, 600, 350, 50))
        playAgain = font.render("Play Again", True, BLACK)
        exitText = font.render("Exit", True, BLACK)
        screen.blit(playAgain, (150, 610))
        screen.blit(exitText, (985, 610))

        pygame.display.flip()
    

    # class method for updating game scene
    def update(self): 
        if self.scene == "loading":
            self.loading()
        if self.scene == "instructions":
            self.instructions()
        if self.scene == "maingame":
            self.maingame()
        if self.scene == "failscreen":
            self.failscreen()
        if self.scene == "victoryscreen":
            self.victoryscreen()
        
game_scene = GameScene()

#timer variable

while True:
    #developer access
    game_scene.update()
    clock.tick(60)
    
        
            
        
        
            


         