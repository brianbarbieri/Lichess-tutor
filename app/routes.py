from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    from app.logic.analysis import get_top_games
    data = get_top_games()
    return render_template('home.html', data=data)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
