import pygame
import random
import sys

# Constants
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
GRID_SIZE = 3
CELL_SIZE = 100
SCREEN_WIDTH = CELL_SIZE * GRID_SIZE
SCREEN_HEIGHT = CELL_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (242, 85, 96)
CROSS_COLOR = (28, 170, 156)
BUTTON_COLOR = (28, 170, 156)
BUTTON_HOVER_COLOR = (28, 128, 120)
TEXT_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, 36)


# Function to initialize the board
def initialize_board():
    return [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


# Function to check for a winner
def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
    for col in range(GRID_SIZE):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    if all(cell != EMPTY for row in board for cell in row):
        return 'Draw'
    return None


# Function to draw the grid
def draw_grid():
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (SCREEN_WIDTH, row * CELL_SIZE), 3)
        pygame.draw.line(screen, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, SCREEN_HEIGHT), 3)


# Function to draw X and O
def draw_move(row, col, player):
    center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
    if player == PLAYER_X:
        pygame.draw.line(screen, CROSS_COLOR, (center[0] - 30, center[1] - 30), (center[0] + 30, center[1] + 30), 5)
        pygame.draw.line(screen, CROSS_COLOR, (center[0] + 30, center[1] - 30), (center[0] - 30, center[1] + 30), 5)
    elif player == PLAYER_O:
        pygame.draw.circle(screen, CIRCLE_COLOR, center, 40, 5)


# Function to handle AI move (easy mode: random move)
def random_move(board):
    available_moves = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == EMPTY]
    return random.choice(available_moves) if available_moves else None


# Function to handle AI move (hard mode: minimax algorithm)
def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == PLAYER_X:
        return -1
    elif winner == PLAYER_O:
        return 1
    elif winner == 'Draw':
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board[r][c] == EMPTY:
                    board[r][c] = PLAYER_O
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[r][c] = EMPTY
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board[r][c] == EMPTY:
                    board[r][c] = PLAYER_X
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[r][c] = EMPTY
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score


# Function to get the best AI move (hard mode)
def best_move(board):
    best_score = -float('inf')
    move = None
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == EMPTY:
                board[r][c] = PLAYER_O
                score = minimax(board, 0, False, -float('inf'), float('inf'))
                board[r][c] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move


# Function to handle the player's move
def handle_move(row, col, board, current_player):
    if board[row][col] == EMPTY:
        board[row][col] = current_player
        return True
    return False


# Function to display the difficulty selection screen
def display_difficulty_screen():
    screen.fill(WHITE)
    title_text = font.render("Tic Tac Toe", True, LINE_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

    easy_button = pygame.Rect(SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2, 200, 50)
    hard_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)

    # Button Hover Effects
    mouse_x, mouse_y = pygame.mouse.get_pos()
    easy_button_color = BUTTON_HOVER_COLOR if easy_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    hard_button_color = BUTTON_HOVER_COLOR if hard_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR

    pygame.draw.rect(screen, easy_button_color, easy_button)
    pygame.draw.rect(screen, hard_button_color, hard_button)

    easy_text = font.render("Easy", True, TEXT_COLOR)
    hard_text = font.render("Hard", True, TEXT_COLOR)
    screen.blit(easy_text, (SCREEN_WIDTH // 4 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    pygame.display.update()

    difficulty = None
    while difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if easy_button.collidepoint(x, y):
                    difficulty = "Easy"
                elif hard_button.collidepoint(x, y):
                    difficulty = "Hard"
    return difficulty


# Function to display the restart, exit, and difficulty selection buttons after a game ends
def display_end_screen(winner):
    screen.fill(WHITE)

    # Display "Game Over!" and who won
    if winner == 'Draw':
        winner_text = font.render("It's a Draw!", True, LINE_COLOR)
    else:
        winner_text = font.render(f"{winner} Wins!", True, LINE_COLOR)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 4))

    # Buttons - Restart, Exit, Easy, Hard
    button_width = 200
    button_height = 50
    margin = 60  # Distance between buttons

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2, button_width, button_height)
    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_height + margin,
                              button_width, button_height)
    easy_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + (button_height + margin) * 2,
                              button_width, button_height)
    hard_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + (button_height + margin) * 3,
                              button_width, button_height)

    # Button Hover Effects
    mouse_x, mouse_y = pygame.mouse.get_pos()
    restart_button_color = BUTTON_HOVER_COLOR if restart_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    exit_button_color = BUTTON_HOVER_COLOR if exit_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    easy_button_color = BUTTON_HOVER_COLOR if easy_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    hard_button_color = BUTTON_HOVER_COLOR if hard_button.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR

    pygame.draw.rect(screen, restart_button_color, restart_button)
    pygame.draw.rect(screen, exit_button_color, exit_button)
    pygame.draw.rect(screen, easy_button_color, easy_button)
    pygame.draw.rect(screen, hard_button_color, hard_button)

    restart_text = font.render("Restart", True, TEXT_COLOR)
    exit_text = font.render("Exit", True, TEXT_COLOR)
    easy_text = font.render("Easy", True, TEXT_COLOR)
    hard_text = font.render("Hard", True, TEXT_COLOR)

    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(exit_text,
                (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + button_height + margin + 10))
    screen.blit(easy_text, (
    SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2 + (button_height + margin) * 2 + 10))
    screen.blit(hard_text, (
    SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2 + (button_height + margin) * 3 + 10))

    pygame.display.update()

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if restart_button.collidepoint(x, y):
                    game_over = True  # Restart the game
                    return True  # Indicate restart
                elif exit_button.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()
                elif easy_button.collidepoint(x, y):
                    game_over = True  # Restart the game
                    return "Easy"
                elif hard_button.collidepoint(x, y):
                    game_over = True  # Restart the game
                    return "Hard"


# Main game loop
def game_loop(difficulty):
    board = initialize_board()
    current_player = PLAYER_X
    winner = None

    while winner is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if handle_move(row, col, board, current_player):
                    current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X

        # AI move
        if current_player == PLAYER_O:
            if difficulty == "Easy":
                move = random_move(board)
            elif difficulty == "Hard":
                move = best_move(board)
            if move:
                board[move[0]][move[1]] = PLAYER_O
                current_player = PLAYER_X

        # Check for winner
        winner = check_winner(board)
        if winner:
            display_end_screen(winner)
            difficulty = display_difficulty_screen()  # Ask for new difficulty level on restart
            game_loop(difficulty)  # Restart with new difficulty level
            return  # Exit after game ends

        # Draw grid and moves
        screen.fill(WHITE)
        draw_grid()
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board[r][c] != EMPTY:
                    draw_move(r, c, board[r][c])

        pygame.display.update()


# Display difficulty selection on startup
difficulty = display_difficulty_screen()
game_loop(difficulty)
