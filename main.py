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
#fonts
titleFont = pygame.font.SysFont('comicsans', 85, True, False)
font = pygame.font.SysFont('comicsans', 45, True, False)
buttonFont = pygame.font.SysFont('comicsans', 25, True, False)

#Rectangle Value
rectY = 360

#Hangman Buttons
radius = 30
buttons = []
button_num = 0 
A = 65 
for i in range(13):
    x = 300 + i*60
    y = 450
    buttons.append([x, y, chr(A + i)])
for i in range(13):
    x = 300 + i*60
    y = 520
    buttons.append([x, y, chr(A + i + 13)])

#game variable
ram = 4

#Questions and Words
questions_list = ["A circuit board that contains all principle components of the computer", 
"The brain of the computer, it's performance is measured in Ghz ", 
"A specialized processor used to accelerate the rendering of  graphics"
]
words_list = ["MOTHERBOARD", "CPU", "GPU"]
question_number = 0
word_number = 0 
guessed = []

#draw ram variables
ramX = 175
ramY = 600
ramImage = 4
#text
textOne = titleFont.render("Hardware Hangman", True, BLACK)
textTwo = font.render("Easy", True, BLACK)
textThree = font.render("Hard", True, BLACK)
#global variable
clock = pygame.time.Clock()

#setting up the screen size
screenSize = (1280, 720)
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Hardware Hangman")


#background images
background = pygame.image.load("background1.png").convert()



class GameScene:
    def __init__(self):
        self.scene = "loading"

    # Menu Scene
    def loading(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                press_easy = mouse_x > 427 and mouse_x < 854 and mouse_y > 360 and mouse_y < 410
                press_hard = mouse_x > 427 and mouse_x < 854 and mouse_y > 450 and mouse_y < 500
                if press_easy:
                    self.scene = "maingame"
                if press_hard:
                    self.scene = "maingame"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.scene = "failscreen"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.scene = "victoryscreen"


        screen.fill(WHITE)
        screen.blit(textOne, (325, 50))

        pygame.draw.rect(screen, GREY, (427, rectY, 427, 50))
        pygame.draw.rect(screen, GREY, (427, 450, 427, 50))

        screen.blit(textTwo, (600, 373))
        screen.blit(textThree, (600, 463))

        
        pygame.display.flip()
    
    # The scene that contains the central hangman game
    def maingame(self):
        global question_number
        global word_number
        global ram
        global guessed
        

        screen.fill(WHITE)
        
        #Draws the Questions
        if len(questions_list[question_number]) < 65:
            question = font.render(questions_list[question_number], True, BLACK)
            screen.blit(question, (100, 50))
        if len(questions_list[question_number]) > 65:

            quesLineOne = font.render(questions_list[question_number][:61], True, BLACK)
            quesLineTwo = font.render(questions_list[question_number][61:], True, BLACK)
            screen.blit(quesLineOne, (100, 50))
            screen.blit (quesLineTwo, (550, 80))
        
        #Prints the word that user is trying to guess
        
        guessed_word = ""
        
        for letter in words_list[word_number]:
            if letter in guessed:
                guessed_word += letter
            else:
                guessed_word += "_ "
            
        
        text = font.render(guessed_word ,True , BLACK)
        screen.blit(text, (480, 250))

        #Draws the buttons
        for button in buttons:
            x, y, letter = button
            pygame.draw.circle(screen, BLACK, (x, y), radius, 5)
            buttonletter = buttonFont.render(letter, True, BLACK)
            screen.blit(buttonletter, [x-6,y-8])
        
        #Moves on to next word if the word is gussed correctly
        if guessed_word == words_list[word_number]:
            question_number += 1
            word_number += 1
            guessed = []
        #draw ram
        
        for i in range(ram):
            ramImage = pygame.image.load("ram.jpg").convert()
            ramImage = pygame.transform.scale(ramImage, (270, 100))
            screen.blit(ramImage, (ramX + i * 225, ramY))
            
    
        #If the user loses all his ram, changes to fail screen 
        ramCounter = font.render(("RAM left:" + str(ram)), True, BLACK)
        screen.blit(ramCounter, (0, 680))
        if ram == 0:
            self.scene = "failscreen"
        
        #If the user guesses all the words correctly, changes to victory screen
        if word_number == len(words_list):
            self.scene = "victoryscreen"


        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in buttons:
                    x, y, letter = button
                    distanceFromButton = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                    if distanceFromButton < radius:
                        guessed.append(letter)
                        if letter not in words_list[word_number]:
                            ram -= 1
                            print(ram)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.scene = "failscreen"
        

            
        pygame.display.flip()

    # failscreen
    def failscreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        failImage = pygame.image.load("failscreen.jpg").convert()
        screen.blit(failImage, (0, 0))
        pygame.draw.rect(screen, BLUE, (125, 376, 250, 60))

        

        pygame.display.flip()

    #victory screen
    def victoryscreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        screen.blit(background, (0,0))
        victoryText = titleFont.render("You WON!", True, BLACK)
        for i in range(5):
            screen.blit(victoryText, (80, 120 + i * 100))
        for i in range(5):
            screen.blit(victoryText, (875, 120 + i * 100))
        
        pygame.display.flip()
    
    def update(self): 
        if self.scene == "loading":
            self.loading()
        if self.scene == "maingame":
            self.maingame()
        if self.scene == "failscreen":
            self.failscreen()
        if self.scene == "victoryscreen":
            self.victoryscreen()
        

game_scene = GameScene()

    

while True:
    #developer access
  
    game_scene.update()
    clock.tick(60)
        
            
        
        
            


         