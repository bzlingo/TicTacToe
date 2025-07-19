import tkinter as tk #a Python module for creating graphical user interfaces (GUIs).
from tkinter import messagebox #submodule from Tkinter, which provides functions to display pop-up messages

# Game Logic by Abdallah
def check_win(board, player):
    win_combos = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in win_combos:
        if board[a] == board[b] == board[c] == player: #if a,b,c matches the winning combos above and they equal one letter
            return True #indicates that the player won
    return False #If none of the winning combos result in a match, indicates that the player has not won.

def is_full(board):
    return all(cell != ' ' for cell in board)
#the method above checks if there are no empty squares left on the TicTacToe board
#either continuing the game if False or terminating the game if True

def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == ' ']
# The method’s purpose is to return a list of indices corresponding to empty positions on the Tic-Tac-Toe board where player or AI can make a move
# The enumerate function iterates over self.board and provides both the index (i) and the value (spot) of each element


# Minimax Algorithm by Fadlia and assem
def minimax(board, is_maximizing): #Defines the minimax function,
    if check_win(board, 'O'):      #Checks if the AI 'O' has won by calling check_win.
        return 1
    elif check_win(board, 'X'):    #Checks if the human 'X' has won
        return -1                  #a negative outcome for the AI
    elif is_full(board):           #Checks if the board is full
        return 0                   #Draw (nobody wins)

    if is_maximizing: #If True, it’s the AI’s turn 'O', aiming to maximize the score
        best_score = -float('inf') #Initializes best_score to negative infinity, ensuring any evaluated score will be higher initially.
        for i in available_moves(board): #Loops over the indices of empty cells on the board, retrieved by available_moves
            board[i] = 'O' #Simulates the AI placing 'O' in the current empty cell.
            score = minimax(board, False) #Recursively calls minimax with is_maximizing=False (human’s turn) to evaluate the outcome of this move
            board[i] = ' ' #Undoes the move by resetting the cell to empty, allowing further exploration.
            best_score = max(score, best_score) #Updates best_score to the maximum of the current best_score and the score from the recursive call
        return best_score #Returns the best score found for the AI’s move.
    else: #If is_maximizing is False, it’s the human’s turn 'X', aiming to minimize the score.
        best_score = float('inf') #Initializes best_score to positive infinity, ensuring any evaluated score will be lower initially.
        for i in available_moves(board): #Loops over the indices of empty cells on the board, retrieved by available_moves
            board[i] = 'X' #Simulates the Human placing 'X' in the current empty cell.
            score = minimax(board, True) #Explanation: Recursively calls minimax with is_maximizing=True (AI’s turn) to evaluate this move.
            board[i] = ' '  #Undoes the move by resetting the cell to empty, allowing further exploration
            best_score = min(score, best_score) #Updates best_score to the minimum of the current best_score and the score from the recursive call
        return best_score #Returns the best score found for the human’s move

def find_best_move(board): #optimal move for AI
    best_score = -float('inf') #Initializes best_score to negative infinity to track the highest score.
    best_move = None #Initializes best_move to None to store the index of the best move
    for i in available_moves(board): #Loops over the indices of empty cells.
        board[i] = 'O' #Simulates the AI placing 'O' in the current cell.
        score = minimax(board, False) #Calls minimax to evaluate the move, assuming the human’s turn
        board[i] = ' ' #Undoes the move by resetting the cell to empty, allowing further exploration
        if score > best_score: #Checks if the current move’s score is  better than the previous best_score.
            best_score = score #Updates best_score to the new higher score.
            best_move = i #Sets best_move to the index of the current cell.
    return best_move #Returns the index of the best move for the AI.

# GUI with Tkinter by khaled and Abdelrhman
class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk() #stores tkinter window
        self.root.title("Tic Tac Toe") #title for the window
        self.board = [' ']*9 #board initialization as a list of 9 empty spaces ('')
        self.current_player = 'X' #Sets the starting player to 'X' (human).
        self.buttons = [] #Creates an empty list to store the button widgets for the 3x3 grid.
        self.create_board() #Calls the create_board method to set up the GUI buttons.
        self.root.mainloop() #Tkinter loop, keeping the window ineractive

    def create_board(self): #create the 3x3 grid of buttons.
        for i in range(3): #Loops over rows (0 to 2).
            for j in range(3): #Loops over columns (0 to 2) for each row.
                btn = tk.Button(self.root, text=' ', font=('Arial', 20), height=2, width=4,
                                command=lambda row=i, col=j: self.on_click(row, col))
                #Links the button to on_click with the current row and col.
                btn.grid(row=i, column=j) #sets the button grid adjustment
                self.buttons.append(btn) #Adds the button to the self.buttons list for later

    def on_click(self, row, col):
        if self.board[row*3 + col] == ' ' and self.current_player == 'X':#Checks if the clicked cell is empty and it’s the human’s turn ('X').
            #The index is calculated as row*3 + col to map 2D coordinates to the 1D board list.
            self.board[row*3 + col] = 'X'  #Places 'X' in the clicked cell on the board.
            self.buttons[row*3 + col].config(text='X') #Updates the button’s text to display 'X'.
            if check_win(self.board, 'X'): #Checks if 'X' has won.
                messagebox.showinfo("Game Over", "Human wins!") #never happens
                self.reset_game()
            elif is_full(self.board): #checks for a tie
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else: #if no win or tie, proceed the game
                self.current_player = 'O' #switches to AI's turn
                self.ai_move() #Calls ai_move to let the AI respond

    def ai_move(self):
        move = find_best_move(self.board) #Uses find_best_move to determine the AI’s optimal move.
        if move is not None: #Checks if a valid move was found (should always be true unless the board is full).
            self.board[move] = 'O' #Places 'O' at the chosen position on the board.
            row, col = divmod(move, 3) #Converts the 1D index move to 2D coordinates (row, col) using divmod (e.g., index 4 → row 1, col 1).
            self.buttons[move].config(text='O') #Updates the corresponding button to display 'O'.
            if check_win(self.board, 'O'): #Checks if the AI has won.
                messagebox.showinfo("Game Over", "O wins!") #AI wins
                self.reset_game() #resets the game for a new one
            elif is_full(self.board): #checks for a tie
                messagebox.showAinfo("Game Over", "It's a tie!") #Draw
                self.reset_game() #resets
            self.current_player = 'X' #Human's turn

    def reset_game(self): #Defines reset_game to restore the initial game state.
        self.board = [' ']*9 #Resets the board to 9 empty spaces.
        for btn in self.buttons:
            btn.config(text=' ') #Clears each button’s text.
        self.current_player = 'X' #Human's turn

#Game
if __name__ == "__main__":
    game = TicTacToeGUI()