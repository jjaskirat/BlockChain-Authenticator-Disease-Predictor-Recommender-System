from flask import render_template, request, Blueprint
from rabadiom.models import Post
from flask_login import login_user, current_user, logout_user, login_required

doc_main = Blueprint('doc_main', __name__)


@doc_main.route("/Doctor/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('doc_home.html', posts= posts)


@doc_main.route("/Doctor/about")
def about():
    return render_template('doc_about.html', title='About')
