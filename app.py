from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4
from flask_debugtoolbar import DebugToolbarExtension

from boggle import BoggleGame


app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# Enable flask debug toolbar
app.debug = True
toolbar = DebugToolbarExtension(app)

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    
    
    return jsonify({
        "gameId": game_id, 
        "board": games[game_id].board
        })

@app.route("/api/score-word", methods=["POST"])
def score_word():
    """Accept a post request with JSON for game id and a word to score or reject if illegal
    Returns a json object of a result string e.g.: {result: "not-on-board"}
    """
    gameId = request.json["gameId"]
    word = request.json["word"].upper()
    game = games[gameId]
    
    if game.is_word_in_word_list(word) and game.check_word_on_board(word):
        if game.is_word_not_a_dup(word):
            result = "ok"
        else:
            result = "duplicate"
    elif not game.is_word_in_word_list(word):
        result = "not-word"
    else:
        result = "not-on-board"
    
    game.play_and_score_word(word)
    
    return jsonify({"result": result})
    