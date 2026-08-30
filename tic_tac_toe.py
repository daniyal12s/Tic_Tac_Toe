import tkinter as tk
from tkinter import messagebox

# ============================================
#           COLOR PALETTE
# ============================================

BG_PRIMARY = "#1a1a2e"
BG_SECONDARY = "#16213e"
ACCENT_PRIMARY = "#0f3460"
ACCENT_SECONDARY = "#e94560"
COLOR_X = "#00d4ff"
COLOR_O = "#ff6b6b"
COLOR_WIN = "#2ecc71"
COLOR_DRAW = "#ffd93d"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#b0b0b0"

# ============================================
#           WINDOW SETUP
# ============================================

root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("550x820")
root.resizable(False, False)
root.configure(bg=BG_PRIMARY)

# ============================================
#           VARIABLES
# ============================================

current_player = "X"
game_over = False

score_x = 0
score_o = 0
draw_score = 0

player_x_name = "Player X"
player_o_name = "Player O"

buttons = []
board = [""] * 9
winning_cells = []

# ============================================
#           FUNCTIONS
# ============================================

def update_score():
    """Update score display with current scores"""
    score_x_label.config(text=str(score_x))
    score_o_label.config(text=str(score_o))
    score_draw_label.config(text=str(draw_score))

def update_player_names():
    """Update player names in UI"""
    x_name_label.config(text=player_x_name)
    o_name_label.config(text=player_o_name)
    turn_label.config(
        text=f"Current Turn: {player_x_name} (X)",
        fg=COLOR_X
    )

def change_turn():
    """Switch between players"""
    global current_player
    
    if current_player == "X":
        current_player = "O"
        turn_label.config(
            text=f"Current Turn: {player_o_name} (O)",
            fg=COLOR_O
        )
    else:
        current_player = "X"
        turn_label.config(
            text=f"Current Turn: {player_x_name} (X)",
            fg=COLOR_X
        )

def check_winner():
    """Check for winning combinations and highlight winning cells"""
    global score_x, score_o, draw_score, game_over, winning_cells
    
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    
    # Check for winner
    for combo in winning_combinations:
        a, b, c = combo
        
        if board[a] == board[b] == board[c] != "":
            # Highlight winning cells
            winning_cells = combo
            for idx in combo:
                buttons[idx].config(bg=COLOR_WIN, fg=TEXT_PRIMARY)
            
            winner_name = player_x_name if board[a] == "X" else player_o_name
            
            if board[a] == "X":
                score_x += 1
            else:
                score_o += 1
            
            update_score()
            game_over = True
            
            messagebox.showinfo(
                "🎉 Winner",
                f"Congratulations!\n{winner_name} Wins!",
                parent=root
            )

            # Automatically start the next round after pressing OK
            restart_game()
            
            return True
    
    # Check for draw
    if all(cell != "" for cell in board):
        draw_score += 1
        update_score()
        game_over = True
        
        messagebox.showinfo(
            "🤝 Draw",
            "It's a Draw! Well Played!",
            parent=root
        )

        # Automatically start the next round after pressing OK
        restart_game()


        
        return True
    
    return False

def button_click(index):
    """Handle button click event"""
    global game_over, current_player
    
    # Validation
    if game_over:
        return
    
    if board[index] != "" or buttons[index]["text"] != "":
        return
    
    # Update board
    board[index] = current_player
    
    # Update button display
    color = COLOR_X if current_player == "X" else COLOR_O
    buttons[index]["text"] = current_player
    buttons[index]["fg"] = color
    # Keep the button enabled so Tkinter does not replace X/O with gray.
    # Occupied cells are already blocked by the validation above.
    
    # Check game status
    if not check_winner():
        change_turn()

def restart_game():
    """Restart game without resetting scores"""
    global current_player, game_over, board, winning_cells
    
    current_player = "X"
    game_over = False
    board = [""] * 9
    winning_cells = []
    
    # Reset all buttons
    for i, btn in enumerate(buttons):
        btn.config(
            text="",
            fg=TEXT_PRIMARY,
            bg=ACCENT_PRIMARY,
            activebackground=ACCENT_PRIMARY,
            activeforeground=TEXT_PRIMARY,
            disabledforeground=TEXT_PRIMARY,
            state=tk.NORMAL
        )
    
    # Reset turn label
    turn_label.config(
        text=f"Current Turn: {player_x_name} (X)",
        fg=COLOR_X
    )

def reset_score():
    """Reset all scores and restart game"""
    global score_x, score_o, draw_score
    
    score_x = 0
    score_o = 0
    draw_score = 0
    
    update_score()
    restart_game()

def update_names_from_input():
    """Update player names from input fields"""
    global player_x_name, player_o_name
    
    new_x_name = x_input.get().strip()
    new_o_name = o_input.get().strip()
    
    if new_x_name == "":
        messagebox.showwarning("Warning", "Player X name cannot be empty!", parent=root)
        return
    
    if new_o_name == "":
        messagebox.showwarning("Warning", "Player O name cannot be empty!", parent=root)
        return
    
    player_x_name = new_x_name
    player_o_name = new_o_name
    
    update_player_names()
    restart_game()
    
    messagebox.showinfo("Success", "Player names updated!", parent=root)

# Hover effects for board buttons
def on_enter(event):
    """Hover enter effect"""
    btn = event.widget
    if btn["text"] == "" and not game_over:
        btn.config(bg=BG_SECONDARY)

def on_leave(event):
    """Hover leave effect"""
    btn = event.widget
    if btn["text"] == "":
        btn.config(bg=ACCENT_PRIMARY)

# ============================================
#           UI CREATION
# ============================================

# -------- HEADER --------
header_frame = tk.Frame(root, bg=BG_PRIMARY)
header_frame.pack(pady=15)

title = tk.Label(
    header_frame,
    text="TIC TAC TOE",
    font=("Segoe UI", 30, "bold"),
    fg=TEXT_PRIMARY,
    bg=BG_PRIMARY
)
title.pack()

# -------- PLAYER NAMES INPUT --------
names_frame = tk.Frame(root, bg=BG_PRIMARY)
names_frame.pack(pady=10)

# Player X Name Input
x_name_input_frame = tk.Frame(names_frame, bg=BG_PRIMARY)
x_name_input_frame.pack(side=tk.LEFT, padx=15)

tk.Label(
    x_name_input_frame,
    text="Player X:",
    font=("Segoe UI", 10, "bold"),
    fg=COLOR_X,
    bg=BG_PRIMARY
).pack(anchor="w")

x_input = tk.Entry(
    x_name_input_frame,
    font=("Segoe UI", 11),
    fg=COLOR_X,
    bg=ACCENT_PRIMARY,
    insertbackground=COLOR_X,
    width=15
)
x_input.pack()
x_input.insert(0, player_x_name)

# Player O Name Input
o_name_input_frame = tk.Frame(names_frame, bg=BG_PRIMARY)
o_name_input_frame.pack(side=tk.LEFT, padx=15)

tk.Label(
    o_name_input_frame,
    text="Player O:",
    font=("Segoe UI", 10, "bold"),
    fg=COLOR_O,
    bg=BG_PRIMARY
).pack(anchor="w")

o_input = tk.Entry(
    o_name_input_frame,
    font=("Segoe UI", 11),
    fg=COLOR_O,
    bg=ACCENT_PRIMARY,
    insertbackground=COLOR_O,
    width=15
)
o_input.pack()
o_input.insert(0, player_o_name)

# Update Names Button
update_names_btn = tk.Button(
    names_frame,
    text="✏️ Update",
    font=("Segoe UI", 10, "bold"),
    bg="#6c5ce7",
    fg=TEXT_PRIMARY,
    activebackground="#5f4bd4",
    activeforeground=TEXT_PRIMARY,
    relief=tk.FLAT,
    padx=12,
    pady=3,
    cursor="hand2",
    command=update_names_from_input
)
update_names_btn.pack(side=tk.LEFT, padx=10, pady=23)

# -------- TURN INDICATOR --------
turn_label = tk.Label(
    root,
    text=f"Current Turn: {player_x_name} (X)",
    font=("Segoe UI", 14, "bold"),
    fg=COLOR_X,
    bg=BG_PRIMARY
)
turn_label.pack(pady=8)

# -------- SCOREBOARD --------
score_frame = tk.Frame(root, bg=BG_PRIMARY)
score_frame.pack(pady=12)

# Player X Card
x_card = tk.Frame(
    score_frame,
    bg=ACCENT_PRIMARY,
    relief=tk.FLAT,
    highlightthickness=2,
    highlightbackground=COLOR_X
)
x_card.grid(row=0, column=0, padx=10, pady=5)

x_name_label = tk.Label(
    x_card,
    text=player_x_name,
    font=("Segoe UI", 10, "bold"),
    fg=COLOR_X,
    bg=ACCENT_PRIMARY
)
x_name_label.pack(pady=(6, 2))

score_x_label = tk.Label(
    x_card,
    text="0",
    font=("Segoe UI", 26, "bold"),
    fg=COLOR_X,
    bg=ACCENT_PRIMARY
)
score_x_label.pack(padx=18, pady=(0, 6))

# Draw Card
draw_card = tk.Frame(
    score_frame,
    bg=ACCENT_PRIMARY,
    relief=tk.FLAT,
    highlightthickness=2,
    highlightbackground=COLOR_DRAW
)
draw_card.grid(row=0, column=1, padx=10, pady=5)

tk.Label(
    draw_card,
    text="Draws",
    font=("Segoe UI", 10, "bold"),
    fg=COLOR_DRAW,
    bg=ACCENT_PRIMARY
).pack(pady=(6, 2))

score_draw_label = tk.Label(
    draw_card,
    text="0",
    font=("Segoe UI", 26, "bold"),
    fg=COLOR_DRAW,
    bg=ACCENT_PRIMARY
)
score_draw_label.pack(padx=18, pady=(0, 6))

# Player O Card
o_card = tk.Frame(
    score_frame,
    bg=ACCENT_PRIMARY,
    relief=tk.FLAT,
    highlightthickness=2,
    highlightbackground=COLOR_O
)
o_card.grid(row=0, column=2, padx=10, pady=5)

o_name_label = tk.Label(
    o_card,
    text=player_o_name,
    font=("Segoe UI", 10, "bold"),
    fg=COLOR_O,
    bg=ACCENT_PRIMARY
)
o_name_label.pack(pady=(6, 2))

score_o_label = tk.Label(
    o_card,
    text="0",
    font=("Segoe UI", 26, "bold"),
    fg=COLOR_O,
    bg=ACCENT_PRIMARY
)
score_o_label.pack(padx=18, pady=(0, 6))

# -------- GAME BOARD --------
board_frame = tk.Frame(root, bg=BG_PRIMARY)
board_frame.pack(pady=12)

for i in range(9):
    btn = tk.Button(
        board_frame,
        text="",
        font=("Segoe UI", 28, "bold"),
        width=3,
        height=1,
        bg=ACCENT_PRIMARY,
        fg=TEXT_PRIMARY,
        activebackground=ACCENT_PRIMARY,
        activeforeground=TEXT_PRIMARY,
        disabledforeground=TEXT_PRIMARY,
        relief=tk.FLAT,
        bd=0,
        cursor="hand2",
        command=lambda i=i: button_click(i)
    )
    
    btn.grid(row=i//3, column=i%3, padx=3, pady=3, ipadx=8, ipady=8)
    
    # Hover effects
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    buttons.append(btn)

# -------- ACTION BUTTONS --------
btn_frame = tk.Frame(root, bg=BG_PRIMARY)
btn_frame.pack(pady=10)

restart_btn = tk.Button(
    btn_frame,
    text="🔄 Restart",
    font=("Segoe UI", 11, "bold"),
    bg=COLOR_WIN,
    fg=BG_PRIMARY,
    activebackground="#27ae60",
    activeforeground=TEXT_PRIMARY,
    relief=tk.FLAT,
    padx=18,
    pady=8,
    cursor="hand2",
    command=restart_game
)
restart_btn.pack(side=tk.LEFT, padx=6)

reset_btn = tk.Button(
    btn_frame,
    text="🔃 Reset",
    font=("Segoe UI", 11, "bold"),
    bg=ACCENT_SECONDARY,
    fg=TEXT_PRIMARY,
    activebackground="#c73e54",
    activeforeground=TEXT_PRIMARY,
    relief=tk.FLAT,
    padx=18,
    pady=8,
    cursor="hand2",
    command=reset_score
)
reset_btn.pack(side=tk.LEFT, padx=6)

# ============================================
#           RUN APPLICATION
# ============================================

root.mainloop()