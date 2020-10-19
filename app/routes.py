from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    from app.logic.analysis import get_top_games
    print(get_top_games())
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')
