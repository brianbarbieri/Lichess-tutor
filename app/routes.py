from flask import render_template, request, Blueprint, redirect, url_for, flash
from app.config import Config  
from app.forms import PostForm
import json

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    form = PostForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        username_payload = {"username" : form.username.data}
        return redirect(url_for('main.statistics', username=username_payload))
    return render_template('home.html', form=form)

@main.route("/statistics")
def statistics():
    from app.logic.analysis import get_top_games, get_move_tree
    un = request.args['username'] 
    un = json.loads(un.replace("\'", "\""))["username"]
    top_games = get_top_games(un)
    move_tree = get_move_tree(un)
    data = {
        "username" : un,
        "tg" : top_games,
        "mt" : move_tree
    }
    return render_template('statistics.html', data=data)

@main.route("/about")
def about():
    return render_template('about.html', title='About')
