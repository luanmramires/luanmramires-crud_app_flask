from flask import Blueprint, render_template, redirect, url_for, request, flash


auth_bp = Blueprint('auth', __name__)