from flask import Blueprint, render_template, redirect, url_for, request, flash


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')

@auth_bp.route('/register')
def register():
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    return render_template('auth/logout.html')



