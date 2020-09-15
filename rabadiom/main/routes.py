from flask import render_template, request, Blueprint
from rabadiom.models import Post
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/Patient/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/Patient/about")
def about():
    return render_template('about.html', title='About')
