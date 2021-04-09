"""
-------------------------------------------------------------------------------
Name:   Computer Ram Man.py
Purpose:  A spin-off of Hangman in Pygame, with each wrong letter-guess resulting in a loss of one ram stick. 
Words to be guessed will all be course-related and will have an accompanying description for the player.
 
Author: Ge.G
 
Created:  04.04.2021
------------------------------------------------------------------------------
"""
# Import libraries
import pygame
import math

pygame.init()

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
BLUE = (0, 120, 215)
GREEN = (0, 255, 0)

#Define fonts
titleFont = pygame.font.SysFont('comicsans', 85, True, False)
font = pygame.font.SysFont('comicsans', 45, True, False)
buttonFont = pygame.font.SysFont('comicsans', 25, True, False)

# Create variables for Hangman keyboard Buttons (maingame)
radius = 25
buttons = []
A = 65 
for i in range(13):
    x = 270 + i*60
    y = 350
    buttons.append([x, y, chr(A + i)])
for i in range(13):
    x = 270 + i*60
    y = 420
    buttons.append([x, y, chr(A + i + 13)])

# game variables controlling amount of RAM/lives player has (maingame)
ram = 0
flowers = 0 
difficulty = "normal"

#timer variable for failscreen
startTime = 100000000000000000000000000000000000000000000

#Questions and Words lists and variables to display the questions and answers to the player
questions_list = ["A circuit board that contains all principle components of the computer", 
"The brain of the computer, it's performance is measured in   Ghz", 
"A  processor used to accelerate the rendering of graphics",
"A form of computer memory that stores temporary data",
"A hardware component that is used to supply power to the     computer",
"Short for malicious software, this word describes harmful    software ",
"This Operating System was created in 1985 by Microsoft",
"Released in 1984 by Apple, this computer was the first       successful PC that featured the GUI",
"This Operating System first released in 1991, is the basis   for all Android phones",
"The Operating System which macOS is based on was released in 1971",
"A type of malware that blocks access from user data until    money is paid to the hacker",
"A type of malware that displays unwanted advertisements      on your computer",
"An operating system that runs on all Apple Iphones",
"The measurement defined as 1024 gigabytes",
"The basic unit of measurement for computer storage",
"The basic unit of measurement for CPU speed",
"The monitor resolution that is 1920 x 1080 pixels",
"A spreadsheet software that is part of the Microsoft Office  Suite",
"A video editing software that is part of the Adobe Creative  Suite",
"A long-term computer storage drive that is much faster than  the standard hard drive",
"A type of virus that spies and tracks your online activity,  it may access your camera",
"A type of virus that records the keystrokes that the user    inputs into the computer",
"An operating system built by Google that is designed to      primarily run web applications",
"A music/media player developed by Apple that is used         across their devices", " "
]
words_list = ["MOTHERBOARD", "CPU", "GPU", "RAM", "PSU", "MALWARE", "WINDOWS", "MACINTOSH", "LINUX", "UNIX", "RANSOMWARE", "ADWARE", "IOS", "TERABYTE", 
"BYTE", "HERTZ", "HD", "EXCEL", "PREMIERE", "SSD", "SPYWARE", "KEYLOGGER", "CHROMEOS", "ITUNES", " "]

# Variables for the question and associated word answer the player is currently on, by default set to first question
question_number = 0
word_number = 0 

# list Variable for letters the player has guessed, by default empty 
guessedLetters = []

# variable for determining if the user has won, each time the player answers a qusetion correctly
winningCount = len(questions_list)

# text data for loading page 
textOne = titleFont.render("Computer RAM Man", True, WHITE)
textTwo = font.render("Easy", True, WHITE)
textThree = font.render("Hard", True, WHITE)
textFour = font.render("Instructions", True, WHITE)

#setting up the screen size, program caption, and clock
screenSize = (1280, 720)
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Computer RAM Man")
clock = pygame.time.Clock()

#background image for loading page/scene
backgroundFour = pygame.image.load("background4.jpg").convert()
backgroundFour = pygame.transform.scale(backgroundFour, (1280,720))

# images for loading page/scene
starImage = pygame.image.load("star.png").convert()
starImage = pygame.transform.scale(starImage, (80, 60))
starImage.set_colorkey(BLACK)
flowerImage = pygame.image.load("flower.png").convert()
flowerImage.set_colorkey((32,31,30))
gpuImage = pygame.image.load("GPU.png").convert()
gpuImage.set_colorkey((32,31,30))
gpuImage = pygame.transform.scale(gpuImage, (250, 370))
cpuImage = pygame.image.load("CPU.png").convert()
cpuImage.set_colorkey((32,31,30))
cpu = pygame.transform.scale(cpuImage, (200, 200))
instructionsImage = pygame.image.load("instructions.jpg").convert()
instructionsImage = pygame.transform.scale(instructionsImage, (864, 486))
instructionsImage.set_colorkey((33,33,33))

# home button image located in various scenes
homeImage = pygame.image.load("home.jpg").convert()
homeImage = pygame.transform.scale(homeImage, (110, 90))
homeImage.set_colorkey((254,254,254))

# images for instructions page/scene
chipMunkImage = pygame.image.load("chipmunk.png").convert()
chipMunkImage.set_colorkey((32,31,30))
humanImage = pygame.image.load("human.png").convert()
humanImage.set_colorkey((32,31,30))
willowImage = pygame.image.load('willow.png').convert()
willowImage.set_colorkey((4,16,15))
willowImage = pygame.transform.scale(willowImage, (295, 398))
tentImage = pygame.image.load('tent.png').convert()
tentImage.set_colorkey((4,16,15))
tentImage = pygame.transform.scale(tentImage, (375, 290))
chipmunkTentImage = pygame.image.load('chipmunktent.png').convert()
chipmunkTentImage.set_colorkey((4,16,15))
chipmunkTentImage = pygame.transform.scale(chipmunkTentImage, (75, 85))
afterwordImage = pygame.image.load("afterword.jpg").convert()
afterwordImage.set_colorkey((33,33,33))

# class called gamescene which has multiple methods containing code that runs the entire game
class GameScene:
    
    # def an attribute for this class called scene, which by default is set to "loading", this attribute is used to run the associated scene using a method later on 
    def __init__(self):
        self.scene = "loading"

    # Menu/loading Scene
    def loading(self):
        # use global variables
        global ram
        global word_number
        global question_number
        global flowers
        global guessedLetters
        global difficulty
        global winningCount
        
        # allows user to quite 
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

                # If user presses hard button then gives the user 4 sticks of ram, and resets all game variables
                if press_easy:
                    self.scene = "maingame"
                    ram = 4
                    word_number = 0
                    question_number = 0
                    flowers = 0
                    guessedLetters = []
                    winningCount = 24
                    difficulty = "easy"

                # If user presses hard button then gives the user 2 sticks of ram, and resets all game variables
                if press_hard:
                    self.scene = "maingame"
                    ram = 2
                    word_number = 0
                    question_number = 0
                    flowers = 0
                    guessedLetters = []
                    winningCount = 24
                    difficulty = "hard"

            # developer access to different scenes
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
        
        # Load images
        pygame.display.flip()
    
    #instructions scene
    def instructions(self):
        
        # Draw instructions, game developer and homebutton images
        screen.fill(BLACK)
        screen.blit(humanImage, (100, 325))
        screen.blit(chipMunkImage, (600, 325))
        screen.blit(instructionsImage, (200, -100))
        screen.blit(homeImage, (-5, 625))
        
        # allows user to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # allows user to return to loadingscreen by pressing home button 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > 5 and mouse_x < 95 and mouse_y > 624 and mouse_y < 710:
                    self.scene = "loading"
        
        # load images
        pygame.display.flip()
    
    # Main Game Scene
    def maingame(self):

        #Use global variables
        global question_number
        global word_number
        global ram
        global flowers
        global guessedLetters
        global words_list
        global winningCount
        global difficulty 
        
        # make background black
        screen.fill(BLACK)
        
        # draw home button
        screen.blit(homeImage, (-5,625))

        #Draws the Questions, splitting the question into 2 lines if the length is too long 
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
        
        #prints onto the screen the word that user is trying to guess, and the letters they have guessed 
        guessed_word = ""
        for letter in words_list[word_number]:
            if letter in guessedLetters:
                guessed_word += letter
            else:
                guessed_word += "_ "
            
        guessedText = font.render(guessed_word ,True , WHITE)
        lengthWord = 2
       
        # determines where on the screen to print the answer word depending on its length 
        if len(words_list[word_number]) >= lengthWord:
            backSpaceWord = len(words_list[word_number]) - lengthWord
            screen.blit(guessedText, (590 - backSpaceWord * 12, 250))

        # Draws images of a gpu and cpu 
        screen.blit(gpuImage, (0, 200))
        screen.blit(cpuImage, (1020, 260))
        
        #Draws the keyboard buttons, using a for loop and the data that we have previously stored in the list buttons 
        for button in buttons:
            x, y, letter = button
            pygame.draw.circle(screen, WHITE, (x, y), radius, 5)
            buttonletter = buttonFont.render(letter, True, WHITE)
            screen.blit(buttonletter, [x-6,y-8])
        
        # Draws progress bar on top of screen showing user progress across all 24 buttons

        # draws the first 12 questions
        if question_number < 13:
            for x in range(12):
                pygame.draw.rect(screen, GREY, (110 + x*90, 0, 90, 75), 2)
                textQuestionNum = font.render(str(x+1), True, WHITE)
                screen.blit(textQuestionNum, (145 + x * 90, 10))
                pygame.draw.rect(screen, GREY, (110 + x*90, 65, 90, 10))
        
        # draws the last 12 questions
        if question_number > 12:
            for x in range(12):
                pygame.draw.rect(screen, GREY, (110 + x*90, 0, 90, 75), 2)
                textQuestionNum = font.render(str(x+13), True, WHITE)
                screen.blit(textQuestionNum, (145 + x*90, 10))
                pygame.draw.rect(screen, GREY, (110 + x*90, 65, 90, 10))
        
        # draws stars for completed questions from  1 to 12
        if question_number >= 1 and question_number < 13:
            for x in range(question_number):
                pygame.draw.rect(screen, BLACK, (110 + x*90, 0, 90, 75))
                screen.blit(starImage, (113 + x*90, 0, 90, 75))
                pygame.draw.rect(screen, GREEN, (110 + x * 90, 65, 90, 10))
      
        # draws stars for completed questions from 13 to 24
        if question_number > 12:
            for x in range(question_number-12):
                pygame.draw.rect(screen, BLACK, (110 + x*90, 0, 90, 75))
                screen.blit(starImage, (113 + x*90, 0, 90, 75))
                pygame.draw.rect(screen, GREEN, (110 + x*90, 65, 90, 10))

        # draws a blue rectangle signifying the current question the player is on
        if question_number < 12:
            pygame.draw.rect(screen, BLUE, (110 + question_number*90, 65, 90, 10))
        if question_number > 12:
            pygame.draw.rect(screen, BLUE, (110 + (question_number-12)*90, 65, 90, 10))


        #Moves on to next question and word answer if the word is guessed correctly
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
            screen.blit(ramImage, (175 + i * 225, 630))

        #draw flowers if the player loses RAM
        if difficulty == "easy": 
            for i in range(flowers):
                screen.blit(flowerImage, (800 - i * 225, 450))
        if difficulty == "hard":
            for i in range(flowers):
                screen.blit(flowerImage, (350 - i * 225, 450))

        # draws "guess word" button
        guessWordText = font.render("Guess Word", True, WHITE)
        pygame.draw.rect(screen, GREY, (480, 185, 300, 40))
        screen.blit(guessWordText, (520, 190))

        #If the user loses all his ram, changes to fail screen 
        if ram == 0:
            self.scene = "failscreen"
        
        # detects if the user has answered all questions, and if they have, enters the vicotry screen
        if winningCount == 0:
            self.scene = "victoryscreen"
        
        # allows user to quit 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # detects mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # if user presses on home button, goes back to loading screen 
                if mouse_x > 5 and mouse_x < 95 and mouse_y > 624 and mouse_y < 710:
                    self.scene = "loading"
        
                # Uses the distance formula to determine if the player has clicked on keyboard button, and appends the guessed letter to the list guessed letters
                for button in buttons:
                    x, y, letter = button
                    distanceFromButton = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                    if distanceFromButton < radius:
                        guessedLetters.append(letter)

                        # if guessed letter is not in the word, removes one life/RAM from the player and adds a flower
                        if letter not in words_list[word_number]:
                            ram -= 1
                            flowers += 1
                
                # Detects if the user presses the "guessword" button, and if they have allows them to enter their full word guess into the terminal
                if mouse_x < 780 and mouse_x > 480 and mouse_y > 185 and mouse_y < 225:
                    fullGuess = input("Enter the full word you are guessing: ")
                    fullGuess = fullGuess.upper()
                    lettersFullGuess = ""

                    # if full word guess is wrong, player is sent to failscreen
                    if fullGuess != words_list[word_number]:
                        self.scene = 'failscreen'
                    if len(fullGuess) < len(words_list[word_number]) or len(fullGuess) > len(words_list[word_number]):
                        self.scene = 'failscreen'

                    # appends the users guess into the guessed letters list 
                    for i in range(len(fullGuess)):
                        lettersFullGuess = fullGuess[i]
                        guessedLetters.append(lettersFullGuess)
                        
            # Developer Access
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_o:
                    word_number -= 1
                    question_number -= 1
                if event.key == pygame.K_p:
                    word_number += 1
                    question_number += 1
                    winningCount -= 1
            
            # Developer Access
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.scene = "failscreen"
        
        pygame.display.flip()

    # failscreen scene
    def failscreen(self):

        #use these global variables 
        global startTime
        
        # Allows user to quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #detects button press and stores the current time 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > 126 and mouse_x < 376 and mouse_y > 377 and mouse_y < 437:
                    startTime = pygame.time.get_ticks()
                    
        # background image
        failImage = pygame.image.load("failscreen.jpg").convert()
        screen.blit(failImage, (0, 0))
        
        # Restart Button image
        pygame.draw.rect(screen, BLUE, (125, 376, 250, 60))
        text = font.render("Press to Restart", True, WHITE)
        screen.blit (text, (140, 410))

        # calculates the seconds passed since the user has pressed the restart button 
        counter = 10
        secondsPassed = (pygame.time.get_ticks() - startTime) / 1000
        counter -= secondsPassed

        # prints the percentage of the restart process
        percentage = 0
        percentage += secondsPassed * 10 // 1
        textPercentage = font.render((str(percentage) + "% complete"), True, WHITE)
        if percentage > 0 and percentage < 101: 
            pygame.draw.rect(screen, BLUE, (125, 376, 300, 60))
            screen.blit(textPercentage, (140, 410))
        
        # once 10 seconds has passed after pressing "restart", returns to loading screen
        if counter < 0 and counter > -1:
            self.scene = "loading"

        # Loads everything onto screen 
        pygame.display.flip()

    #victory screen scene 
    def victoryscreen(self):
        
        # fills background with black 
        screen.fill(BLACK)
        
        # allows user to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # Go back to titlescreen or quit game depending on which button the user presses 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                pressAgain = mouse_x > 74 and mouse_x < 426 and mouse_y > 599 and mouse_y < 651
                pressExit = mouse_x > 849 and mouse_x < 1201 and mouse_y > 599 and mouse_y < 651
                if pressAgain:
                    self.scene = "loading"
                if pressExit:
                    pygame.quit()

        #draw developer message, trees, tent and chipmunk
        screen.blit(chipmunkTentImage, (637, 585))
        screen.blit(tentImage, (450, 450))
        screen.blit(willowImage, (150, 150))
        screen.blit(willowImage, (0, 100))
        screen.blit(willowImage, (-100, 250))
        screen.blit(willowImage, (100, 350))
        screen.blit(willowImage, (700, 250))
        screen.blit(willowImage, (800, 100))
        screen.blit(willowImage, (900, 350))
        screen.blit(willowImage, (950, 150))
        screen.blit(willowImage, (550, 160))
        screen.blit(willowImage, (440, 80))
        screen.blit(willowImage, (330, 100))
        screen.blit(afterwordImage, (165, -40))

        # draw buttons and button text
        pygame.draw.rect(screen, GREY, (75, 600, 350, 50))
        pygame.draw.rect(screen, GREY, (850, 600, 350, 50))
        playAgain = font.render("Play Again", True, BLACK)
        exitText = font.render("Exit", True, BLACK)
        screen.blit(playAgain, (150, 610))
        screen.blit(exitText, (985, 610))

        # loads images onto the screen 
        pygame.display.flip()

    # class method for updating game scene, if the attribute scene is set to a certain scene, runs the scene
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

# defines an object using the class Gamescene we created called game
game = GameScene()

# Game Loop
while True:
    # runs the method in the object game "update", which runs whichever gamescene the player is on (set to loading screen by default)
    game.update()
    clock.tick(60)
    
        
            
        
        
        