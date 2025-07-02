from flask import Blueprint, render_template
from flask_login import login_required,current_user


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/dashboard')
def dashboard():
    return render_template('main/dashboard.html')


@main_bp.route('/profile')
def profile():
    return render_template('main/profile.html')




