from flask import Blueprint, render_template


finance_bp = Blueprint('finance', __name__)


@finance_bp.route('/expenses')
def expenses():
    return render_template('finance/expenses.html')


@finance_bp.route('/incomes')
def incomes():
    return render_template('finance/incomes.html')


@finance_bp.route('/categories')
def categories():
    return render_template('finance/categories.html')


@finance_bp.route('/add_income')
def add_income():
    return render_template('finance/add_income.html')


@finance_bp.route('/add_expense')
def add_expense():
    return render_template('finance/add_expense.html')


@finance_bp.route('/add_category')
def add_category():
    return render_template('finance/add_category.html')






