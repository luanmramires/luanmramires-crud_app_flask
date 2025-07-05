from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import Income, Expense, Category, db
from sqlalchemy import func
from datetime import datetime, timedelta
import calendar

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Obter parâmetros de filtro
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    # Calcular datas de início e fim do mês
    start_date = datetime(year, month, 1).date()
    end_date = datetime(year, month, calendar.monthrange(year, month)[1]).date()
    
    # Buscar receitas e despesas do mês
    incomes = Income.query.filter(
        Income.user_id == current_user.id,
        Income.date >= start_date,
        Income.date <= end_date
    ).order_by(Income.date.desc()).all()
    
    expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).order_by(Expense.date.desc()).all()
    
    # Calcular totais
    total_income = sum(float(income.amount) for income in incomes)
    total_expense = sum(float(expense.amount) for expense in expenses)
    balance = total_income - total_expense
    
    # Dados para gráfico de pizza (receitas vs despesas)
    chart_data = {
        'labels': ['Receitas', 'Despesas'],
        'datasets': [{
            'data': [total_income, total_expense],
            'backgroundColor': ['#28a745', '#dc3545'],
            'borderColor': ['#28a745', '#dc3545'],
            'borderWidth': 2
        }]
    }
    
    # Dados para gráfico de despesas por categoria
    expense_by_category = db.session.query(
        Category.name,
        func.sum(Expense.amount).label('total')
    ).join(Expense).filter(
        Expense.user_id == current_user.id,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).group_by(Category.name).all()
    
    expense_chart_data = {
        'labels': [cat.name for cat in expense_by_category],
        'datasets': [{
            'data': [float(cat.total) for cat in expense_by_category],
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
            'borderWidth': 2
        }]
    }
    
    # Dados para gráfico de receitas por categoria
    income_by_category = db.session.query(
        Category.name,
        func.sum(Income.amount).label('total')
    ).join(Income).filter(
        Income.user_id == current_user.id,
        Income.date >= start_date,
        Income.date <= end_date
    ).group_by(Category.name).all()
    
    income_chart_data = {
        'labels': [cat.name for cat in income_by_category],
        'datasets': [{
            'data': [float(cat.total) for cat in income_by_category],
            'backgroundColor': ['#28a745', '#20c997', '#17a2b8', '#6f42c1', '#fd7e14', '#e83e8c'],
            'borderWidth': 2
        }]
    }
    
    # Estatísticas adicionais
    stats = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'income_count': len(incomes),
        'expense_count': len(expenses),
        'avg_income': total_income / len(incomes) if incomes else 0,
        'avg_expense': total_expense / len(expenses) if expenses else 0
    }
    
    return render_template('main/dashboard.html',
                         incomes=incomes,
                         expenses=expenses,
                         stats=stats,
                         chart_data=chart_data,
                         expense_chart_data=expense_chart_data,
                         income_chart_data=income_chart_data,
                         current_year=year,
                         current_month=month,
                         month_name=calendar.month_name[month])

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')

@main_bp.route('/api/dashboard-data')
@login_required
def dashboard_data():
    """API endpoint para dados do dashboard (para atualizações AJAX)"""
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    start_date = datetime(year, month, 1).date()
    end_date = datetime(year, month, calendar.monthrange(year, month)[1]).date()
    
    incomes = Income.query.filter(
        Income.user_id == current_user.id,
        Income.date >= start_date,
        Income.date <= end_date
    ).order_by(Income.date.desc()).all()
    
    expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).order_by(Expense.date.desc()).all()
    
    total_income = sum(float(income.amount) for income in incomes)
    total_expense = sum(float(expense.amount) for expense in expenses)
    
    return jsonify({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'income_count': len(incomes),
        'expense_count': len(expenses)
    })




