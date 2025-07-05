from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.forms import IncomeForm, ExpenseForm, CategoryForm
from app.models import Category, Income, Expense, db
from flask_login import login_required, current_user



finance_bp = Blueprint('finance', __name__)


@finance_bp.route('/expenses')
@login_required
def expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    categories = Category.query.filter_by(user_id=current_user.id, type='expense').all()
    return render_template('finance/expenses.html', expenses=expenses, categories=categories)

@finance_bp.route('/incomes')
@login_required
def incomes():
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).all()
    categories = Category.query.filter_by(user_id=current_user.id, type='income').all()
    return render_template('finance/incomes.html', incomes=incomes, categories=categories)

@finance_bp.route('/categories')
@login_required
def categories():
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.type, Category.name).all()
    return render_template('finance/categories.html', categories=categories)


@finance_bp.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    form = IncomeForm()
    # Buscar categorias de receita do usuário atual
    income_categories = Category.query.filter_by(user_id=current_user.id, type='income').all()
    form.category_id.choices = [(cat.id, cat.name) for cat in income_categories]
    if form.validate_on_submit():
        income = Income(description=form.description.data, amount=form.amount.data, date=form.date.data, user_id=current_user.id, category_id=form.category_id.data)
        db.session.add(income)
        db.session.commit()
        flash('Receita adicionada com sucesso!', 'success')
        return redirect(url_for('finance.incomes'))
    return render_template('finance/add_income.html', form=form)


@finance_bp.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    # Buscar categorias de despesa do usuario atual
    income_categories = Category.query.filter_by(user_id=current_user.id, type='expense').all()
    form.category_id.choices = [(cat.id, cat.name) for cat in income_categories]

    if form.validate_on_submit():
        expense = Expense(description=form.description.data,
                          amount=form.amount.data,
                          date=form.date.data,
                          user_id=current_user.id,
                          category_id=form.category_id.data,
                          )
        db.session.add(expense)
        db.session.commit()
        flash('Despesa adicionado com sucesso!', 'success')
        return redirect(url_for('finance.expenses'))
    return render_template('finance/add_expense.html', form=form)
    


@finance_bp.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, type=form.type.data, color=form.color.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()
        flash('Categoria adicionada com sucesso!', 'success')
        return redirect(url_for('finance.categories'))
    return render_template('finance/add_category.html', form=form)


@finance_bp.route('/delete_income/<int:id>')
@login_required
def delete_income(id):
    income = Income.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(income)
    db.session.commit()
    flash('Receita excluída com sucesso!', 'success')
    return redirect(url_for('finance.incomes'))

@finance_bp.route('/delete_expense/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash('Despesa excluída com sucesso!', 'success')
    return redirect(url_for('finance.expenses'))

@finance_bp.route('/delete_category/<int:id>')
@login_required
def delete_category(id):
    category = Category.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(category)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('finance.categories'))






