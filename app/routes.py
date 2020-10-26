from flask import render_template, request, Blueprint, redirect, url_for, flash, session, jsonify
import json

from app.config import Config  
from app.forms import PostForm
from app.logic.utils import get_by_path, to_keep_one

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    form = PostForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        username_payload = {"username" : form.username.data}
        return redirect(url_for("main.statistics", username=username_payload))
    return render_template("home.html", form=form)

@main.route("/statistics")
def statistics():
    from app.logic.analysis import get_top_games, get_move_tree
    un = request.args["username"] 
    un = json.loads(un.replace("\'", "\""))["username"]
    top_games = get_top_games(un, 5)
    data = {
        "username" : un,
        "tg" : top_games
    }
    print(data)
    session['data'] = data
    return render_template("statistics.html", data=data)

@main.route("/about")
def about():
    return render_template("about.html", title="About")

@main.route("/test")
def test():
    with open('app/test_data.json') as json_file:
        data = json.load(json_file)
        session['tree'] = data
        session["location"] = ["mt"]
    return render_template("test.html", data=data)

@main.route("/tree_data")
def tree_data():
    move = request.args.get('move')
    moves = session["location"]
    moves.append(move)
    session["location"] = moves

    tree = session['tree']
    branch = get_by_path(tree, moves)
    branch = {key:to_keep_one(branch[key], "score") for key in branch if key != "score"}
    return(jsonify(branch))
