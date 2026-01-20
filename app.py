from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session storage

def reset_game():
    session["board"] = [" " for _ in range(9)]
    session["current_player"] = "X"

def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == " "]

def check_winner(board):
    win_combos = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a, b, c in win_combos:
        if board[a] == board[b] == board[c] != " ":
            return board[a]

    if " " not in board:
        return "Draw"

    return None

def random_ai_move(board):
    pos = random.choice(available_moves(board))
    board[pos] = "O"

@app.route("/", methods=["GET", "POST"])
def index():
    if "board" not in session:
        reset_game()

    board = session["board"]
    winner = check_winner(board)

    if request.method == "POST" and not winner:
        move = int(request.form["move"])
        if board[move] == " ":
            board[move] = "X"
            winner = check_winner(board)

            if not winner:
                random_ai_move(board)
                winner = check_winner(board)

        session["board"] = board

    return render_template("index.html", board=board, winner=winner)

@app.route("/reset")
def reset():
    reset_game()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
