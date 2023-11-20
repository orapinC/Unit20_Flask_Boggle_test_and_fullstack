from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "notSoSecretKey"

boggle_game = Boggle()

@app.route("/")
def homepage():
    """display boggle game board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore',0)
    nplays = session.get('nplays',0)
    return render_template("index.html", board=board, highscore=highscore, nplays=nplays)

@app.route("/check-word")
def checkword():
    """word in dictionary"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board,word)
    return jsonify({'result': response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """post score, keep tract of no of play, and high score."""
    #get score from front-end
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays",0)
    session['nplays'] = nplays +1
    session['highscore'] = max(score, highscore)
    return jsonify(brokeRecord=score>highscore)