from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import glob
import random

root = Tk()
root.title("XO")
root.iconbitmap("xo.ico")

button_size = (109, 95)

x_image_path = glob.glob("images/X.png")[0]
o_image_path = glob.glob("images/O.png")[0]

# Resize images to match button size
x_img = Image.open(x_image_path).resize(button_size)
o_img = Image.open(o_image_path).resize(button_size)

# Convert to Tkinter-compatible images
x_tk = ImageTk.PhotoImage(x_img)
o_tk = ImageTk.PhotoImage(o_img)

board = [[""for r in range(3)] for c in range(3)] #طريقة لزيزة بالتكرار دونها
current_turn = "player"

user_score = 0
pc_score = 0
game_over = False

# To make btns disabel in runtime
def disabel():
    for row in btns:
        for btn in row:
            btn.config(state=DISABLED)

# To reset the buttons board and make scores zero after game over
def reset(action):
    global game_over, current_turn, user_score, pc_score
    if game_over:
        reset_btn.config(state=ACTIVE)
    if action:
        text = ""
        if user_score > pc_score:
            text = "You are ahead of the opponent"
        elif user_score <= pc_score:
            text="You have a chance to improve the score"
        response = messagebox.askyesno("Restart", text+"\nDo you want to reset the game?")
        if response == True:
            user_score = 0
            pc_score = 0
            label_2.config(text=user_score)
            label_4.config(text=pc_score)
            label_6.config(text="")
            game_over = False
            current_turn = "player"
            for r in range(3):
                for c in range(3):
                    btn = btns[r][c]  
                    btn.config(image="", bg="black", state=NORMAL, width=15, height=6)
                    btn.image = None   
                    board[r][c] = ""
            reset_btn.config(state=DISABLED)
            restart_btn.config(state=DISABLED)
        else:
            return

# To restart the game and clear the btns board after the game over 
def restart(action):
    global game_over, current_turn
    if game_over:
        restart_btn.config(state=ACTIVE)
    if action:
        label_6.config(text="")
        game_over = False
        current_turn = "player"
        for r in range(3):
            for c in range(3):
                btn = btns[r][c]  
                btn.config(image="", bg="black", state=NORMAL, width=15, height=6)
                btn.image = None 
                board[r][c] = ""
        restart_btn.config(state=DISABLED)
        reset_btn.config(state=DISABLED)
    
# To decide who is the winner
def winner():
    global user_score, pc_score, game_over
    winning_combinations = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    for combo in winning_combinations:
        symbols = [board[r][c] for r, c in combo]
        if symbols == ["X", "X", "X"]:
            label_6.config(text="You Win!!", fg="green")
            user_score += 1
            label_2.config(text=user_score)
            for r, c in combo:
                btns[r][c].config(bg="green")
            disabel()
            game_over = True
            root.after(300, lambda: restart(False))
            root.after(300, lambda: reset(False))
            return  
        elif symbols == ["O", "O", "O"]:
            label_6.config(text="PC Wins!!", fg="red")
            pc_score += 1
            label_4.config(text=pc_score)
            for r, c in combo:
                btns[r][c].config(bg="red")
            disabel()
            game_over = True
            root.after(300, lambda: restart(False))
            root.after(300, lambda: reset(False))
            return  

    # Check for tie 
    if all(board[r][c] != "" for r in range(3) for c in range(3)):
        for r in range(3):
            for c in range(3):
                btns[r][c].config(bg="yellow")
        label_6.config(text="Tie!!", fg="#FFD700")
        disabel()
        game_over = True
        root.after(300, lambda: restart(False))
        root.after(300, lambda: reset(False))

# The player move
def place_symbol(button, row, column):
    global current_turn, game_over
    if game_over:
        return
    if board[row][column]=="" and current_turn =="player":
        button.config(image=x_tk, width=109, height=95)
        button.image = x_tk
        board[row][column] = "X"
        winner()
        current_turn = "PC"
        if not game_over:
            root.after(500, pc_move)

# The pc move
def pc_move():
    global current_turn
    #دون هذه الطريقة لانها حلوة و تعلم اكثر عنها
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
    if empty:
        r, c = random.choice(empty)
        button = btns[r][c]
        button.config(image=o_tk, width=109, height=95)
        button.image = o_tk
        board[r][c] = "O"
        current_turn = "player"
    winner()

# Create the scores frame and show the result after rounds
frame_result = LabelFrame(root, text="Scores", padx=60, pady=5)

label_1 = Label(frame_result, text="You  ", font=("Arial", 14), padx=15, anchor=E)
label_2 = Label(frame_result, text=user_score, font=("Arial", 14), anchor=E)
label_3 = Label(frame_result, text=":", font=("Arial", 14))
label_4 = Label(frame_result, text=pc_score, font=("Arial", 14), anchor=W)
label_5 = Label(frame_result, text="  PC", font=("Arial", 14), padx=16, anchor=W)
label_6 = Label(frame_result, text="", font=("Arial", 18), bd=5)

# To put the element on window
frame_result.pack()
label_1.grid(row=0, column=0, sticky=W+E)
label_2.grid(row=0, column=1, sticky=W+E)
label_3.grid(row=0, column=2, sticky=W+E)
label_4.grid(row=0, column=3, sticky=W+E)
label_5.grid(row=0, column=4, sticky=W+E)
label_6.grid(row=1, column=0, columnspan=5, sticky=W+E)

# Create frame and btns to control in the game after every round
frame_buttons =Frame(root, padx=5, pady=5,)

reset_btn = Button(frame_buttons, text="Reset", font=("NewRoman", 10), height=2, width=14, relief="groove", state=DISABLED, command=lambda : reset(True))
restart_btn = Button(frame_buttons, text="Restart", font=("NewRoman", 10), height=2, width=14, relief="groove", state=DISABLED, command=lambda : restart(True))

frame_buttons.pack(pady=10)
reset_btn.grid(row=0, column=0, sticky=W+E)
restart_btn.grid(row=0, column=1, sticky=W+E)

# Create square btns frame as space play
frame_squares = Frame(root, padx=5, pady=5)

# Make btns in grid
btns = []
for row in range(3):
    row_btns = []
    for col in range(3):
        btn = Button(frame_squares, width=15, height=6, bg="#000000")
        btn.config(command=lambda b=btn, r=row, c=col: place_symbol(b, r, c))
        btn.grid(row=row, column=col)
        row_btns.append(btn)
    btns.append(row_btns)

frame_squares.pack()

root.mainloop()
