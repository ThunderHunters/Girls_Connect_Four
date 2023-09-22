# Be sure to pip install any missing imports.
import numpy as np
import pygame
import sys
import math
import pygame.time

# Create a Pygame mixer for sound effects
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Load the sound files (Change the path here to where you downloaded the files)
play_drum = pygame.mixer.Sound("XXX/Snare Drum Hit 01.wav")
play_bongo = pygame.mixer.Sound("XXX/Low Tom Hit 01.wav")
play_sheep = pygame.mixer.Sound("XXX/pp.wav")
play_bell = pygame.mixer.Sound("XXX/bgg.wav")

# Load the background music
pygame.mixer.music.load("XXX/HarmBox.wav")

# Set the volume for the background music
pygame.mixer.music.set_volume(0.4)

# Define colors 
BLUE = (0,0,255)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
MAGENTA = (255,0,255)

# Define game constants
ROW_COUNT = 6
COLUMN_COUNT = 7
TOP_MARGIN = 50  
MESSAGE_HEIGHT = 40  

message = "Girls Connect Four Fun!"

# Function to display instructions
def display_instructions(screen):
    font = pygame.font.Font(None, 24)
    instruction_lines = [
        "Girls Connect Four!",
        "1. Click on the column where you want to place your piece.",
        "2. Try to connect four of your pieces in a row, vertically, horizontally, or diagonally.",
        "3. The first player to connect four wins the game.",
    ]

    # Calculate the total height of the instructions
    total_height = len(instruction_lines) * 22

    # Calculate the X-coordinate to center the instructions
    margin_x = (screen.get_width() - total_height) // 15

    # Y-coordinate for the top margin
    margin_y = 10  # Adjust as needed

    for idx, line in enumerate(instruction_lines):
        text = font.render(line, True, MAGENTA)
        text_rect = text.get_rect()
        text_rect.topleft = (margin_x, margin_y + idx * 22)  # Adjust Y-coordinate for spacing
        screen.blit(text, text_rect)


# Function to display the message on the screen
def display_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, BLUE)
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx  # Center horizontally
    text_rect = text_rect.move(0, 20)  # Move the text down by 20 pixels
    screen.blit(text, text_rect)

# Reset game variables and board
def restart_game():
    global game_over, board, turn
    game_over = False
    board = create_board()
    turn = 0
    draw_border()

# Create Border
def draw_border():
    pygame.draw.rect(screen, (0, 0, 255), (0, 0, width, height), 3)   

# Create Board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Create Game Logic
def drop_piece(board, row, selection, piece):
    board[row][selection] = piece

def is_valid_location(board, selection):
    return board[ROW_COUNT - 1][selection] == 0

def get_next_open_row(board, selection):
    for r in range(ROW_COUNT):
        if board[r][selection] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))
    

def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
            

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positive diagonals for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negative diagonals for a win
    for c in range(3, COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, YELLOW, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            draw_border()
           

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, MAGENTA, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

# Initialize game variables
board = create_board()
print_board(board)
game_over = False
turn = 0

SQUARESIZE = 100
width = COLUMN_COUNT  * SQUARESIZE 
height = (ROW_COUNT+1) * SQUARESIZE 
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
print_board(board)
draw_board(board, screen)
display_instructions(screen)
pygame.display.update()

myfont = pygame.font.SysFont("Comic Sans MS", 50)

# Set the caption (window title)
pygame.display.set_caption("Girls Connect Four")
screen.fill((0,0,0))

# Set a flag to track if the music has started
music_started = False

while True:

# Check if music should start after 10 seconds
    if not music_started:
                    if pygame.time.get_ticks() >= 1000:  # 10 seconds delay
                        pygame.mixer.music.play(-1)
                        music_started = True   

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


        display_message(screen, "Girls Connect Four Fun!")


        if event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = event.pos 
                 

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            selection = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, selection):
                if turn == 0:
                    row = get_next_open_row(board, selection)
                    drop_piece(board, row, selection, 1)
                    play_drum.play()
                    
                    if winning_move(board, 1):
                        # Clear the margin by filling it with the background color (black)
                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, TOP_MARGIN))
                        label = myfont.render("Player 1 Wins!", 1, MAGENTA)
                        message_x = (width - label.get_width()) // 2
                        message_y = TOP_MARGIN -30
                        screen.blit(label, (message_x, message_y))
                        game_over = True
                        play_bell.play()
                        
                else:
                    row = get_next_open_row(board, selection)
                    drop_piece(board, row, selection, 2)
                    play_bongo.play()
                    display_message(screen, "Girls Connect Four Fun!")

                    if winning_move(board, 2):
                        # Clear the margin by filling it with the background color (black)
                        pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, TOP_MARGIN))                        
                        label = myfont.render("Player 2 Wins!", 1, BLUE)
                        message_x = (width - label.get_width()) // 2
                        message_y = TOP_MARGIN -30
                        screen.blit(label, (message_x, message_y))
                        game_over = True
                        play_sheep.play()
                        
                print_board(board)
                draw_board(board, screen)
                screen.fill((0,0,0))
                turn += 1
                turn = turn % 2

            if game_over:
                restart_game()
             
                